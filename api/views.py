from django.shortcuts import render
from rest_framework import generics, permissions
import jwt
from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from authorizations.models import Authorizations, Profile
from .serializers import AuthorizationSerializer, AdminAuthorizationSerializer


# Create your views here.
class AuthorizationListAPIView(generics.ListAPIView):
    serializer_class = AuthorizationSerializer

    def get_queryset(self):
        server = self.request.query_params.get('server')
        client = self.request.query_params.get('client')
        if server is not None:
            if client is not None:
                queryset = Authorizations.objects.filter(server=server, client=client)
            queryset = Authorizations.objects.filter(server=server)
        else:
            if client is not None:
                queryset = Authorizations.objects.filter(client=client)
            else:
                queryset = Authorizations.objects.all()
        return queryset


class AuthorizationCreateAPIView(generics.CreateAPIView):
    serializer_class = AuthorizationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminAuthorizationSerializer
        return AuthorizationSerializer

    def perform_create(self, serializer):
        serializer.save(issuer_id=self.request.user.pk)


class AuthorizationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = AuthorizationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminAuthorizationSerializer
        return AuthorizationSerializer

    def get_queryset(self):
        queryset = Authorizations.objects.filter(issuer_id=self.request.user.pk)
        return queryset


class AuthorizationRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AuthorizationSerializer

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminAuthorizationSerializer
        return AuthorizationSerializer

    def get_queryset(self):
        queryset = Authorizations.objects.filter(issuer_id=self.request.user.pk)
        print(queryset)
        return queryset


class JwtCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        token = self.request.data['token']
        user = self.request.data['user']
        profile = Profile.objects.get(user__username=user)
        public_key = profile.public_key
        data = jwt.decode(jwt=token, key=public_key, algorithms=['RS256'])
        print(data)
        start_validity = datetime.fromtimestamp(int(data['nbf']), tz=timezone.utc)
        expiration_time = datetime.fromtimestamp(int(data['exp']), tz=timezone.utc)
        Authorizations.objects.create(issuer=profile, server=data['server'],
                                      client=data['client'], start_validity=start_validity,
                                      expiration_time=expiration_time)
        return Response('Authorization create')


