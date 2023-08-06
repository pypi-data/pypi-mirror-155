import os
from datetime import date
from unittest import TestCase
from unittest.mock import patch, sentinel

import responses
from requests.exceptions import RequestException, Timeout
from zeep.exceptions import Error as ZeepError
from zeep.plugins import HistoryPlugin

from verify_vat_number.data import VerifiedCompany
from verify_vat_number.exceptions import (InvalidVatNumber, ServiceTemporarilyUnavailable, UnsupportedCountryCode,
                                          VatNotFound, VerifyVatException)
from verify_vat_number.vies import get_from_eu_vies, get_last_received_envelope, parse_address, verify_vat


def get_envelope(
        address: str,
        company_name: str = 'CZ.NIC, z.s.p.o.',
        vat_number: str = '67985726',
        country_code: str = 'CZ'
        ) -> bytes:
    """Get Envelope."""
    return f"""
        <ns0:Envelope
            xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:ns1="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
        <ns0:Body>
            <ns1:checkVatResponse>
                <ns1:countryCode>{country_code}</ns1:countryCode>
                <ns1:vatNumber>{vat_number}</ns1:vatNumber>
                <ns1:requestDate>2022-05-20+02:00</ns1:requestDate>
                <ns1:valid>true</ns1:valid>
                <ns1:name>{company_name}</ns1:name>
                <ns1:address>{address}</ns1:address>
            </ns1:checkVatResponse>
        </ns0:Body>
    </ns0:Envelope>""".encode('utf-8')


def get_envelope_private_data():
    return """
        <ns0:Envelope
            xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:ns1="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
            <ns0:Body>
                <ns1:checkVatResponse>
                    <ns1:countryCode>DE</ns1:countryCode>
                    <ns1:vatNumber>306401413</ns1:vatNumber>
                    <ns1:requestDate>2022-06-09+02:00</ns1:requestDate>
                    <ns1:valid>true</ns1:valid>
                    <ns1:name>---</ns1:name>
                    <ns1:address>---</ns1:address>
                </ns1:checkVatResponse>
            </ns0:Body>
        </ns0:Envelope>"""


def get_envelope_vat_is_false():
    return """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <checkVatResponse xmlns="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
                    <countryCode>CZ</countryCode>
                    <vatNumber>67985728</vatNumber>
                    <requestDate>2022-05-18+02:00</requestDate>
                    <valid>false</valid>
                    <name>---</name>
                    <address>---</address>
                </checkVatResponse>
            </soap:Body>
        </soap:Envelope>"""


def get_unexpected_envelope():
    return """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <checkVatResponse xmlns="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
                    <countryCode>CZ</countryCode>
                    <vatNumber>67985728</vatNumber>
                    <requestDate>2022-05-18+02:00</requestDate>
                    <valid>true</valid>
                </checkVatResponse>
            </soap:Body>
        </soap:Envelope>"""


def get_wsdl_content() -> bytes:
    """Get WSDL content."""
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vies-checkVatService.wsdl')
    with open(filepath, 'rb') as handle:
        return handle.read()


