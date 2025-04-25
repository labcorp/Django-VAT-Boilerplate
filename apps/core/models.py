import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(_('Created on'), auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(_('Updated_on'), auto_now=True, editable=False)
    active = models.BooleanField(_('active'), default=True)

    class Meta:
        abstract = True


class Log(AbstractBaseModel):
    class Meta:
        ordering = ('-created_on', )

    filename = models.CharField(_('filename'), blank=True, max_length=128)
    function_name = models.CharField(_('function name'), blank=True, max_length=128)
    level_name = models.CharField(_('level name'), blank=True, max_length=32)
    level_number = models.PositiveSmallIntegerField(_('level number'), default=0)
    line_number = models.PositiveSmallIntegerField(_('line number'), default=0)
    message = models.TextField(_('message'), null=True, blank=True)
    module = models.CharField(_('module'), null=True, blank=True, max_length=128)
    path = models.CharField(_('path'), blank=True, max_length=255)
    stack_info = models.TextField(_('stack'), null=True, blank=True)
    args = models.TextField(_('args'), blank=True)
