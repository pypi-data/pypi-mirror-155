"""Patch pydicom.dataelem's DataElement_from_raw function."""
import contextlib
import dataclasses
import re
import typing as t

import pydicom.config as pydicom_config
import pydicom.dataelem as pydicom_dataelem
from dateutil.parser import ParserError, parse
from pydicom.charset import decode_string, default_encoding, encode_string
from pydicom.datadict import dictionary_VR, get_entry
from pydicom.dataelem import DataElement, RawDataElement
from pydicom.dataset import Dataset
from pydicom.multival import MultiValue
from pydicom.tag import BaseTag
from pydicom.valuerep import MAX_VALUE_LEN, TEXT_VR_DELIMS, DSclass
from pydicom.values import convert_value, validate_value

from .config import get_config
from .utils import generate_uid

__all__ = ["raw_elem_tracker"]

# pylint: disable=protected-access
private_vr_for_tag = pydicom_dataelem._private_vr_for_tag
LUT_DESCRIPTOR_TAGS = pydicom_dataelem._LUT_DESCRIPTOR_TAGS
# pylint: enable=protected-access


def char_range(a: str, b: str) -> t.List[str]:
    """Create a range of characters using ascii int values."""
    return [chr(v) for v in range(ord(a), ord(b) + 1)]


def tag_specific_fixer(
    raw: RawDataElement,
    **_kwargs,
) -> t.Tuple[RawDataElement, dict]:
    """Fixes for known specific tags."""
    # make sure that SpecificCharacterSet has correct VR
    if raw.tag == 0x00080005 and raw.VR != "CS":
        raw = raw._replace(VR="CS")
    # avoid conversion errors on surplus SequenceDelimitationItem tags
    if raw.tag == 0xFFFEE0DD and raw.VR != "OB":
        raw = raw._replace(VR="OB")
    return raw, {}


def replace_None_with_known_VR(
    raw: RawDataElement, dataset: t.Optional[Dataset] = None, **kwargs
) -> t.Tuple[RawDataElement, dict]:
    """Replace VR=None with VR found in the public or private dictionaries."""
    if (raw.VR is not None) and not kwargs.get("force_infer"):
        return raw, {}
    VR = raw.VR
    try:
        VR = dictionary_VR(raw.tag)
    except KeyError:
        # just read the bytes, no way to know what they mean
        if raw.tag.is_private:
            # VRs for private tags see PS3.5, 6.2.2
            VR = private_vr_for_tag(dataset, raw.tag)
        # group length tag implied in versions < 3.0
        elif raw.tag.element == 0:
            VR = "UL"
        else:
            VR = "UN"
    if VR != raw.VR:
        raw = raw._replace(VR=VR)
    return raw, {}


def replace_UN_with_known_VR(
    raw: RawDataElement, dataset: t.Optional[Dataset] = None, **_kwargs
) -> t.Tuple[RawDataElement, dict]:
    """Replace VR='UN' with VR found in the public or private dictionaries."""
    if raw.VR != "UN":
        return raw, {}
    VR = raw.VR
    if raw.tag.is_private:
        VR = private_vr_for_tag(dataset, raw.tag)
    elif raw.value is None or len(raw.value) < 0xFFFF:
        try:
            VR = dictionary_VR(raw.tag)
        except KeyError:
            pass
    if VR != raw.VR:
        raw = raw._replace(VR=VR)
    return raw, {}


# TBD wouldn't an allow-list be simpler/shorter?
# http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
backslash_compatible_VRs = (
    "AT,DS,FD,FL,IS,LT,OB,OB/OW,OB or OW,OF,OW,OW/OB,OW or OB,SL,SQ,SS,ST,UL,UN,US,UT"
).split(",")


