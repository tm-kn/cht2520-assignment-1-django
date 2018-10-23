from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Sheet(models.Model):
    title = models.SlugField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT, related_name='sheets')

    class Meta:
        unique_together = (
            'title',
            'user',
        )

    def __str__(self):
        return _('%(user)s/%(sheet)s') % {
            'user': self.user.username,
            'sheet': self.title,
        }
