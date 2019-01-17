from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Activity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT, related_name='activities')
    activity = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.CharField(max_length=255, db_index=True)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = _('activities')

    def __str__(self):
        return _('%(activity)s@%(project)s') % {
            'activity': self.activity,
            'project': self.project,
        }

    def clean(self):
        if self.end_datetime and self.start_datetime \
                and self.end_datetime <= self.start_datetime:
            raise ValidationError({
                'end_datetime':
                [_('End datetime must be greater than the start datetime.')]
            })

    @property
    def duration(self):
        end_datetime = self.end_datetime or timezone.now()
        return end_datetime - self.start_datetime
