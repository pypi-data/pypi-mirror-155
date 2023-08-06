"""Utils for VAT numbers."""
import re


def strip_vat_reg_number(number: str) -> str:
    """Remove all characters except letters and numbers."""
    return re.sub(r'[\W_]+', '', number)


def strip_vat_id_number(number: str) -> str:
    """Remove all characters except numbers."""
    return re.sub(r'\D+', '', number)
