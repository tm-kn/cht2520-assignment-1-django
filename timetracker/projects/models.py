from django.db import models


class Project(models.Model):
    sheet = models.ForeignKey(
        'sheets.Sheet',
        models.CASCADE,
        related_name='projects'
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
