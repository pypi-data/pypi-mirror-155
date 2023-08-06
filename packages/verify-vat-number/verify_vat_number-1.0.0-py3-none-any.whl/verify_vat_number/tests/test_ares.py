import xml.etree.ElementTree as ET
from unittest import TestCase

import responses
from requests.exceptions import RequestException, Timeout

from verify_vat_number.ares import (NS, SERVICE_URL, check_error_code, get_from_cz_ares, get_text, get_xml_content,
                                    get_xml_doc)
from verify_vat_number.data import VerifiedCompany
from verify_vat_number.exceptions import (InvalidVatNumber, ServiceTemporarilyUnavailable, UnexpectedResponseFormat,
                                          VatNotFound, VerifyVatException)

RESPONSE_67985726 = """<?xml version="1.0" encoding="UTF-8"?>
<are:Ares_odpovedi
    xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
    xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4"
    xmlns:udt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/uvis_datatypes/v_1.0.1"
    odpoved_datum_cas="2022-06-08T10:08:16"
    odpoved_pocet="1"
    odpoved_typ="Standard"
    vystup_format="XML"
    xslt="klient"
    validation_XSLT="/ares/xml_doc/schemas/ares/ares_answer/v_1.0.0/ares_answer.xsl"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1
        http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1/ares_answer_v_1.0.1.xsd"
    Id="ares">
    <are:Odpoved>
        <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
        <are:Typ_vyhledani>FREE</are:Typ_vyhledani>
        <are:Zaznam>
            <are:Shoda_ICO>
                <dtt:Kod>9</dtt:Kod>
            </are:Shoda_ICO>
            <are:Vyhledano_dle>ICO</are:Vyhledano_dle>
            <are:Typ_registru>
                <dtt:Kod>2</dtt:Kod>
                <dtt:Text>OR</dtt:Text>
            </are:Typ_registru>
            <are:Datum_vzniku>1998-05-27</are:Datum_vzniku>
            <are:Datum_platnosti>2022-06-08</are:Datum_platnosti>
            <are:Pravni_forma>
                <dtt:Kod_PF>751</dtt:Kod_PF>
            </are:Pravni_forma>
            <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
            <are:ICO>67985726</are:ICO>
            <are:Identifikace>
                <are:Adresa_ARES>
                    <dtt:ID_adresy>212121734</dtt:ID_adresy>
                    <dtt:Kod_statu>203</dtt:Kod_statu>
                    <dtt:Nazev_okresu>Hlavní město Praha</dtt:Nazev_okresu>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:Nazev_mestske_casti>Praha 3</dtt:Nazev_mestske_casti>
                    <dtt:Nazev_ulice>Milešovská</dtt:Nazev_ulice>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Typ_cislo_domovni>1</dtt:Typ_cislo_domovni>
                    <dtt:Cislo_orientacni>5</dtt:Cislo_orientacni>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Adresa_UIR>
                        <udt:Kod_oblasti>19</udt:Kod_oblasti>
                        <udt:Kod_kraje>19</udt:Kod_kraje>
                        <udt:Kod_okresu>3100</udt:Kod_okresu>
                        <udt:Kod_obce>554782</udt:Kod_obce>
                        <udt:Kod_pobvod>35</udt:Kod_pobvod>
                        <udt:Kod_nobvod>35</udt:Kod_nobvod>
                        <udt:Kod_casti_obce>490229</udt:Kod_casti_obce>
                        <udt:Kod_mestske_casti>500097</udt:Kod_mestske_casti>
                        <udt:PSC>13000</udt:PSC>
                        <udt:Kod_ulice>456276</udt:Kod_ulice>
                        <udt:Cislo_domovni>1136</udt:Cislo_domovni>
                        <udt:Typ_cislo_domovni>1</udt:Typ_cislo_domovni>
                        <udt:Cislo_orientacni>5</udt:Cislo_orientacni>
                        <udt:Kod_adresy>21760837</udt:Kod_adresy>
                        <udt:Kod_objektu>21719365</udt:Kod_objektu>
                    </dtt:Adresa_UIR>
                </are:Adresa_ARES>
            </are:Identifikace>
            <are:Kod_FU>3</are:Kod_FU>
            <are:Priznaky_subjektu>NAAANANNNNANNNNNNNNNPNNNANNNNN</are:Priznaky_subjektu>
        </are:Zaznam>
    </are:Odpoved>
</are:Ares_odpovedi>
"""


