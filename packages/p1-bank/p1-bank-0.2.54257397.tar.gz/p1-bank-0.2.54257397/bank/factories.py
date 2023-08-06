from builtins import object
import factory


class BankFactory(factory.DjangoModelFactory):
    short_name = factory.Sequence(lambda n: 'BANK X%02d' % n)
    long_name = factory.Sequence(lambda n: 'PT BANK X%02d' % n)
    bank_code = factory.Sequence(lambda n: 'X%02d' % n)
    branch_code = factory.Sequence(lambda n: 'X%03d' % n)

    class Meta(object):
        model = 'bank.Bank'
