from django.db.models.query import QuerySet
from django.http import response
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from .permissions import IsOwner
from django.conf import settings
from django.contrib import auth
import jwt

 # this section is for login, jwt authentication

# Register API
class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY, algorithm="HS256")

            serializer = UserSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

            # SEND Response
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#---------------------------------------------------------------------------------------------

class UserViewSet(ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = '__all__'
    ordering_fields = '__all__'


class ImageListViewSet(ModelViewSet):
    serializer_class =ImageListSerializer
    queryset = ImageList.objects.all()

    def list(self, request):
            
        ListObj = ImageList.objects.all()
        Tasks = {}
        List_obj = []
        for item in ListObj:
            Title = item.Title
            Id = item.id
            item.Title = []
            
            ListItems = Image.objects.filter(ImageList = item.id)
            for items in ListItems:
                Tasks.update({'id':items.id, 'Image':str(items.Image),})
                Tasks_copy = Tasks.copy()
                
                item.Title.append(Tasks_copy)
            List_obj.append({f'id:{Id}-{Title}':item.Title})
            
        return Response(List_obj)


class ImageViewSet(ModelViewSet):
    serializer_class =ImageSerializer
    queryset = Image.objects.all()

    
class ListViewSet(ModelViewSet):
    serializer_class =ListSerializer
    queryset = List.objects.all()

    def list(self, request):
            
        ListObj = List.objects.all()
        Tasks = {}
        List_obj = []
        for item in ListObj:
            Title = item.Title
            Id = item.id
            item.Title = []
            
            ListItems = ListItem.objects.filter(List = item.id)
            for items in ListItems:
                Tasks.update({'id':items.id, 'Task':items.Task, 'done':items.Done})
                Tasks_copy = Tasks.copy()
                
                item.Title.append(Tasks_copy)
            List_obj.append({f'id:{Id}-{Title}':item.Title})
            
        return Response(List_obj)

class ListItemViewSet(ModelViewSet):
    serializer_class =ListItemsSerializer
    queryset = ListItem.objects.all()


# get all notes created by logged in user
class NoteViewSet(ModelViewSet):
    serializer_class =NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [IsOwner,permissions.IsAuthenticated]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['^Title',]
    ordering_fields =['Title','Created_at','Updated_at']



class RegisterViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                
                "Message": "User created successfully",
                
                "User": serializer.data}, status=status.HTTP_201_CREATED
                )
        
        return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ExtendedUserViewSet(ModelViewSet):
    serializer_class = ExtendeduserSerializer
    permission_classes = [IsOwner,permissions.IsAuthenticated]
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




