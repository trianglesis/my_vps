from django.contrib import admin
# from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from core.models import *

# Register your models here.
# admin.site.unregister(User)

# DEBUG:
# admin.site.register(User)
admin.site.register(AuthGroup)
admin.site.register(AuthGroupPermissions)
admin.site.register(AuthPermission)
admin.site.register(AuthUser)
admin.site.register(AuthUserGroups)
admin.site.register(AuthUserUserPermissions)
admin.site.register(DjangoAdminLog)
admin.site.register(DjangoContentType)
admin.site.register(DjangoMigrations)
admin.site.register(DjangoSession)

admin.site.register(CeleryTaskmeta)
admin.site.register(CeleryTasksetmeta)

# admin.site.register(Site)