def replace_backslash_in_VM1_str(
    raw: RawDataElement, **_kwargs
) -> t.Tuple[RawDataElement, dict]:
    r"""Replace invalid \ characters with _ in string VR values of VM=1."""
    try:
        VR, VM, *_ = get_entry(raw.tag)
    except KeyError:
        return raw, {}
    if VM == "1" and VR == raw.VR and VR not in backslash_compatible_VRs:
        value = raw.value
        if value and b"\\" in value:
            raw = raw._replace(value=value.replace(b"\\", b"_"))
    return raw, {}


def crop_text_VR(
    raw: RawDataElement,
    **kwargs,
) -> t.Tuple[RawDataElement, dict]:
    """Crop text VRs which are too long."""
    value = kwargs.get("value", raw.value)
    if raw.VR in MAX_VALUE_LEN and value:
        VR = t.cast(str, raw.VR)
        max_len = MAX_VALUE_LEN[VR]
        if len(value) > max_len:
            cropped = value[:max_len]
            raw = raw._replace(value=cropped)
            return raw, {"value": cropped}
    return raw, {}


def get_dictionary_VR_for_tag(
    tag: BaseTag, dataset: t.Optional[Dataset] = None
) -> t.Optional[str]:
    """Get the dictionary VR for a given tag."""
    VR = None
    try:
        VR = dictionary_VR(tag)
    except KeyError:
        if tag.is_private:
            # VRs for private tags see PS3.5, 6.2.2
            VR = private_vr_for_tag(dataset, tag)
        # Don't attempt to guess at other VRs
    return VR


def convert_exception_fixer(
    raw: RawDataElement,
    encoding: t.Optional[t.Union[str, t.List[str]]] = None,
    dataset: t.Optional[Dataset] = None,
    **_kwargs,
) -> t.Tuple[RawDataElement, dict]:
    """FW File convert_value handler.

    Will perform the following:
      - try loading elements with user-specified fallback VRs on failure
      - when all else fails, use VR=OB to just load the value as bytes
    """

    def _OB():
        """Shortcut to replace VR with OB.

        OB should allow any value to be converted successfully since it is just
        raw bytes (OB -> "Other Bytes")
        """
        return convert_exception_fixer(raw._replace(VR="OB"), encoding, dataset)

    config = get_config()
    VR = t.cast(str, raw.VR)
    value = None
    try:
        # Need to call both convert_value and DataElement Constructor here
        # because _some_ VRs have their `validate`
        # method called in `convert_value` and _some_ only have it called in
        # their `DataElement` constructor.
        #
        # For example, for the DA VR, convert_value returns a
        # pydicom.values.MultiString, which doesn't validate the actual format
        # of the value, only whether the value can be loaded into a
        # MultiString.
        #
        # Then the DataElement constructor actually constructs the VR class
        # which sees if the value can be loaded into a datetime
        #
        # References:
        #
        # DA converter called in convert_value:
        # https://github.com/pydicom/pydicom/blob/v2.2.2/pydicom/values.py#L170
        #
        # DA VR class instantiated:
        # https://github.com/pydicom/pydicom/blob/v2.2.2/pydicom/dataelem.py#L543

        pydicom_config.settings.reading_validation_mode = 2
        value = convert_value(VR, raw, encoding)
        DataElement(raw.tag, VR, value)
    except NotImplementedError:
        # Try one more time to infer VR.  We only get here if the VR is
        # explicitely set to something that we can't convert, i.e a VR that
        # doesn't exist, so we need to force inference, since VR is not None
        # and is not UN.
        raw, _ = replace_None_with_known_VR(raw, dataset=dataset, force_infer=True)
        return convert_exception_fixer(raw, encoding, dataset)
    except ValueError:
        # If we get a value error, it could be caused by either validate_value
        # or convert_value.

        # One possible reason could be that the VR is explicitely labelled
        # wrong.  So lets try a number of possible ones it could be.  For each
        # VR in the config, we validate the value.  If that fails we attempt to
        # fix it.  Then we pass this new VR and possibly fixed value into
        # convert_values.  If it still fails, move on, otherwise return with
        # this fix.
        VRs = config.fix_VR_mismatch_with_VRs if config.fix_VR_mismatch else []
        # We need to attempt to validate with the current VR as well
        VRs.append(VR)
        candidate = get_dictionary_VR_for_tag(raw.tag, dataset)
        if candidate and candidate not in VRs:
            VRs.append(candidate)
        for try_VR in VRs:
            # Temporary Value from attempt_to_fix
            tmp_val = raw.value
            try:
                # different VRs raise at different stages - run all
                # invalid IS raises in validate_value
                # invalid PN raises in DataElement.__init__, but only on a
                # converted value
                validate_value(try_VR, raw.value, 2)
                value = convert_value(try_VR, raw, encoding)
                DataElement(raw.tag, try_VR, value)
            except ValueError:
                # Try to fix value, or return original
                tmp_val = fix_invalid_VR_value(
                    try_VR, raw, encoding=encoding, dataset=dataset
                )
            try:
                # Avoid calling TrackedRawDataElement._replace here since we
                # don't want this value change tracked
                tmp = RawDataElement._replace(raw, value=tmp_val)
                value = convert_value(try_VR, tmp, encoding)
                DataElement(raw.tag, try_VR, tmp_val)
            except ValueError:
                continue
            # Replace VR and value if fixed.
            raw = raw._replace(VR=try_VR) if try_VR != VR else raw
            raw = raw._replace(value=tmp_val) if tmp_val != raw.value else raw
            return convert_exception_fixer(raw, encoding, dataset)
        return _OB()
    except Exception:  # pylint: disable=broad-except
        # Any other unforeseen exception in conversion
        return _OB()
    return raw, {"value": value}


