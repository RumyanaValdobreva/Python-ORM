from django.db import models


class IsAwardedMixin(models.Model):
    is_awarded = models.BooleanField(default=False)

    class Meta:
        abstract = True


class LastUpdatedMixin(models.Model):
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
