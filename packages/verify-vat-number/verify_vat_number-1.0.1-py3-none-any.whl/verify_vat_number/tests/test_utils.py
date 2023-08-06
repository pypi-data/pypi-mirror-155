from unittest import TestCase

from verify_vat_number.utils import strip_vat_id_number, strip_vat_reg_number


class TestUtils(TestCase):

    ascii = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\t\r\n'

    def test_strip_vat_id_number(self):
        self.assertEqual(strip_vat_id_number(self.ascii), '0123456789')

    def test_strip_vat_reg_number(self):
        code = strip_vat_reg_number(self.ascii)
        self.assertEqual(code, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
