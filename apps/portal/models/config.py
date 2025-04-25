from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _


from apps.core.models import AbstractBaseModel
from apps.content.models.seo import AbstractSEOModel
from apps.content.models.schedule import AbstractSchedulableContent


class Config(AbstractBaseModel, AbstractSchedulableContent, AbstractSEOModel):
    site = models.OneToOneField(Site, related_name='config', on_delete=models.CASCADE)
    gtm_id = models.CharField(_('GTM ID'), blank=True, null=True, help_text=_('Something like GTM-XXXXXXX'))
