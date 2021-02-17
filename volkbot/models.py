from django.db import models

class Quote(models.Model):
    value = models.CharField('Quote to say',
        max_length=1024,
        blank=True, null=True
    )