"""Flywheel utilities and common helpers."""
# pylint: disable=unused-import
try:
    from importlib.metadata import version
except ImportError:  # pragma: no cover
    from importlib_metadata import version  # type: ignore

__version__ = version(__name__)

from .datetime import ZoneInfo, format_datetime, get_datetime, get_tzinfo
from .dicts import AttrDict, attrify, flatten_dotdict, get_field, inflate_dotdict
from .files import AnyFile, AnyPath, BinFile, TempDir, TempFile, fileglob, open_any
from .filters import (
    BaseFilter,
    ExpressionFilter,
    Filters,
    IncludeExcludeFilter,
    NumberFilter,
    SetFilter,
    SizeFilter,
    StringFilter,
    TimeFilter,
)
from .formatters import (
    Template,
    Timer,
    format_template,
    hrsize,
    hrtime,
    pluralize,
    quantify,
    report_progress,
)
from .parsers import (
    Pattern,
    parse_field_name,
    parse_hrsize,
    parse_hrtime,
    parse_pattern,
    parse_url,
)
from .state import Cached
from .testing import assert_like