def fix_uids(raw: RawDataElement, **_kwargs) -> t.Optional[bytes]:
    """Attempt to fix an invalid UID.

    * Determine if UID "looks" valid
    * If so, use this value as only entropy source to generate new UID
    (deterministic)
    * Otherwise, generate a new UID
    """
    VALID_THRESHOLD = 0.8
    FIX_TAGS = (
        (0x0020, 0x000E),  # SeriesInstanceUID
        (0x0020, 0x000D),  # StudyInstanceUID
        (0x0020, 0x0052),  # FrameOfReferenceUID
        (0x0008, 0x0018),  # SOPInstanceUID
        (0x0008, 0x1155),  # ReferencedSOPInstanceUID
    )

    if raw.tag not in FIX_TAGS:
        return raw.value

    val = raw.value.decode()  # type: ignore
    tmp = []
    for part in val.split("."):
        tmp.append(part.lstrip("0") if part != "0" else part)
    new = ".".join(tmp)
    # Try to validate value stripped of 0's
    try:
        validate_value("UI", new, validation_mode=2)
        return new.encode(encoding="ascii")
    except ValueError:
        pass
    # Assume not valid if length is less than 5
    if len(new) > 5:
        # If all characters are numbers or periods, it "looks" valid
        allowed_chars = [*char_range("0", "9"), "."]
        valid = 0
        for c in new:
            if c in allowed_chars:
                valid += 1
        # If more than xx% of characters are valid, assume it "looks" like a UID
        if float(valid) / float(len(new)) > VALID_THRESHOLD:
            return generate_uid(entropy_srcs=[new]).encode("ascii")
    return generate_uid().encode("ascii")


def fix_datetimes(raw: RawDataElement, **_kwargs) -> t.Optional[bytes]:
    """Attempt to parse an invalid date and format correctly."""
    # TZ handling could be added by splitting on "-" or "+" if needed
    try:
        date = parse(raw.value.decode())  # type: ignore
        if raw.VR == "DA":
            fmt_dt = date.strftime("%Y%m%d")
        elif raw.VR == "DT":
            fmt_dt = date.strftime("%Y%m%d%H%M%S.%f%z")
        else:
            fmt_dt = date.strftime("%H%M%S.%f%z")
        fmt_dt = fmt_dt.rstrip("0")
        if fmt_dt[-1] == ".":
            fmt_dt += "0"
        return fmt_dt.encode(encoding="ascii")
    except (ParserError, OverflowError):
        return raw.value


