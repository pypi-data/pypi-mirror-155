================
Django Banks
================

A Django application that provides Indonesian bank choices for use with forms
and a country field for models.

.. contents::
    :local:
    :backlinks: none


Installation
============

1. Run ``pip install p1-bank``
2. Add ``'bank'`` to ``INSTALLED_APPS`` in settings.py
3. Run `python manage.py migrate` to create banks models

Bank Model
===========

A model of bank that holds all banks in Indonesia.

Supports long name, short name, bank code, and branch code.

.. code:: python

    >>> from django.apps import apps
    >>> Bank = apps.get_model('bank', 'Bank')
    >>> bank = Bank.objects.get(short_name='BANK BCA')
    >>> bank.long_name
    u'PT. BANK CENTRAL ASIA TBK.'
    >>> bank.short_name
    u'BANK BCA'
    >>> bank.bank_code
    u'014'
    >>> bank.branch_code
    u'0397'
    >>> bank.bi_code
    u'0140397'

It is possible to get a bank object from bi code:

.. code:: python

    >>> Bank.objects.get_by_bi_code('0140397')
    <Bank: BANK BCA>

or upsert (update or create) from list with header:

.. code:: python

    >>> Bank.objects.get(bank_code='200')
    <Bank: BANK BTN>
    >>> bank_list = [
            ['bank_code', 'short_name'],
            ['200', 'BTN']
        ]
    >>> Bank.objects.upsert_from_list_with_header(bank_list)
    >>> Bank.objects.get(bank_code='200')
    <Bank: BTN>

Bank Field
===========

``BankField`` is based on Django's ``ForeignKey``, a relationship
to Bank model.

Consider an ``Account`` model using a ``BankField``:

.. code:: python

    from django.db import models
    from p1_bank.fields import BankField

    class Account(models.Model):
        name = models.CharField(max_length=100)
        bank = BankField(related_name='accounts')

Any ``Account`` instance will have a ``bank`` attribute that you can use to
identify account's bank:

.. code:: python

    >>> bank = Bank.objects.get(short_name='BANK BCA')
    >>> account = Account.objects.create(name='Kania', bank=bank)
    >>> account.bank
    'BANK BCA'
    >>> account.bank.code
    '014'

Bank Factories
==============

You may use bank factories to support your test (requires ``factory_boy``)

.. code:: python

    >>> from bank.factories import BankFactory
    >>> BankFactory()
    <Bank: Bank X00>
    >>> BankFactory()
    <Bank: Bank X01>
    >>> bank301 = BankFactory(bank_code='301')
    >>> bank301.bank_code
    '301'
