from __future__ import unicode_literals

from django.db import models
from .managers import BankManager

import sys
if sys.version_info[0] < 3:
    from django.utils.translation import ugettext_lazy as _
else:
    from django.utils.translation import gettext_lazy as _


class Bank(models.Model):
    """
    Model of Indonesian Bank
    bank_code  : three digit identifying a bank
    branch_code: four-digit code identifying a branch
    short_name : commonly used name
    long_name  : corporation name
    """
    bank_code = models.CharField(_('Bank Code'), max_length=5)
    branch_code = models.CharField(_('Branch Code'), max_length=5, null=True)
    short_name = models.CharField(_('Short Name'), max_length=50, null=True)
    long_name = models.CharField(_('Long Name'), max_length=128, null=True)

    objects = BankManager()

    @property
    def bi_code(self):
        bank_code = self.bank_code
        branch_code = ''

        if self.branch_code is not None:
            branch_code = self.branch_code

        return '%s%s' % (bank_code, branch_code)

    def __str__(self):
        return self.short_name