def fix_AS(raw: RawDataElement, **_kwargs) -> t.Optional[bytes]:
    """Fixer for AS strings.

    Ensure one of D,W,M,Y is at end of the string, and pad to 4 characters.

    If no time quantifier is present, assume Years, this is in line with
    fw_file.dicom.utils.get_session_age.
    """
    age_str = raw.value.decode().upper()  # type: ignore
    match = re.match(r"(?P<value>[0-9]+)(?P<scale>[dwmyDWMY]*)", age_str)
    if match:
        # Pad value to 3 chars with preceding 0s
        new_val = match.group("value").lstrip("0")
        if len(new_val) > 3 or (match.group("scale") and len(match.group("scale")) > 1):
            # Don't want to lose information, but not valid, just return and let VR
            # be set to OB
            return raw.value
        pad = 3 - len(new_val)
        if pad:
            new_val = "0" * pad + new_val
        new_val += match.group("scale") if match.group("scale") else "Y"
        return new_val.encode(encoding="ascii")
    return raw.value


def fix_number_strings(raw: RawDataElement, **_kwargs) -> t.Optional[bytes]:
    """Fix DS (Decimal String) and IS (Integer String) number strings.

    * Remove invalid characters
    * Truncate floats in IS VR
    """
    # Fix invalid values in number string
    DS_allowed = [*char_range("0", "9"), "E", "e", ".", "+", "-"]
    val = raw.value.decode()  # type: ignore
    new_parts = []
    for part in val.split("\\"):
        new_parts.append("".join(c if c in DS_allowed else "" for c in part))
    new_val = "\\".join(new_parts).encode(encoding="ascii")
    # If still not valid, return original value, VR will be changed to OB to be decoded.
    try:
        DataElement(raw.tag, "DS", new_val)
    except ValueError:
        return raw.value
    # Fix decimal value in IS
    if raw.VR == "IS":
        if not any(c in new_val for c in b".eE"):  # DS handles decimals/exp style
            return new_val
        # Try to convert as DS
        tmp = RawDataElement._replace(raw, value=new_val)
        value = convert_value("DS", tmp)
        # TODO consider logging vs warnings, apply as needed
        if isinstance(value, (MultiValue, list, tuple)):
            value = "\\".join((str(int(v)) for v in value))
        else:
            assert isinstance(value, DSclass)
            value = str(int(value))
        # pylint: disable=unexpected-keyword-arg
        return value.encode(encoding="ascii")
        # pylint: enable=unexpected-keyword-arg
    return new_val


def fix_invalid_char(
    raw: RawDataElement,
    encoding: t.Optional[t.Union[str, t.List[str]]] = None,
    **_kwargs,
) -> t.Optional[bytes]:
    """Attempt to remove non-printable characters from byte decoding."""
    orig_validation_mode = pydicom_config.settings.reading_validation_mode
    pydicom_config.settings.reading_validation_mode = 0
    if not encoding:
        encoding = [default_encoding]  # pragma: no cover
    elif not isinstance(encoding, list):
        encoding = [encoding]  # pragma: no cover
    assert isinstance(raw.value, bytes)
    val = decode_string(raw.value, encodings=encoding, delimiters=TEXT_VR_DELIMS)
    new_val = ""
    for char in val:
        new_val += char if char.isprintable() else "_"
    pydicom_config.settings.reading_validation_mode = orig_validation_mode
    return encode_string(new_val, encodings=encoding)


VR_FIXERS = {
    "DA": fix_datetimes,
    "DT": fix_datetimes,
    "TM": fix_datetimes,
    "AS": fix_AS,
    "UI": fix_uids,
    "DS": fix_number_strings,
    "IS": fix_number_strings,
    "SH": fix_invalid_char,
    "LO": fix_invalid_char,
    "ST": fix_invalid_char,
    "PN": fix_invalid_char,
    "LT": fix_invalid_char,
    "UC": fix_invalid_char,
    "UT": fix_invalid_char,
}


