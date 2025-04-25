from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField


SEO_FIELDSETS = (
    _('SEO options'), {
        'classes': ('collapse',),
        'fields': ('title', 'description', 'image', ),
    }
)


class AbstractSEOModel(models.Model):
    title = models.CharField(_('title'), max_length=128, blank=True)
    description = models.CharField(_('description'), max_length=255, blank=True)
    image = FilerImageField(null=True, blank=True, related_name='seo_image', help_text=_('Default: 1200x630px. Will be resized'), on_delete=models.SET_NULL)

    class Meta:
        abstract = True
