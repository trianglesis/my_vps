from django.db import models
from django.utils.translation import gettext_lazy as _


class Options(models.Model):
    option_key = models.CharField(max_length=120, unique=True)
    option_value = models.TextField(blank=True, null=True)
    option_bool = models.BooleanField(default=False)
    private = models.BooleanField(default=True)

    comments = models.TextField(blank=True, null=True)  # Explanation

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'main_options'
        ordering = ['updated_at']

    def __str__(self):
        return f'{self.id} - {self.option_key}'


class MailsTexts(models.Model):
    mail_key = models.CharField(_('key unique'), max_length=120, unique=True)
    subject = models.CharField(_('subject'), max_length=255, unique=True)
    body = models.TextField(_('body'), blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'visitors_agents'
        ordering = ['updated_at']
        unique_together = (('ip', 'hashed_ip_agent_path'),)


class NetworkVisitorsAddressesAgentProxy(NetworkVisitorsAddresses):
    class Meta:
        proxy = True
        verbose_name = '[ Visitors ] User agent'
        verbose_name_plural = '[ Visitors ] User agents'



class NetworkVisitorsAddressesUrlPathProxy(NetworkVisitorsAddresses):
    class Meta:
        proxy = True
        verbose_name = '[ Visitors ] Request path'
        verbose_name_plural = '[ Visitors ] Request path'