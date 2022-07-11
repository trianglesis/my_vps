from django.db import models
from django.utils.translation import gettext_lazy as _


class MailsTexts(models.Model):
    mail_key = models.CharField(_('key unique'), max_length=120, unique=True)
    subject = models.CharField(_('subject'), max_length=255, unique=True)
    body = models.TextField(_('body'), blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now=True)
    private = models.BooleanField(_('private value'), null=True)

    class Meta:
        managed = True
        db_table = 'core_mail_texts'

    def __str__(self):
        return f'{self.id} - {self.mail_key}'


class NetworkVisitorsAddresses(models.Model):
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    is_routable = models.BooleanField(null=True)
    user_agent = models.TextField(null=True, blank=True)
    url_path = models.TextField(null=True, blank=True)

    request_get_args = models.TextField(null=True, blank=True)
    request_post_args = models.TextField(null=True, blank=True)

    hashed_ip_agent_path = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'visitors_agents'
        ordering = ['updated_at']
        unique_together = (('ip', 'hashed_ip_agent_path'),)
