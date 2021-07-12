from django.db import models
from django.utils import timezone

from accounts.models import Profile
# Create your models here.


class Authorizations(models.Model):
    issuer = models.ForeignKey(Profile, on_delete=models.PROTECT)
    server = models.CharField(max_length=32)
    client = models.CharField(max_length=32)
    start_validity = models.DateTimeField(default=timezone.now)
    expiration_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'authorizations'
