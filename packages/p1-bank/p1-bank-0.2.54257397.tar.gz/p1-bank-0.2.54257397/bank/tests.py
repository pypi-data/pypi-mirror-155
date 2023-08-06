from builtins import str
from django.test import TestCase
from .models import Bank


class BankModelTestCase(TestCase):

    def setUp(self):
        self.bank_1, _ = Bank.objects.update_or_create(
            bank_code='008', branch_code='0017',
            defaults={
                'short_name': 'Mandiri',
                'long_name': 'PT. Bank Mandiri (Persero) Tbk.'})
        self.bank_2, _ = Bank.objects.update_or_create(
            bank_code='x14',
            defaults={
                'short_name': 'BCA',
                'long_name': 'PT. Bank Central Asia, Tbk.'})

    def test_bi_code(self):
        self.assertEqual(self.bank_1.bi_code, '0080017')
        self.assertEqual(self.bank_2.bi_code, 'x14')

    def test_unicode(self):
        self.assertEqual(str(self.bank_1), 'Mandiri')


class BankManagerTestCase(TestCase):

    def setUp(self):
        self.bank_1, _ = Bank.objects.update_or_create(
            bank_code='008', branch_code='0017',
            defaults={
                'short_name': 'Mandiri',
                'long_name': 'PT. Bank Mandiri (Persero) Tbk.'})
        self.bank_2, _ = Bank.objects.update_or_create(
            bank_code='x14',
            defaults={
                'short_name': 'BCA',
                'long_name': 'PT. Bank Central Asia, Tbk.'})
        self.bank_3, _ = Bank.objects.update_or_create(
            bank_code='001', branch_code='0000',
            defaults={
                'short_name': 'BI',
                'long_name': 'Bank Indonesia KP Jakarta'})
        self.bank_4, _ = Bank.objects.update_or_create(
            bank_code='001', branch_code='0906',
            defaults={
                'short_name': 'BI Semarang',
                'long_name': 'Bank Indonesia Cabang Semarang'})

    def test_get_by_bi_code(self):
        banks = Bank.objects.get_by_bi_code('0080017')
        self.assertEqual(banks, self.bank_1)

    def test_upsert_from_list_with_header(self):
        bank_list = [
            ['bank_code', 'short_name'],
            ['x14', 'BNI'],
            ['427', 'BNI Syariah'],
            ['001', ''],
        ]
        Bank.objects.upsert_from_list_with_header(bank_list)

        banks_x14 = Bank.objects.filter(bank_code='x14')
        banks_001 = Bank.objects.filter(bank_code='001')
        self.assertEqual(len(banks_x14), 1)
        self.assertEqual(len(banks_001), 2)
        self.assertEqual(banks_x14[0].short_name, 'BNI')
        self.assertEqual(banks_001[0].short_name, '')
        self.assertEqual(banks_001[1].short_name, '')
