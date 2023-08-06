from django.db import models
from django.db import transaction


class BankManager(models.Manager):

    def get_by_bi_code(self, bi_code):
        """
        bi code is concatenation of bank code and branch code.
        bi code should have length of 7.
        """

        if len(bi_code) != 7:
            raise Exception('bi code should have length of 7')

        bank_code = bi_code[:3]
        branch_code = bi_code[3:]

        return super(BankManager, self).get(
            bank_code=bank_code,
            branch_code=branch_code)

    def upsert_from_list_with_header(self, bank_list):
        """
        upsert from list of list.

        first bank_list list is name of field. bank_code is required.

        Example:
            [
                ['bank_code', 'short_name'],
                ['200', 'BTN'],
            ]
        """

        if len(bank_list) == 0:
            raise Exception('Empty list')
        elif 'bank_code' not in bank_list[0]:
            raise Exception('bank_code field is required')

        with transaction.atomic():
            for row in bank_list[1:]:

                bank = dict()
                for index, item in enumerate(row):
                    bank[bank_list[0][index]] = item

                if 'branch_code' in bank_list[0]:
                    super(BankManager, self).update_or_create(
                        bank_code=bank.get('bank_code'),
                        branch_code=bank.get('branch_code', None),
                        defaults=bank)
                else:
                    super(BankManager, self) \
                        .filter(bank_code=bank.get('bank_code')) \
                        .update(**bank)
