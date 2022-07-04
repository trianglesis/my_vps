from django.db import models
from django.utils.translation import gettext_lazy as _


class Options(models.Model):
    option_key = models.CharField(_('option key unique'), max_length=120, unique=True)
    option_value = models.TextField(_('option value'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    private = models.BooleanField(_('private value'), null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'remotes_options'

    def __str__(self):
        if self.private:
            t = f'PRIVATE: {self.id} - {self.option_key}'
        else:
            t = f'{self.id} - {self.option_key}'
        return t

