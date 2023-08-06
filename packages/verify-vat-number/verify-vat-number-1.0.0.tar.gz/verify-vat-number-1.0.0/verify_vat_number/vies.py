"""
VIES VAT number validation.

https://ec.europa.eu/taxation_customs/vies/
"""
import logging
import re
import xml.etree.ElementTree as ET
from datetime import date
from typing import Dict, NamedTuple, Optional

import zeep
from requests.exceptions import RequestException, Timeout
from zeep.exceptions import Error as ZeepError
from zeep.plugins import HistoryPlugin

from .data import VerifiedCompany
from .exceptions import (InvalidVatNumber, ServiceTemporarilyUnavailable, UnsupportedCountryCode, VatNotFound,
                         VerifyVatException)
from .utils import strip_vat_reg_number

SERVICE_URL = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"
COUNTRY_CODES = {
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CY': 'Cyprus',
    'CZ': 'Czechia',
    'DE': 'Germany',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'EL': 'Greece',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IT': 'Italy',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    'MT': 'Malta',
    'NL': 'The Netherlands',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'XI': 'Northern Ireland',
}

PATTERNS = (
    re.compile(r'(?P<street_and_num>.+)\n(?P<district>.+)\n\s*(?P<postal_code>\d{3}\s*\d{2})\s+(?P<city>.+)'),
    re.compile(r'(?P<street_and_num>.+)\n\s*(?P<postal_code>\d{3}\s*\d{2})\s+(?P<city>.+)'),
    re.compile(r'(?P<street_and_num>.+)\n\s*(?P<postal_code>L-\d+)\s+(?P<city>.+)$'),
    re.compile(r'(?P<street_and_num>.+)\n(?P<district>.+)\n\s*(?P<postal_code>\d+\w*(-\d+)?)\s+(?P<city>.+)'),
    re.compile(r'(?P<street_and_num>.+)\n\s*(?P<postal_code>\d+\w*(-\d+)?)\s+(?P<city>.+)'),
    re.compile(r'(?P<street_and_num>.+),(?P<district>.+),\s*(?P<postal_code>\d+)\s+(?P<city>.+)'),
    re.compile(r'(?P<street_and_num>.+),(?P<district>.+),(?P<city>.+)'),
    re.compile(r'(?P<street_and_num>.+)\s+(?P<postal_code>\d+)\s+(?P<city>.+)$'),
)


PATTERNS_COUNTRY = {
    'SK': (
        re.compile(r'(?P<street_and_num>.+)\n(?P<postal_code>\d{3}\s*\d{2})\s+(?P<city>.+)\n(?P<country>.+)'),
    ) + PATTERNS,
    'BG': (
        re.compile(r'(?P<street_and_num>.+),(?P<city>.+)\s+(?P<postal_code>\d+)'),
    ) + PATTERNS,
    'EL': (
        re.compile(r'(?P<street_and_num>.+)\s+(?P<postal_code>\d+)\s+-\s+(?P<city>.+)'),
        re.compile(r'(?P<street_and_num>.+)\s+(?P<postal_code>\d+)\s+(?P<city>.+)'),
    ) + PATTERNS,
    'EE': (
        re.compile(r'(?P<street_and_num>.+)\s+(?P<postal_code>\d{5})\s+(?P<city>.+)'),
    ) + PATTERNS,
    'IE': (
        re.compile(r'(?P<street_and_num>.+),\s*(?P<city>.+)$'),
    ) + PATTERNS,
    'LV': (
        re.compile(r'(?P<street_and_num>.+),\s*(?P<city>.+),\s*(?P<district>.+),\s*(?P<postal_code>\w+-\d+)'),
        re.compile(r'(?P<street_and_num>.+),\s*(?P<city>.+),\s*(?P<postal_code>\w+-\d+)'),
    ) + PATTERNS,
    'MT': (
        re.compile(r'(?P<street_and_num>.+\n.+\n.+)\n(?P<postal_code>.+)\n(?P<city>.+)'),
        re.compile(r'(?P<street_and_num>.+\n.+)\n(?P<postal_code>.+)\n(?P<city>.+)'),
    ) + PATTERNS,
    'RO': (
        re.compile(r'(?P<city>.+)\n(?P<street_and_num>.+\n.+)'),
        re.compile(r'(?P<city>.+)\n(?P<street_and_num>.+)'),
    ),  # + PATTERNS is intentionally omitted because RO patterns are in conflict with others.
}

LOGGER = logging.getLogger(__name__)

