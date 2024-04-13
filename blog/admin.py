from django.contrib import admin
from blog.models import *


# Register your models here.
# admin.site.unregister(Post)

class PostAdmin(admin.ModelAdmin):
    """
    https://django-tinymce.readthedocs.io/en/latest/usage.html
    """
    model = Post
    ordering = ('-publish_date',)
    filter_horizontal = ('tags',)
    list_display = [
        'title',
        'subtitle',
        'slug',
        'body',
        'meta_description',
        'date_created',
        'date_modified',
        'publish_date',
        'published',
        'author',
        # 'tags',

    ]
    readonly_fields = [
        'date_created',
        'date_modified',
    ]
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = [
        ('Title', {'fields': [
            ('title',),
            ('subtitle',),
        ]}),
        ('Content', {'fields': [
            ('body',)
        ]}),
        ('Meta', {'fields': [
            ('meta_description',),
            ('published',),
            ('publish_date',),
        ]}),
        ('Details', {'fields': [
            ('author',),
            ('tags',),
            ('slug',),
            ('date_created',),
            ('date_modified',),
        ]})

    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
