from django.db import models
from django.utils import timezone
from accounts.models import Profile
from trillian.models import Trillian


# Create your models here.
class Authorizations(models.Model):
    issuer = models.ForeignKey(Profile, on_delete=models.PROTECT)
    server = models.CharField(max_length=32)
    client = models.CharField(max_length=32)
    start_validity = models.DateTimeField(default=timezone.now)
    expiration_time = models.DateTimeField()
    inclusion_proof = models.TextField()

    class Meta:
        verbose_name_plural = 'authorizations'

#    def save(self, *args, **kwargs):
        # set the value of the read_only_field using the regular field
        # call the save() method of the parent
#        super.save(*args, **kwargs)
