from django.db.models import fields
from rest_framework import serializers, fields
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('Image',)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        #extra_kwargs = {'password': {'write_only': True}}


# this model is for adding more fields in Django User model
class ExtendeduserSerializer(serializers.ModelSerializer):
    User = UserSerializer(read_only=True)

    class Meta:
        model = Extendeduser
        fields = ('User', 'Phone', 'Profile', 'Created_at', 'Updated_at')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    # Serializer for password change endpoint.
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id','Title',)


class ListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItem
        fields = ('List','id','Task', 'Done')


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageList
        fields = ('id','Title',)

class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = ('ImageList','Image')



class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        Labels = fields.Field(source='Labels_list')
        fields = ('id', 'Title', 'Description', 'User', 'List', 'Labels_list',
                  'ImageList', 'Background_color', 'Reminder', 'Created_at', 'Updated_at')
