from rest_framework import serializers
from authorizations.models import Authorizations


class AuthorizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Authorizations
        exclude = ('issuer',)


class AdminAuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorizations
        fields = ('id', 'issuer', 'server', 'client', 'start_validity', 'expiration_time')
