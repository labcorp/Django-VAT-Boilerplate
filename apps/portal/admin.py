from django.contrib import admin

from apps.portal.models.config import Config
from apps.content.models.schedule import SCHEDULABLE_CONTENT_FIELDSETS
from apps.content.models.seo import SEO_FIELDSETS


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('site', 'gtm_id', )
    search_fields = ('site',)
    list_filter = ('site', )
    fieldsets = (
        (None, {
            'fields': ('site', 'gtm_id', )
        }),
        SEO_FIELDSETS,
        SCHEDULABLE_CONTENT_FIELDSETS
    )
