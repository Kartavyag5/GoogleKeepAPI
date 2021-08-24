from django.db.models import fields
from rest_framework import serializers, fields
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import *

# this is for testing purpose

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, min_length=6)
    username = serializers.CharField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email already exists')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ('username already exists')})

        return super().validate(args)
  

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class loginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('username','password')

#-----------------------------------------------------------


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('Image',)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','password')
        

# this model is for adding more fields in Django User model
class ExtendeduserSerializer(serializers.ModelSerializer):
    User = UserSerializer()

    class Meta:
        model = Extendeduser
        fields = ('User', 'Phone', 'Profile', 'Created_at', 'Updated_at')

# Register Serializer


# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             validated_data['username'], validated_data['email'], validated_data['password'])
#         return user


# class loginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#         extra_kwargs = {'password': {'write_only': True}}


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    # Serializer for password change endpoint.
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItem
        fields = ('Name', 'Done')


class ListSerializer(serializers.ModelSerializer):
    Items = ListItemsSerializer(many=True)

    class Meta:
        model = List
        fields = ('Title', 'Items')


class NoteSerializer(serializers.ModelSerializer):
    User = ExtendeduserSerializer()
    Images = ImageSerializer(many=True)
    List = ListSerializer()

    class Meta:
        model = Note
        Labels = fields.Field(source='Labels_list')
        fields = ('id', 'Title', 'Description', 'User', 'List', 'Labels_list',
                  'Images', 'Background_color', 'Reminder', 'Created_at', 'Updated_at')