# Here is the list of VAT Number to use to receive each kind of answer:
#   100 = Valid request with Valid VAT Number
#   200 = Valid request with an Invalid VAT Number
#   201 = Error: INVALID_INPUT
#   202 = Error: INVALID_REQUESTER_INFO
#   300 = Error: SERVICE_UNAVAILABLE
#   301 = Error: MS_UNAVAILABLE
#   302 = Error: TIMEOUT
#   400 = Error: VAT_BLOCKED
#   401 = Error: IP_BLOCKED
#   500 = Error: GLOBAL_MAX_CONCURRENT_REQ
#   501 = Error: GLOBAL_MAX_CONCURRENT_REQ_TIME
#   600 = Error: MS_MAX_CONCURRENT_REQ
#   601 = Error: MS_MAX_CONCURRENT_REQ_TIME For all the other cases,
#                The web service will responds with a "SERVICE_UNAVAILABLE" error
TIMEOUT_ERROR_CODES = (
    'SERVICE_UNAVAILABLE',  # An error was encountered either at the network level or the Web application level.
    'MS_UNAVAILABLE',  # The application at the Member State is not replying or not available.
    'TIMEOUT',  # The application did not receive a reply within the allocated time period.
    'GLOBAL_MAX_CONCURRENT_REQ',  # The maximum number of concurrent requests has been reached.
    'MS_MAX_CONCURRENT_REQ',  # The maximum number of concurrent requests for this Member State has been reached.
)
UNPUBLISHED_DATA = '---'


class checkVatResponse(NamedTuple):
    """zeep.objects.checkVatResponse."""

    countryCode: str
    vatNumber: str
    requestDate: date
    valid: bool
    name: Optional[str]
    address: Optional[str]


def verify_vat(vat_registration_number: str, service_url: str = None) -> checkVatResponse:
    """Verify VAT registration number by VIES."""
    vat_registration_number = strip_vat_reg_number(vat_registration_number)
    if vat_registration_number == '':
        raise InvalidVatNumber('Invalid number format.')
    country_code = vat_registration_number[:2].upper()
    registration_number = vat_registration_number[2:]
    if country_code not in COUNTRY_CODES:
        raise UnsupportedCountryCode(country_code)
    url = SERVICE_URL if service_url is None else service_url
    LOGGER.info(f'{url} Country code: {country_code} VAT: {registration_number}')
    history = HistoryPlugin()
    try:
        client = zeep.Client(wsdl=url, plugins=[history])
        data = client.service.checkVat(countryCode=country_code, vatNumber=registration_number)
    except FileNotFoundError as err:
        raise VerifyVatException(err)
    except Timeout as err:
        raise ServiceTemporarilyUnavailable(err)
    except ZeepError as err:
        if str(err) in TIMEOUT_ERROR_CODES:
            raise ServiceTemporarilyUnavailable(err, source=get_last_received_envelope(history))
        raise VerifyVatException(err, source=get_last_received_envelope(history))
    except RequestException as err:
        source = err.response.content if err.response else b''
        raise VerifyVatException(err, source=source)
    if LOGGER.level == logging.DEBUG:
        element = get_last_received_envelope(history)
        if element is not None:
            LOGGER.debug(ET.tostring(element, encoding='unicode'))
    if not data.valid:
        raise VatNotFound(source=get_last_received_envelope(history))
    return data


def get_from_eu_vies(vat_registration_number: str, service_url: str = None) -> VerifiedCompany:
    """Verify VAT registration number by VIES. Return company name and address."""
    data = verify_vat(vat_registration_number, service_url)
    company_name = UNPUBLISHED_DATA if data.name is None else data.name.strip()
    address = UNPUBLISHED_DATA if data.address is None else data.address.strip()
    response = VerifiedCompany(company_name=company_name, address=address)
    if address == UNPUBLISHED_DATA:
        return response
    for key, value in parse_address(vat_registration_number[:2].upper(), response.address).items():
        setattr(response, key, value)
    # The language code is 'EL' according to ISO 639-1, 'GR' is the country code according to ISO 3166.
    response.country_code = {'EL': 'GR'}.get(data.countryCode, data.countryCode)
    return response


def parse_address(country_code: str, address: str) -> Dict[str, str]:
    """Parse address."""
    response: Dict[str, str] = {}
    patterns = PATTERNS_COUNTRY.get(country_code, PATTERNS)
    for pattern in patterns:
        match = pattern.match(address)
        if match is not None:
            return {key: value.strip() for key, value in match.groupdict().items()}
    return response


def get_last_received_envelope(history: HistoryPlugin) -> Optional[ET.Element]:
    """Get last received envelope."""
    try:
        if history.last_received is not None:
            return history.last_received.get('envelope')
    except IndexError:
        pass
    return None
