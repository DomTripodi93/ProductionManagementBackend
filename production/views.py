from django.http import HttpResponse
from django.conf import settings
from django_filters import rest_framework as filter

from .models import UserSettings, ProUser, Production, StartTime, Machine, Part, HourlyProduction, ChangeLog
from .serializers import ProUserSerializer, UserSettingsSerializer, StartTimeSerializer, ProductionSerializer, MachineSerializer, HourlyProductionSerializer, PartSerializer, ChangeLogSerializer
from .permissions import ViewOwnProduction, UpdateOwnProUser, CreateOwnProduction, UpdateOwnProduction

from rest_framework import status, viewsets, filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication 
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.filters import OrderingFilter

from .forms import UserCreationForm

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id, "name": token.user.name})

class ProductionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Production.objects.all().order_by('-date')
    serializer_class = ProductionSerializer
    permission_classes=(CreateOwnProduction, UpdateOwnProduction, )
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_fields = ("machine", "shift", "job", "date", "in_question")
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Production.objects.none()
        else:
            return Production.objects.filter(user=self.request.user).order_by('-date')

class MachineViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes=(CreateOwnProduction, UpdateOwnProduction, )
    filter_backends = (OrderingFilter,)
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Machine.objects.none()
        else:
            return Machine.objects.filter(user=self.request.user).order_by("machine")

class PartViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes=(CreateOwnProduction, UpdateOwnProduction, )
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_fields = ("machine", "part", "job", )
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Part.objects.none()
        else:
            return Part.objects.filter(user=self.request.user).order_by("-job")

class HourlyProductionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = HourlyProduction.objects.all()
    serializer_class = HourlyProductionSerializer
    permission_classes=(CreateOwnProduction, UpdateOwnProduction, )
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_fields = ("machine", "date", "job", )
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return HourlyProduction.objects.none()
        else:
            return HourlyProduction.objects.filter(user=self.request.user).order_by("machine", "-date")


class StartTimeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = StartTime.objects.all()
    serializer_class = StartTimeSerializer
    permission_classes=(CreateOwnProduction, UpdateOwnProduction, )
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_fields = ("machine", "date", "job", )
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return StartTime.objects.none()
        else:
            return StartTime.objects.filter(user=self.request.user).order_by("machine", "-date", "-time")

class ChangeLogViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = ChangeLog.objects.all()
    serializer_class = ChangeLogSerializer
    permission_classes=(CreateOwnProduction, UpdateOwnProduction, )
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_fields = ("changed_model", )
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return ChangeLog.objects.none()
        else:
            return ChangeLog.objects.filter(user=self.request.user).order_by("-timestamp")

class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = ProUserSerializer
    queryset = ProUser.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProUser, )


class UserSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSettingsSerializer
    queryset = UserSettings.objects.all().order_by('-user')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProduction, )

class LoginViewSet(viewsets.ViewSet):
    serializer_class= AuthTokenSerializer

    def create(self, request):
        return CustomObtainAuthToken().post(request)
