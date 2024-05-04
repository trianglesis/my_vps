from hashlib import blake2b

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.security import Other


def hashify(item_col, digest_size=8):
    h = blake2b(digest_size=digest_size)
    if item_col is None:
        h.update('nothing'.encode('utf-8'))
    # Hash as a simple string, same as it will be stored in table
    elif isinstance(item_col, dict):
        h.update(str(item_col).encode('utf-8'))
    else:
        h.update(item_col.encode('utf-8'))
    return h.hexdigest()


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


class StatusCodeVisitors(models.Model):
    code = models.CharField(max_length=4, unique=True)

    class Meta:
        managed = True
        db_table = 'visitors_code'
        ordering = ['code']
        verbose_name = '[ Visit ] HTTP Code'
        verbose_name_plural = '[ Visit ] HTTP Codes'


class URLPathsVisitors(models.Model):
    hash = models.CharField(max_length=16, unique=True)
    url_path = models.TextField()
    # Status codes to sort out bad requests
    code = models.ForeignKey(StatusCodeVisitors, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'visitors_url_path'
        ordering = ['created_at']
        verbose_name = '[ Visit ] URL Path'
        verbose_name_plural = '[ Visit ] URL Paths'

    def save(self, *args, **kwargs):
        self.hash = hashify(self.url_path)
        return super(URLPathsVisitors, self).save(*args, **kwargs)


class UserAgentVisitors(models.Model):
    hash = models.CharField(max_length=16, unique=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'visitors_user_agent'
        ordering = ['created_at']
        verbose_name = '[ Visit ] User Agent'
        verbose_name_plural = '[ Visit ] User Agents'

    def save(self, *args, **kwargs):
        self.hash = hashify(self.user_agent)
        return super(UserAgentVisitors, self).save(*args, **kwargs)


class RequestGetVisitors(models.Model):
    hash = models.CharField(max_length=16, unique=True)
    request_get_args = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'visitors_request_get'
        ordering = ['created_at']
        verbose_name = '[ Visit ] Request GET'
        verbose_name_plural = '[ Visit ] Request GETs'

    def save(self, *args, **kwargs):
        self.hash = hashify(self.request_get_args)
        return super(RequestGetVisitors, self).save(*args, **kwargs)


class RequestPostVisitors(models.Model):
    hash = models.CharField(max_length=16, unique=True)
    request_post_args = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'visitors_request_post'
        ordering = ['created_at']
        verbose_name = '[ Visit ] Request POST'
        verbose_name_plural = '[ Visit ] Request POSTs'

    def save(self, *args, **kwargs):
        self.hash = hashify(self.request_post_args)
        return super(RequestPostVisitors, self).save(*args, **kwargs)


class NetworkVisitorsAddresses(models.Model):
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    is_routable = models.BooleanField(null=True, verbose_name='Rout')
    hashed_ip_agent_path = models.CharField(max_length=255)

    rel_url_path = models.ForeignKey(URLPathsVisitors,
                                     blank=True,
                                     null=True,
                                     related_name='visitor_rel_url_path',
                                     on_delete=models.CASCADE)
    rel_user_agent = models.ForeignKey(UserAgentVisitors,
                                       blank=True,
                                       null=True,
                                       related_name='visitor_rel_user_agent',
                                       on_delete=models.CASCADE)
    rel_request_get = models.ForeignKey(RequestGetVisitors,
                                        blank=True,
                                        null=True,
                                        related_name='visitor_rel_request_get',
                                        on_delete=models.CASCADE)
    rel_request_post = models.ForeignKey(RequestPostVisitors,
                                         blank=True,
                                         null=True,
                                         related_name='visitor_rel_request_post',
                                         on_delete=models.CASCADE)

    # Some extra META data
    http_host = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'visitors_agents'
        ordering = ['updated_at']
        unique_together = (('ip', 'hashed_ip_agent_path'),)
        verbose_name = '[ Visit ] Network Address'
        verbose_name_plural = '[ Visit ] Network Addresses'

    def __str__(self):
        return f'Visitor id:{self.pk} {self.ip}'

    def masked_ip(self):
        secret = Other.SECRET_FOR_VISITORS_IP
        return hashify(f"{secret}{self.ip}", digest_size=12)