class TestVies(TestCase):

    url = 'https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    service_url = 'https://ec.europa.eu/taxation_customs/vies/services/checkVatService'
    logger_name = 'verify_vat_number.vies'
    address = "Milešovská 1136/5\nPRAHA 3 - VINOHRADY\n130 00  PRAHA 3"

    def test_verify_vat_empty_number(self):
        with self.assertRaisesRegex(InvalidVatNumber, 'Invalid number format.'):
            verify_vat('!')

    def test_verify_vat_unsupported_country_code(self):
        with self.assertRaisesRegex(UnsupportedCountryCode, 'GB'):
            verify_vat('GB123456789')

    def test_verify_vat_file_not_found(self):
        with self.assertRaises(VerifyVatException) as context:
            verify_vat('CZ67985726', 'foo')
        self.assertIsNone(context.exception.source)

    def test_verify_vat_timeout(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=Timeout())
            with self.assertRaises(ServiceTemporarilyUnavailable) as context:
                verify_vat('CZ67985726')
        self.assertIsNone(context.exception.source)

    def test_verify_vat_request_exception(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=RequestException())
            with self.assertRaises(VerifyVatException) as context:
                verify_vat('CZ67985726')
        self.assertEqual(context.exception.source, '')

    def test_verify_vat_request_exception_check_vat(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=get_wsdl_content())
            rsps.add(responses.POST, self.service_url, body=RequestException())
            with self.assertRaises(VerifyVatException) as context:
                verify_vat('CZ67985726')
        self.assertEqual(context.exception.source, '')

    def test_verify_vat_zeep_error_service_unavailable(self):
        content = """<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/">
                <ns0:Body>
                    <ns0:Fault>
                        <faultcode>soap:Server</faultcode>
                        <faultstring>SERVICE_UNAVAILABLE</faultstring>
                    </ns0:Fault>
                </ns0:Body>
            </ns0:Envelope>"""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=get_wsdl_content())
            rsps.add(responses.POST, self.service_url, body=content)
            with self.assertRaises(ServiceTemporarilyUnavailable) as context:
                verify_vat('CZ67985726')
        self.assertEqual(context.exception.source, content)

    def test_verify_vat_zeep_error_ms_unavailable(self):
        content = """<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/">
                <ns0:Body>
                    <ns0:Fault>
                        <faultcode>soap:Server</faultcode>
                        <faultstring>MS_UNAVAILABLE</faultstring>
                    </ns0:Fault>
                </ns0:Body>
            </ns0:Envelope>"""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=get_wsdl_content())
            rsps.add(responses.POST, self.service_url, body=content)
            with self.assertRaisesRegex(ServiceTemporarilyUnavailable, 'MS_UNAVAILABLE') as context:
                verify_vat('CZ67985726')
        self.assertEqual(context.exception.source, content)

    def test_verify_vat_zeep_error_timeout(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=ZeepError('TIMEOUT'))
            with self.assertRaisesRegex(ServiceTemporarilyUnavailable, 'TIMEOUT') as context:
                verify_vat('CZ67985726')
        self.assertIsNone(context.exception.source)

    def test_verify_vat_zeep_error_global_max_concurrent_req(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=ZeepError('GLOBAL_MAX_CONCURRENT_REQ'))
            with self.assertRaisesRegex(ServiceTemporarilyUnavailable, 'GLOBAL_MAX_CONCURRENT_REQ') as context:
                verify_vat('CZ67985726')
        self.assertIsNone(context.exception.source)

    def test_verify_vat_zeep_error_ms_max_concurrent_req(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=ZeepError('MS_MAX_CONCURRENT_REQ'))
            with self.assertRaisesRegex(ServiceTemporarilyUnavailable, 'MS_MAX_CONCURRENT_REQ') as context:
                verify_vat('CZ67985726')
        self.assertIsNone(context.exception.source)

    def test_verify_vat_zeep_error_other(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=ZeepError('VAT_BLOCKED'))
            with self.assertRaisesRegex(VerifyVatException, 'VAT_BLOCKED') as context:
                verify_vat('CZ67985726')
        self.assertIsNone(context.exception.source)

    def test_verify_vat(self):
        with self.assertLogs(self.logger_name, level='INFO') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, self.url, body=get_wsdl_content())
                rsps.add(responses.POST, self.service_url, body=get_envelope(self.address))
                response = verify_vat('CZ67985726')
        self.assertEqual(response.countryCode, 'CZ')
        self.assertEqual(response.vatNumber, '67985726')
        self.assertEqual(response.requestDate, date(2022, 5, 20))
        self.assertEqual(response.valid, True)
        self.assertEqual(response.name, 'CZ.NIC, z.s.p.o.')
        self.assertEqual(response.address, self.address)
        self.assertEqual(logs.output, [
            'INFO:verify_vat_number.vies:https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl '
            'Country code: CZ VAT: 67985726'
        ])

    def test_verify_vat_log_debug(self):
        with self.assertLogs(self.logger_name, level='DEBUG') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, self.url, body=get_wsdl_content())
                rsps.add(responses.POST, self.service_url, body=get_envelope(self.address))
                response = verify_vat('CZ67985726')
        self.assertEqual(response.countryCode, 'CZ')
        self.assertEqual(response.vatNumber, '67985726')
        self.assertEqual(response.requestDate, date(2022, 5, 20))
        self.assertEqual(response.valid, True)
        self.assertEqual(response.name, 'CZ.NIC, z.s.p.o.')
        self.assertEqual(response.address, self.address)
        self.assertEqual(logs.output, [
            'INFO:verify_vat_number.vies:https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
            ' Country code: CZ VAT: 67985726',
            'DEBUG:verify_vat_number.vies:'
            '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/"'
            ' xmlns:ns1="urn:ec.europa.eu:taxud:vies:services:checkVat:types">\n'
            '        <ns0:Body>\n'
            '            <ns1:checkVatResponse>\n'
            '                <ns1:countryCode>CZ</ns1:countryCode>\n'
            '                <ns1:vatNumber>67985726</ns1:vatNumber>\n'
            '                <ns1:requestDate>2022-05-20+02:00</ns1:requestDate>\n'
            '                <ns1:valid>true</ns1:valid>\n'
            '                <ns1:name>CZ.NIC, z.s.p.o.</ns1:name>\n'
            '                <ns1:address>Milešovská 1136/5\nPRAHA 3 - VINOHRADY\n130 00  PRAHA 3</ns1:address>\n'
            '            </ns1:checkVatResponse>\n'
            '        </ns0:Body>\n'
            '    </ns0:Envelope>'
        ])

    def test_verify_vat_log_debug_none(self):
        with patch('verify_vat_number.vies.get_last_received_envelope', return_value=None):
            with self.assertLogs(self.logger_name, level='DEBUG') as logs:
                with responses.RequestsMock() as rsps:
                    rsps.add(responses.GET, self.url, body=get_wsdl_content())
                    rsps.add(responses.POST, self.service_url, body=get_envelope(self.address))
                    response = verify_vat('CZ67985726')
        self.assertEqual(response.countryCode, 'CZ')
        self.assertEqual(response.vatNumber, '67985726')
        self.assertEqual(response.requestDate, date(2022, 5, 20))
        self.assertEqual(response.valid, True)
        self.assertEqual(response.name, 'CZ.NIC, z.s.p.o.')
        self.assertEqual(response.address, self.address)
        self.assertEqual(logs.output, [
            'INFO:verify_vat_number.vies:https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl '
            'Country code: CZ VAT: 67985726'
        ])

    def test_verify_vat_not_found(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=get_wsdl_content())
            rsps.add(responses.POST, self.service_url, body=get_envelope_vat_is_false())
            with self.assertRaises(VatNotFound) as context:
                verify_vat('CZ67985728')
        self.assertEqual(
                context.exception.source,
                '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/"'
                """ xmlns:ns1="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
            <ns0:Body>
                <ns1:checkVatResponse>
                    <ns1:countryCode>CZ</ns1:countryCode>
                    <ns1:vatNumber>67985728</ns1:vatNumber>
                    <ns1:requestDate>2022-05-18+02:00</ns1:requestDate>
                    <ns1:valid>false</ns1:valid>
                    <ns1:name>---</ns1:name>
                    <ns1:address>---</ns1:address>
                </ns1:checkVatResponse>
            </ns0:Body>
        </ns0:Envelope>""")

    def test_get_unexpected_envelope(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=get_wsdl_content())
            rsps.add(responses.POST, self.service_url, body=get_unexpected_envelope())
            response = get_from_eu_vies('CZ67985728')
        self.assertEqual(response, VerifiedCompany(
            company_name='---',
            address='---',
            street_and_num=None,
            city=None,
            postal_code=None,
            district=None,
            country_code=None)
        )

    def test_get_last_received_envelope_none(self):
        history = HistoryPlugin()
        self.assertIsNone(get_last_received_envelope(history))

    def test_get_last_received_envelope_no_response(self):
        history = HistoryPlugin()
        history.egress(sentinel.command, None, None, None)
        self.assertIsNone(get_last_received_envelope(history))

    def test_get_last_received_envelope(self):
        history = HistoryPlugin()
        history.egress(sentinel.command, None, None, None)
        history.ingress(sentinel.response, None, None)
        self.assertEqual(get_last_received_envelope(history), sentinel.response)

    def test_get_from_eu_vies(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=get_wsdl_content())
            rsps.add(responses.POST, self.service_url, body=get_envelope(self.address))
            response = get_from_eu_vies('CZ67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Milešovská 1136/5\nPRAHA 3 - VINOHRADY\n130 00  PRAHA 3',
            street_and_num='Milešovská 1136/5',
            city='PRAHA 3',
            postal_code='130 00',
            district='PRAHA 3 - VINOHRADY',
            country_code='CZ')
        )

    def test_get_from_eu_vies_private_data(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=get_wsdl_content())
            rsps.add(responses.POST, self.service_url, body=get_envelope_private_data())
            response = get_from_eu_vies('DE306401413')
        self.assertEqual(response, VerifiedCompany(
            company_name='---',
            address='---',
            street_and_num=None,
            city=None,
            postal_code=None,
            district=None,
            country_code=None)
        )

    def test_get_from_eu_vies_el_gr(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, self.url, body=get_wsdl_content())
            rsps.add(responses.POST, self.service_url, body=get_envelope(self.address, country_code='EL'))
            response = get_from_eu_vies('EL67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Milešovská 1136/5\nPRAHA 3 - VINOHRADY\n130 00  PRAHA 3',
            street_and_num='Milešovská 1136/5',
            city='PRAHA 3',
            postal_code='130 00',
            district='PRAHA 3 - VINOHRADY',
            country_code='GR')
        )

    def test_parse_address_empty(self):
        data = parse_address('CZ', '')
        self.assertEqual(data, {})

    def test_parse_address_three_lines(self):
        data = parse_address('CZ', 'Street 42\nCity - district\n13000  City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'postal_code': '13000',
            'city': 'City'
        })

    def test_parse_address_three_lines_postal_with_space(self):
        data = parse_address('CZ', 'Street 42\nCity - district\n130 00  City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'postal_code': '130 00',
            'city': 'City'
        })

    def test_parse_address_two_lines(self):
        data = parse_address('CZ', 'Street 42\n13000  City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'postal_code': '13000',
            'city': 'City'
        })

    def test_parse_address_two_lines_prefixed_postal(self):
        data = parse_address('CZ', 'Street 42\nL-13000  City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'postal_code': 'L-13000',
            'city': 'City'
        })

    def test_parse_address_three_lines_postal_with_letters(self):
        data = parse_address('CZ', 'Street 42\nCity - district\n130MA-01  City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'postal_code': '130MA-01',
            'city': 'City'
        })

    def test_parse_address_three_lines_postal_with_divis(self):
        data = parse_address('CZ', 'Street 42\nCity - district\n130-01  City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'postal_code': '130-01',
            'city': 'City'
        })

    def test_parse_address_two_lines_postal_with_letters(self):
        data = parse_address('CZ', 'Street 42\n130MA-01  City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'postal_code': '130MA-01',
            'city': 'City'
        })

    def test_parse_address_two_lines_postal_with_divis(self):
        data = parse_address('CZ', 'Street 42\n130-01  City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'postal_code': '130-01',
            'city': 'City'
        })

    def test_parse_address_three_commas_with_postal(self):
        data = parse_address('CZ', 'Street 42,City - district,13000 City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'postal_code': '13000',
            'city': 'City'
        })

    def test_parse_address_three_commas(self):
        data = parse_address('CZ', 'Street 42,City - district,City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'city': 'City'
        })

    def test_parse_address_one_line(self):
        data = parse_address('CZ', 'Street 42 13000 City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'postal_code': '13000',
            'city': 'City'
        })

    def test_parse_address_sk_three_lines(self):
        data = parse_address('SK', 'Street 42\nCity - district\n13000  City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'postal_code': '13000',
            'city': 'City'
        })

    def test_parse_address_sk_three_lines_postal_with_space(self):
        data = parse_address('SK', 'Street 42\nCity - district\n130 00  City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'postal_code': '130 00',
            'city': 'City'
        })

    def test_parse_address_sk_three_lines_country(self):
        data = parse_address('SK', 'Street 42\nCity - district\n13000  City\nSlovensko')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'postal_code': '13000',
            'city': 'City'
        })

    def test_parse_address_sk_three_lines_postal_with_space_country(self):
        data = parse_address('SK', 'Street 42\nCity - district\n130 00  City\nSlovensko')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'postal_code': '130 00',
            'city': 'City'
        })

    def test_parse_address_bg(self):
        data = parse_address('BG', 'Street 42,City 13000')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'postal_code': '13000',
            'city': 'City'
        })

    def test_parse_address_el_divis(self):
        data = parse_address('EL', 'Street 42 13000 - City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'postal_code': '13000',
            'city': 'City'
        })

    def test_parse_address_el(self):
        data = parse_address('EL', 'Street 42 13000 City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'postal_code': '13000',
            'city': 'City'
        })

    def test_parse_address_ee(self):
        data = parse_address('EE', 'Street 42 13000 City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'postal_code': '13000',
            'city': 'City'
        })

    def test_parse_address_ie(self):
        data = parse_address('IE', 'Street 42, City')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'city': 'City',
        })

    def test_parse_address_lv_three_commas(self):
        data = parse_address('LV', 'Street 42, City, City - district, AE-45')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'district': 'City - district',
            'postal_code': 'AE-45',
            'city': 'City'
        })

    def test_parse_address_lv_two_commas(self):
        data = parse_address('LV', 'Street 42, City, AE-45')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42',
            'postal_code': 'AE-45',
            'city': 'City'
        })

    def test_parse_address_mt_five_lines(self):
        data = parse_address('MT', 'Street 42\n24/12\nOpt.\nAE-45600\nCity')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42\n24/12\nOpt.',
            'postal_code': 'AE-45600',
            'city': 'City'
        })

    def test_parse_address_mt_four_lines(self):
        data = parse_address('MT', 'Street 42\n24/12\nAE-45600\nCity')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42\n24/12',
            'postal_code': 'AE-45600',
            'city': 'City'
        })

    def test_parse_address_ro_three_lines(self):
        data = parse_address('RO', 'City\nStreet 42\n24/12')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42\n24/12',
            'city': 'City',
        })

    def test_parse_address_ro_two_lines(self):
        data = parse_address('RO', 'City\nStreet 42 - 24/12')
        self.assertDictEqual(data, {
            'street_and_num': 'Street 42 - 24/12',
            'city': 'City'
        })
