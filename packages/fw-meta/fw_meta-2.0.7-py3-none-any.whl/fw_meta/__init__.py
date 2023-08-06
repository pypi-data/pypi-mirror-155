"""Flywheel meta extractor."""
# pylint: disable=unused-import
try:
    from importlib.metadata import version
except ImportError:  # pragma: no cover
    from importlib_metadata import version  # type: ignore

__version__ = version(__name__)

from .exports import ExportFilter, ExportRule, ExportTemplate
from .imports import MetaData, MetaExtractor, extract_meta