def fix_invalid_VR_value(  # pylint: disable=too-many-return-statements
    VR: str,
    raw: RawDataElement,
    dataset: t.Optional[Dataset] = None,
    encoding: t.Optional[t.Union[str, t.List[str]]] = None,
) -> t.Optional[bytes]:
    """Try to fix an invalid value for the given VR.

    Returns:
        Either a fixed value, or the original
    """
    # DICOM VR reference
    # https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html

    # Date, Datetime, Time
    assert raw.value
    if VR in VR_FIXERS:
        fixer = VR_FIXERS[VR]
        return fixer(raw, dataset=dataset, encoding=encoding)  # type: ignore
    if VR == "CS":
        # Naively try to convert to uppercase as defined in the VR spec:
        new_val = raw.value.decode().upper()
        return new_val.encode(encoding="ascii")
    return raw.value  # pragma: no cover


def LUT_descriptor_fixer(
    raw: RawDataElement, **kwargs
) -> t.Tuple[RawDataElement, dict]:
    """Fix LUT Descriptor tags."""
    # Value has already been converted, so value is a native python type,
    # not bytes
    value = kwargs.get("value", None)
    if raw.tag in LUT_DESCRIPTOR_TAGS and value:
        try:
            if value[0] < 0:
                value[0] += 65536  # type: ignore
        except TypeError:  # pragma: no cover
            pass
    return raw, {"value": value}


def DataElement_from_raw(  # pylint: disable=too-many-branches
    raw: RawDataElement,
    encoding: t.Optional[t.Union[str, t.List[str]]] = None,
    dataset: t.Optional[Dataset] = None,
) -> DataElement:
    """Override pydicom's DataElement_from_raw.

    This implementation separates the existing (as of pydicom 2.2.x)
    DataElement_from_raw into unit functions which are called in order.

    All these functions are accessible and configurable as user functions.
    FW File provides sensible defaults for these functions.
    """
    config = get_config()
    orig_validation = pydicom_config.settings.reading_validation_mode
    pydicom_config.settings.reading_validation_mode = 2
    # Hardcode tracker first since user still needs to opt in
    tracker = pydicom_config.data_element_callback_kwargs.get("tracker")
    if tracker:
        raw = tracker.track(raw)
    fixer_kwargs: t.Dict[str, t.Any] = {}
    for fn in config.raw_elem_fixers:
        fn = t.cast(t.Callable, fn)
        raw, out_kwargs = fn(
            raw,
            encoding=encoding,
            dataset=dataset,
            **fixer_kwargs,
            **pydicom_config.data_element_callback_kwargs,
        )
        fixer_kwargs.update(out_kwargs)
    VR = t.cast(str, raw.VR)
    if fixer_kwargs.get("value", None):
        # Allow user to set converted value in fixers.
        value = fixer_kwargs.get("value")
    else:
        # Otherwise assume fixers have already ensured that convert_values
        # will not raise.
        value = convert_value(VR, raw, encoding)
    if tracker:
        tracker.update(raw)
    de = DataElement(
        raw.tag,
        VR,
        value,
        raw.value_tell,
        raw.length == 0xFFFFFFFF,
        already_converted=True,
    )
    pydicom_config.settings.reading_validation_mode = orig_validation
    return de


@dataclasses.dataclass
class ReplaceEvent:
    """Dataclass to hold tracking event information."""

    field: str
    old: t.Optional[str]
    new: str

    def __repr__(self):
        """Return representation of tracking event."""
        return f"Replace {self.field}: {self.old} -> {self.new}"


