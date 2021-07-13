from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from authorizations.models import Authorizations
from .serializers import AuthorizationSerializer


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


class AuthorizationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = AuthorizationSerializer
    queryset = Authorizations.objects.all()


class AuthorizationRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = AuthorizationSerializer
    queryset = Authorizations.objects.all()
