from django.conf import settings
from django.contrib import admin

from apps.core.models import Log


admin.site.site_header = settings.PROJECT_NAME
admin.site.site_title = settings.PROJECT_NAME
admin.site.enable_nav_sidebar = True


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('level_name', 'function_name', 'line_number', 'message', 'created_on', )
    search_fields = ('level_name', 'message', )
    list_filter = ('level_name', )
