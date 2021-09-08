from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import *
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

# ---------------------------------start of user Section--------------------------------------------

# Register API

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
                'status': 'successfully Create a new user!! ',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

# show all users
class UserViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated|permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = '__all__'
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = self.queryset
        #if user is admin 
        if self.request.user.id == 18:
            query_set = queryset.all()
        else:    
            query_set = queryset.filter(id=self.request.user.id)
        
        return query_set

# shows all users with extra details (phone, Image)

class ExtendedUserViewSet(ModelViewSet):
    serializer_class = ExtendeduserSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Extendeduser.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['^username', '^email', '^Created_at', '^Updated_at']
    ordering_fields = ['username', 'Created_at', 'Updated_at']

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.id == 18:
            query_set = queryset.all()
        else:    
            query_set = queryset.filter(User=self.request.user.id)

        if query_set.count()==0:
            raise ValidationError(detail="Logged user has no Extra Details / no Logged in")

        return query_set


# change password of logged in user
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

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

# --------------------------------------end of User section------------------------------------------


# -----------------------start of Note Objects section-------------------------------------------

class ImageListViewSet(ModelViewSet):
    serializer_class = ImageListSerializer
    queryset = ImageList.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(User=self.request.user)

    def list(self, request):
        # if user is admin then any data it can see,edit,delete.
        if request.user.id == 18:
            ListObj = ImageList.objects.all()
        else:    
            ListObj = ImageList.objects.filter(User=self.request.user.id) 
        
        if ListObj.count() == 0:
            return Response({'msg': 'user did not create any list / No User logged in'})
        Tasks = {}
        List_obj = []
        for item in ListObj:
            Title = item.Title
            Id = item.id
            item.Title = []

            ListItems = Image.objects.filter(ImageList=item.id)
            for items in ListItems:
                Tasks.update({'id': items.id, 'Image': str(items.Image), })
                Tasks_copy = Tasks.copy()

                item.Title.append(Tasks_copy)
            List_obj.append({f'id:{Id}-{Title}': item.Title})

        return Response(List_obj)


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        # if user is admin.
        if self.request.user.id == 18:
            query_set = queryset.all()
            
        else:    
            query_set = queryset.filter(User=self.request.user.id)
            
        if query_set.count()==0:
            raise ValidationError(detail="Logged user has not create any Image yet")

        return query_set



class ListViewSet(ModelViewSet):
    serializer_class = ListSerializer
    queryset = List.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(User=self.request.user)

    def list(self, request):
        # if user is admin then any data it can see,edit,delete.
        if request.user.id == 18:
            ListObj = List.objects.all()
        else:    
            ListObj = List.objects.filter(User=self.request.user.id)    

        if ListObj.count() == 0:
            return Response({'msg': 'user did not create any list / No User logged in'})
        Tasks = {}
        List_obj = []
        for item in ListObj:
            Title = item.Title
            Id = item.id
            item.Title = []
            ListItems = ListItem.objects.filter(List=item.id)
            for items in ListItems:
                Tasks.update({
                        'id': items.id, 
                        'Task': items.Task,
                        'done': items.Done
                    })

                Tasks_copy = Tasks.copy()

                item.Title.append(Tasks_copy)
            List_obj.append({f'id:{Id}-{Title}': item.Title})

        return Response(List_obj)


class ListItemViewSet(ModelViewSet):
    serializer_class = ListItemsSerializer
    queryset = ListItem.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        # if user is admin.
        if self.request.user.id == 18:
            query_set = queryset.all()
        else:    
            query_set = queryset.filter(User=self.request.user.id)

        if query_set.count()==0:
            raise ValidationError(detail="Logged user has not create any Note yet")

        return query_set


# get all notes created by logged in user
class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['^Title', ]
    ordering_fields = ['Title', 'Created_at', 'Updated_at']

    def perform_create(self, serializer):
        serializer.save(User=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        # if user is admin.
        if self.request.user.id == 18:
            query_set = queryset.all()
        else:    
            query_set = queryset.filter(User=self.request.user.id)

        if query_set.count()==0:
            raise ValidationError(detail="Logged user has not create any Note yet")

        return query_set

    #this function will show only data created by user
    # def list(self, request):
    #     # if user is admin then any data it can see,edit,delete.
    #     if request.user.id == 18:
    #         note = Note.objects.all()
    #     else:    
    #         note = Note.objects.filter(User=self.request.user.id)

    #     if note.count() == 0:
    #         return Response({'msg': 'user did not create any Note / No User logged in'})
    #     note_list = []
    #     note_obj = {}
    #     for items in note:
    #         label = items.Labels
    #         label_list = label.split(',')
    #         note_obj.update({
    #             'id': items.id,
    #             'Title': items.Title,
    #             'Description': items.Description,
    #             'user': str(items.User),
    #             'List' : str(items.List),
    #             'Labels': label_list,
    #             'ImageList' : str(items.ImageList),
    #             'Background_color': items.Background_color,
    #             'Reminder': items.Reminder,
    #             'Created_at': items.Created_at,
    #             'Updated_at': items.Updated_at,
    #         })
    #         note_obj_copy = note_obj.copy()
    #         note_list.append(note_obj_copy)
    #     return Response({f'id:{request.user.id}-{request.user.username}': note_list})
