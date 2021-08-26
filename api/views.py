from django.db.models.query import QuerySet
from django.http import response
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import *
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from .permissions import IsOwner

from django.contrib.auth import login



# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    
    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })



class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = loginSerializer
    
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


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
    serializer_class = RegisterSerializer
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




