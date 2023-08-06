"""Dataclass VerifiedCompany with verified values."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class VerifiedCompany:
    """Company name and address verified by VAT number."""

    company_name: str
    address: str
    street_and_num: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    district: Optional[str] = None
    country_code: Optional[str] = None
