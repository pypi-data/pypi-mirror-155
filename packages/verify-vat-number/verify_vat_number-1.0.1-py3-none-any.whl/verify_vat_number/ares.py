"""Load data from ARES at https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi."""
import logging
import xml.etree.ElementTree as ET
from typing import Dict, Optional, Tuple

import pycountry
import requests

from .data import VerifiedCompany
from .exceptions import (InvalidVatNumber, ServiceTemporarilyUnavailable, UnexpectedResponseFormat, VatNotFound,
                         VerifyVatException)
from .utils import strip_vat_id_number

SERVICE_URL = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi'
NS = {
      'are': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1',
      'dtt': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4',
      'udt': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/uvis_datatypes/v_1.0.1',
}

LOGGER = logging.getLogger(__name__)


def get_xml_content(vat_ident_number: str, service_url: str = None) -> bytes:
    """Get xml content from ARES."""
    url = SERVICE_URL if service_url is None else service_url
    LOGGER.info(f'{url}?ico={vat_ident_number}')
    try:
        response = requests.get(url, params={'ico': vat_ident_number})
    except requests.exceptions.Timeout as err:
        raise ServiceTemporarilyUnavailable(err)
    except requests.exceptions.RequestException as err:
        source = err.response.content if err.response else b''
        raise VerifyVatException(err, source=source)
    if not response.ok:
        raise VerifyVatException(f'[{response.status_code}] {response.reason}', source=response.content)
    if LOGGER.level >= logging.DEBUG:
        LOGGER.debug(response.content.decode('UTF-8'))
    return response.content


def get_xml_doc(vat_ident_number: str, service_url: str = None) -> Tuple[ET.Element, bytes]:
    """Get xml document from ARES."""
    content = get_xml_content(vat_ident_number, service_url)
    try:
        return ET.fromstring(content), content
    except ET.ParseError as err:
        raise VerifyVatException(err, source=content)


def get_from_cz_ares(vat_ident_number: str, service_url: str = None, ns: Dict[str, str] = None) -> VerifiedCompany:
    """Verify VAT identifier number by ARES. Return company name and address."""
    vat_ident_number = strip_vat_id_number(vat_ident_number)
    if vat_ident_number == '':
        raise InvalidVatNumber('Invalid number format.')
    if len(vat_ident_number) > 8:
        raise InvalidVatNumber('The number cannot be more than 8 digits long.')
    if ns is None:
        ns = NS
    root, source = get_xml_doc(vat_ident_number, service_url)

    check_error_code(root, ns, source)  # Raise ServiceTemporarilyUnavailable if dtt:Error_kod.

    query = './/are:Pocet_zaznamu'
    node = root.find(query, ns)
    if node is None:
        raise UnexpectedResponseFormat(query, source=source)
    if int(str(node.text)) != 1:
        raise VatNotFound(source=source)

    query = './/are:Adresa_ARES'
    address = root.find(query, ns)
    if address is None:
        raise UnexpectedResponseFormat(query, source=source)

    data = VerifiedCompany(company_name=get_text('.//are:Obchodni_firma', root, ns, source), address='',
                           country_code='CZ')

    query = 'dtt:Nazev_mestske_casti'
    node = address.find(query, ns)
    if node is not None:
        data.city = str(node.text)
    else:
        data.city = get_text('dtt:Nazev_obce', address, ns, source)

    data.district = f'{data.city} - ' + get_text('dtt:Nazev_casti_obce', address, ns, source)

    query = 'dtt:PSC'
    node = address.find(query, ns)
    if node is None:
        raise UnexpectedResponseFormat(query, source=source)
    data.postal_code = str(node.text)

    query = 'dtt:Nazev_ulice'
    node = address.find(query, ns)
    if node is None:
        street_name = data.city
    else:
        street_name = str(node.text)

    house_number = get_text('dtt:Cislo_domovni', address, ns, source)

    orientation_number = None
    query = 'dtt:Cislo_orientacni'
    node = address.find(query, ns)
    if node is not None:
        orientation_number = str(node.text)

    street_and_num = f'{street_name} {house_number}'
    if orientation_number:
        street_and_num += f'/{orientation_number}'
    data.street_and_num = street_and_num

    country_code: str = get_text('dtt:Kod_statu', address, ns, source)
    country: Optional[pycountry.db.Country] = pycountry.countries.get(numeric=country_code)
    if country is not None:
        data.country_code = country.alpha_2

    data.address = f'{data.street_and_num}\n{data.postal_code} {data.city}'
    return data


def check_error_code(root: ET.Element, ns: Dict[str, str], source: bytes) -> None:
    """Check if message has an Error code."""
    query = './/dtt:Error_kod'
    node = root.find(query, ns)
    if node is not None:
        message = f'Error code: {node.text}'
        query = './/dtt:Error_text'
        node = root.find(query, ns)
        if node is not None:
            message += f'; {node.text}'
        raise ServiceTemporarilyUnavailable(message, source=source)


def get_text(query: str, root: ET.Element, ns: Dict[str, str], source: bytes) -> str:
    """Get text from node.text selected by query."""
    node = root.find(query, ns)
    if node is None:
        raise UnexpectedResponseFormat(query, source=source)
    return str(node.text)