class TrackedRawDataElement(RawDataElement):
    """RawDataElement subclass adding change tracking to _replace events."""

    id_: int
    original: RawDataElement
    events: t.List[ReplaceEvent]

    def __new__(cls, *args, id_=None, **kwargs) -> "TrackedRawDataElement":
        """Return a new TrackedRawDataElement instance."""
        tracked = super().__new__(cls, *args, **kwargs)
        tracked.id_ = id_
        tracked.original = RawDataElement(*args, **kwargs)
        tracked.events = []
        return tracked

    # pylint: disable=arguments-differ
    def _replace(self, **kwargs) -> "TrackedRawDataElement":
        """Extend namedtuple _replace with change event tracking."""
        for key, val in kwargs.items():
            old = getattr(self, key)
            event = ReplaceEvent(field=key, old=old, new=val)
            self.events.append(event)
        raw = super()._replace(**kwargs)  # calls new
        # NOTE updating the extra namedtuple attrs
        raw.original = self.original
        raw.events = self.events
        raw.id_ = self.id_
        return raw

    def export(self) -> dict:
        """Return the original dataelem, the events and the final version as a dict."""
        return {
            "original": self.original,
            "events": self.events,
            "final": self,
        }


def filter_none_vr_replacement(event: ReplaceEvent) -> bool:
    """Return True except for VR=None replacement events."""
    return not (event.field == "VR" and event.old is None)


class Tracker:
    """Tracker for RawDataElement change events within a dataset."""

    def __init__(self):
        """Initializes the tracker instance."""
        self.data_element_dict: t.Dict[int, TrackedRawDataElement] = {}

    @property
    def data_elements(self) -> t.List[TrackedRawDataElement]:
        """Expose data_elements as a list for backwards compat."""
        return list(self.data_element_dict.values())

    # NOTE: We need to us hash, and not ID to store the unique id.  hash looks
    # at the values of the object, whereas id looks at the location in memory.
    # id is guarenteed to be unique while objects overlap in lifetime, but due
    # to this implementation, RawDataElements won't be overlapping in life
    # time, and due to RawDataElement being a namedtuple with a very definite
    # size, they are often stored at the same location in memory.  So you can
    # end up with id returning the same value for two different
    # RawDataElements.

    def track(self, raw: RawDataElement) -> TrackedRawDataElement:
        """Return a TrackedRawDataElement from a RawDataElement."""
        # Store a unique id for each Tracked element, and use it to update the
        # _data_element_dict on Tracker
        # This needs to be `hash`, not `id`, see note above
        dict_key = hash(raw)
        # Can't actually think of a use case here.  We'd have to be calling
        # `track` on the same RawDataElement again, which would have already
        # been decoded.
        if dict_key in self.data_element_dict:
            return self.data_element_dict[dict_key]  # pragma: no cover
        tracked_elem = TrackedRawDataElement(*raw, id_=dict_key)
        self.data_element_dict[dict_key] = tracked_elem
        return tracked_elem

    def update(self, tr_raw: TrackedRawDataElement) -> None:
        """Update a TrackedRawDataElement."""
        self.data_element_dict[tr_raw.id_] = tr_raw

    def trim(self, event_filter: t.Callable = None) -> None:
        """Filter tracked events and remove data elements without any changes."""
        if not event_filter:
            event_filter = filter_none_vr_replacement
        for key in list(self.data_element_dict):
            de = self.data_element_dict[key]
            de.events = [evt for evt in de.events if event_filter(evt)]
            if not de.events:
                self.data_element_dict.pop(key)

    def __repr__(self):
        """Return representation of the tracker instance."""
        strings = []
        for raw in self.data_elements:
            trace = raw.export()
            events = "None"
            if trace["events"]:
                events = "\n" + "\n".join([f"\t{e}" for e in trace["events"]])
            strings.append(
                f"- original: {trace['original']}\n"
                f"  events: {events}\n"
                f"  final: {trace['final']}\n"
            )
        return "\n".join(strings)


@contextlib.contextmanager
def raw_elem_tracker(tracker: Tracker = None) -> t.Iterator[None]:
    """Context manager for tracking changes made to RawDataElements."""
    orig_tracker = pydicom_config.data_element_callback_kwargs.get("tracker")
    pydicom_config.data_element_callback_kwargs["tracker"] = tracker
    try:
        yield
    finally:
        pydicom_config.data_element_callback_kwargs["tracker"] = orig_tracker
