from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Activity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.PROTECT,
        related_name='activities',
        verbose_name=_('user'))
    activity = models.CharField(max_length=255, verbose_name=_('activity'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    project = models.CharField(
        max_length=255, db_index=True, verbose_name=_('project'))
    start_datetime = models.DateTimeField(
        default=timezone.now, verbose_name=_('start time'))
    end_datetime = models.DateTimeField(
        blank=True, null=True, verbose_name=_('end time'))

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ['-start_datetime']

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

    def get_duration_display(self):
        duration_seconds = self.duration.total_seconds()
        hours = int(duration_seconds / 3600)
        minutes = int((duration_seconds % 3600) / 60)
        return f"{hours} h {minutes} min."

    @property
    def start_date(self):
        return self.start_datetime.date()

    @property
    def start_time(self):
        return self.start_datetime.time()

    @property
    def end_time(self):
        if self.end_datetime:
            return self.end_datetime.time()

    def get_absolute_url(self):
        return reverse('activities:detail', args=[self.id])

    def is_active(self):
        return self.end_datetime is None

    def stop(self):
        if not self.is_active():
            raise RuntimeError('Activity must be active in order to stop it')
        # If activity is less than a minute, delete it
        self.end_datetime = timezone.now()
        if (self.end_datetime - self.start_datetime) < timezone.timedelta(
                minutes=1):
            self.delete()
            return
        self.save(update_fields=['end_datetime'])