class TestAres(TestCase):

    logger_name = 'verify_vat_number.ares'
    logging_info = 'INFO:verify_vat_number.ares:https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi?ico=67985726'

    def test_get_xml_content_request_exception(self):
        with self.assertLogs(self.logger_name, level='INFO') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=RequestException())
                with self.assertRaises(VerifyVatException) as context:
                    get_xml_content('67985726')
        self.assertEqual(context.exception.source, '')
        self.assertEqual(logs.output, [self.logging_info])

    def test_get_xml_content_timeout(self):
        with self.assertLogs(self.logger_name, level='INFO') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=Timeout())
                with self.assertRaises(ServiceTemporarilyUnavailable) as context:
                    get_xml_content('67985726')
        self.assertIsNone(context.exception.source)
        self.assertEqual(logs.output, [self.logging_info])

    def test_get_xml_content_response_is_not_ok(self):
        with self.assertLogs(self.logger_name, level='INFO') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', status=404, body="Page not found.")
                with self.assertRaises(VerifyVatException) as context:
                    get_xml_content('67985726')
        self.assertEqual(context.exception.source, 'Page not found.')
        self.assertEqual(logs.output, [self.logging_info])

    def test_get_xml_content(self):
        with self.assertLogs(self.logger_name, level='DEBUG') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=RESPONSE_67985726.encode('utf8'))
                content = get_xml_content('67985726')
        self.assertEqual(content.decode('utf8'), RESPONSE_67985726)
        self.assertEqual(logs.output, [self.logging_info, f'DEBUG:verify_vat_number.ares:{RESPONSE_67985726}'])

    def test_get_xml_content_param_url(self):
        with self.assertLogs(self.logger_name, level='INFO') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=RESPONSE_67985726.encode('utf8'))
                content = get_xml_content('67985726', SERVICE_URL)
        self.assertEqual(content.decode('utf8'), RESPONSE_67985726)
        self.assertEqual(logs.output, [self.logging_info])

    def test_get_xml_doc_invalid_xml(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body="<foo")
            with self.assertRaises(VerifyVatException) as context:
                get_xml_doc('67985726')
        self.assertEqual(context.exception.source, '<foo')

    def test_get_xml_doc(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=RESPONSE_67985726.encode('utf8'))
            root, source = get_xml_doc('67985726')
        self.assertIsInstance(root, ET.Element)
        self.assertEqual(source.decode('utf8'), RESPONSE_67985726)

    def test_check_error_code_no_error(self):
        content = b"""<?xml version="1.0" encoding="UTF-8"?><Error></Error>"""
        root = ET.fromstring(content)
        check_error_code(root, NS, content)
        self.assertIsInstance(root, ET.Element)

    def test_check_error_code_only_number(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Error
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4"
                >
                <dtt:Error_kod>7</dtt:Error_kod>
            </are:Error>"""
        root = ET.fromstring(content)
        with self.assertRaisesRegex(ServiceTemporarilyUnavailable, 'Error code: 7') as context:
            check_error_code(root, NS, content.encode('utf-8'))
        self.assertEqual(context.exception.source, content)

    def test_check_error_code_number_and_message(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Error
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4"
                >
                <dtt:Error_kod>7</dtt:Error_kod>
                <dtt:Error_text>chyba logických vazeb</dtt:Error_text>
            </are:Error>"""
        root = ET.fromstring(content)
        with self.assertRaisesRegex(ServiceTemporarilyUnavailable, 'Error code: 7; chyba logických vazeb') as context:
            check_error_code(root, NS, content.encode('utf-8'))
        self.assertEqual(context.exception.source, content)

    def test_get_text_unexpected_format(self):
        content = """<?xml version="1.0" encoding="UTF-8"?><Error></Error>"""
        root = ET.fromstring(content)
        with self.assertRaisesRegex(UnexpectedResponseFormat, 'dtt:foo') as context:
            get_text('dtt:foo', root, NS, content.encode('utf-8'))
        self.assertEqual(context.exception.source, content)

    def test_get_text(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <Error xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <dtt:foo>Hello world!</dtt:foo>
            </Error>"""
        root = ET.fromstring(content)
        text = get_text('dtt:foo', root, NS, content.encode('utf-8'))
        self.assertEqual(text, 'Hello world!')

    def test_get_from_cz_ares(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=RESPONSE_67985726.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Milešovská 1136/5\n13000 Praha 3',
            street_and_num='Milešovská 1136/5',
            city='Praha 3',
            postal_code='13000',
            district='Praha 3 - Vinohrady',
            country_code='CZ'
        ))

    def test_get_from_cz_ares_custom_namespace(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=RESPONSE_67985726.encode('utf8'))
            response = get_from_cz_ares('67985726', ns=NS)
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Milešovská 1136/5\n13000 Praha 3',
            street_and_num='Milešovská 1136/5',
            city='Praha 3',
            postal_code='13000',
            district='Praha 3 - Vinohrady',
            country_code='CZ'
        ))

    def test_get_from_cz_ares_empty_number(self):
        with self.assertRaisesRegex(InvalidVatNumber, 'Invalid number format.'):
            get_from_cz_ares('!')

    def test_get_from_cz_ares_too_long_number(self):
        with self.assertRaisesRegex(InvalidVatNumber, 'The number cannot be more than 8 digits long.'):
            get_from_cz_ares('123456789')

    def test_get_from_cz_ares_error_code(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Error
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4"
                >
                <dtt:Error_kod>7</dtt:Error_kod>
                <dtt:Error_text>chyba logických vazeb</dtt:Error_text>
            </are:Error>"""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            with self.assertRaises(ServiceTemporarilyUnavailable) as context:
                get_from_cz_ares('67985726')
        self.assertEqual(context.exception.source, content)

    def test_get_from_cz_ares_pocet_zaznamu_missing(self):
        content = """<foo></foo>"""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            with self.assertRaisesRegex(UnexpectedResponseFormat, './/are:Pocet_zaznamu') as context:
                get_from_cz_ares('67985726')
        self.assertEqual(context.exception.source, content)

    def test_get_from_cz_ares_pocet_zaznamu_is_not_one(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1">
                <are:Pocet_zaznamu>0</are:Pocet_zaznamu>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            with self.assertRaises(VatNotFound) as context:
                get_from_cz_ares('67985726')
        self.assertEqual(context.exception.source, content)

    def test_get_from_cz_ares_adresa_ared_missing(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            with self.assertRaisesRegex(UnexpectedResponseFormat, './/are:Adresa_ARES') as context:
                get_from_cz_ares('67985726')
        self.assertEqual(context.exception.source, content)

    def test_get_from_cz_ares_nazev_mestske_casti(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_mestske_casti>Praha 3</dtt:Nazev_mestske_casti>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Nazev_ulice>Milešovská</dtt:Nazev_ulice>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Kod_statu>203</dtt:Kod_statu>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Milešovská 1136\n13000 Praha 3',
            street_and_num='Milešovská 1136',
            city='Praha 3',
            postal_code='13000',
            district='Praha 3 - Vinohrady',
            country_code='CZ'
        ))

    def test_get_from_cz_ares_nazev_obce(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Nazev_ulice>Milešovská</dtt:Nazev_ulice>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Kod_statu>203</dtt:Kod_statu>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Milešovská 1136\n13000 Praha',
            street_and_num='Milešovská 1136',
            city='Praha',
            postal_code='13000',
            district='Praha - Vinohrady',
            country_code='CZ'
        ))

    def test_get_from_cz_ares_psc(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            with self.assertRaisesRegex(UnexpectedResponseFormat, 'dtt:PSC') as context:
                get_from_cz_ares('67985726')
        self.assertEqual(context.exception.source, content)

    def test_get_from_cz_ares_nazev_ulice(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Kod_statu>203</dtt:Kod_statu>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Praha 1136\n13000 Praha',
            street_and_num='Praha 1136',
            city='Praha',
            postal_code='13000',
            district='Praha - Vinohrady',
            country_code='CZ'
        ))

    def test_get_from_cz_ares_cislo_orientacni(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Cislo_orientacni>5</dtt:Cislo_orientacni>
                    <dtt:Kod_statu>203</dtt:Kod_statu>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Praha 1136/5\n13000 Praha',
            street_and_num='Praha 1136/5',
            city='Praha',
            postal_code='13000',
            district='Praha - Vinohrady',
            country_code='CZ'
        ))

    def test_get_from_cz_ares_unknown_country(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Kod_statu>0</dtt:Kod_statu>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Praha 1136\n13000 Praha',
            street_and_num='Praha 1136',
            city='Praha',
            postal_code='13000',
            district='Praha - Vinohrady',
            country_code='CZ'
        ))
