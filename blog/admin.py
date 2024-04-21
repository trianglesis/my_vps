from django.contrib import admin
from django.forms import TextInput
from django.contrib.sites.shortcuts import get_current_site

from blog.models import *


# Register your models here.
# admin.site.unregister(Post)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = (
        'name',
        'description',
    )
    # Later add selection fort all posts with such a tag


class PostAdmin(admin.ModelAdmin):
    """
    https://django-tinymce.readthedocs.io/en/latest/usage.html
    """
    model = Post
    search_fields = ['title', 'body']
    ordering = ('-publish_date',)
    filter_horizontal = ('tags',)
    list_display = [
        'title',
        'published',
        'subtitle',
        'slug',
        # 'body',
        'meta_description',
        'date_created',
        'date_modified',
        'publish_date',
        'author',
        'site',
        # 'tags',

    ]
    list_filter = [
        'publish_date',
        'date_created',
        'date_modified',
        'published',
        'tags__name',
    ]
    readonly_fields = [
        'date_created',
        'date_modified',
    ]
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = [
        (None, {'fields': [
            ('title',),
            ('subtitle',),
            ('body',),
            ('meta_description',),
        ]}),
        ('Published', {'fields': [
            ('author',),
            ('tags',),
            ('publish_date',),
            ('published',),
        ]}),
        ('Details', {'fields': [
            ('site',),
            ('slug',),
            ('date_created',),
            ('date_modified',),
        ]})

    ]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '160'})},
        # models.TextField: {'widget': Textarea(attrs={'rows': 12, 'cols': 50})},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        https://stackoverflow.com/a/5633217/4915733
        :param db_field:
        :param request:
        :param kwargs:
        :return:
        """
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
        if db_field.name == 'site':
            kwargs['initial'] = get_current_site(request)
        return super(PostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
