# pylint: disable=R0903, E1101
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


SCHEDULABLE_CONTENT_FIELDSETS = (
    _('Schedule options'), {
        'classes': ('collapse',),
        'fields': ('active', 'date_in', 'date_out', ),
    }
)


class PublishedManager(models.Manager):
    def published(self):
        qs = self.filter(active=True)
        qs = qs.filter(Q(date_in__lte=timezone.now()) | Q(date_in__isnull=True))
        qs = qs.filter(Q(date_out__gte=timezone.now()) | Q(date_out__isnull=True))
        return qs


class AbstractSchedulableContent(models.Model):
    class Meta:
        abstract = True

    objects = PublishedManager()

    date_in = models.DateTimeField(_('date in'), blank=True, null=True)
    date_out = models.DateTimeField(_('date out'), blank=True, null=True)

    def is_published(self):
        published = True

        if self.date_in and self.date_in > timezone.now():
            published = False
        if self.date_out and self.date_out < timezone.now():
            published = False

        # All schedulabe content must inherit from AbstractBaseModel
        return published if self.active else False # type: ignore
