from django.db import models

import sys
if sys.version_info[0] < 3:
    from django.utils.translation import ugettext_lazy as _
else:
    from django.utils.translation import gettext_lazy as _


class BankField(models.ForeignKey):

    def __init__(self, **kwargs):

        kwargs['to'] = 'bank.Bank'
        kwargs['on_delete'] = models.PROTECT
        kwargs.setdefault('verbose_name', _('Bank'))
        kwargs.setdefault('related_name', 'bank_set')

        super(BankField, self).__init__(**kwargs)
