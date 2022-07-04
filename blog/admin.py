from django.contrib import admin
from blog.models import *

# Register your models here.
# admin.site.unregister(Post)

admin.site.register(Post)
admin.site.register(Tag)
