from django.db import models
# Create your models here.


class Authorizations(models.Model):
    email = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    identifier = models.CharField(max_length=32)
    public_key = models.TextField()
#    issuer = models.ForeignKey()
    server = models.CharField(max_length=32)
    client = models.CharField(max_length=32)
    start_validity = models.DateTimeField()
    expiration_time = models.DateTimeField()
