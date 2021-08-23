from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from api.permissions import IsOwner
from rest_framework.authentication import BasicAuthentication


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginViewSet(ViewSet):
    serializer_class = loginSerializer
    
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(Login, self).post(request, format=None)
        
# get all notes created by logged in user
class NoteViewSet(ModelViewSet):
    serializer_class =NoteSerializer
    queryset = Note.objects.all()
    authentication_classes = [BasicAuthentication,]
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['^Title',]
    ordering_fields =['Title','Created_at','Updated_at']

# Get User API
class UserViewSet(ModelViewSet):
    serializer_class = ExtendeduserSerializer
    permission_classes = [IsOwner,]
    queryset = Extendeduser.objects.all()
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['^username','^email','^Created_at','^Updated_at']
    ordering_fields = ['username','Created_at','Updated_at']

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsOwner,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




