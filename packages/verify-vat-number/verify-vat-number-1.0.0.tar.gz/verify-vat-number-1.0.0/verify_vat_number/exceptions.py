"""Module exceptions."""
import xml.etree.ElementTree as ET
from typing import Dict, Optional, Union


class VerifyVatException(Exception):
    """Basic module exception."""

    def __init__(
            self,
            message: Union[Exception, str, Dict] = None,
            source: Union[bytes, ET.Element, str] = None
            ) -> None:
        """Initialize exception with estra attribute 'source'."""
        super().__init__(message)
        self._source = source

    @property
    def source(self) -> Optional[str]:
        """Source from which the error raised."""
        if isinstance(self._source, ET.Element) or hasattr(self._source, 'tag'):
            return ET.tostring(self._source, encoding='unicode')  # type: ignore
        elif isinstance(self._source, bytes):
            return self._source.decode('utf-8')
        return self._source


class ServiceTemporarilyUnavailable(VerifyVatException):
    """The service is temporarily unavailable."""


class VatNotFound(VerifyVatException):
    """Vat number was not found."""


class UnexpectedResponseFormat(VerifyVatException):
    """Unexpected format of response."""


class InvalidVatNumber(VerifyVatException):
    """Invalid VAT number."""


class UnsupportedCountryCode(InvalidVatNumber):
    """Unsupported country code."""
