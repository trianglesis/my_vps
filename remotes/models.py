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


class PerlButtons(models.Model):
    dom = models.CharField(max_length=50)
    gate = models.CharField(max_length=50)
    mode = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = [['dom', 'gate', 'mode']]

    def __str__(self):
        # t = f'{self.id} - {self.dom}:{self.gate}:{self.mode}'
        t = f'{self.id} - {self.description}'
        return t


class PerlCameras(models.Model):
    dvr = models.SmallIntegerField()
    cam = models.SmallIntegerField()
    type = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    button = models.ForeignKey(PerlButtons, models.CASCADE,
                               blank=True, null=True)

    class Meta:
        unique_together = [['dvr', 'cam']]

    def __str__(self):
        t = f'{self.id} - {self.dvr}:{self.cam}:{self.type}'
        return t
