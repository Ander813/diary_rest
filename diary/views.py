from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecordsFilter
from .models import Record, RecordType, AbstractRecordType
from .serializers import RecordSerializer, RecordTypeSerializer, AbstractRecordTypeSerializer, UserSerializer


class RecordListView(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filter_class = RecordsFilter


class RecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        return Record.objects.filter(id=self.kwargs['pk'])


class RecordTypeListView(generics.ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.query_params.get('abstract', '') == 'true':
            return AbstractRecordTypeSerializer
        else:
            return RecordTypeSerializer

    def get_queryset(self):
        if self.request.GET.get('abstract', None) == 'true':
            return AbstractRecordType.objects.all()
        return RecordType.objects.all()


class RecordTypeDetailView(generics.RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        if self.request.query_params.get('abstract', '') == 'true':
            return AbstractRecordTypeSerializer
        else:
            return RecordTypeSerializer

    def get_queryset(self):
        return RecordType.objects.filter(id=self.kwargs['pk'])


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserLoginView(APIView):
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        if request.user.is_authenticated:
            return Response('Already logged in')

        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return Response("Authorized")
        return Response("Wrong email/password")
    

class UserLogoutView(APIView):
    
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response('Logged out')
        else:
            return Response('You are not logged in')

