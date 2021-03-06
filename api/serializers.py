from rest_framework.fields import Field
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('Image',)

# User Serializer for use in extended serializer


class UserSerializer(serializers.ModelSerializer):
    notes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Note.objects.all())
    Task_lists = serializers.PrimaryKeyRelatedField(
        many=True, queryset=List.objects.all())
    image_lists = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ImageList.objects.all())
    Extra_details = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Extendeduser.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email','Extra_details', 'notes',
                  'Task_lists', 'image_lists',)
        extra_kwargs = {'password': {'write_only': True}}


# this model is for adding more fields in Django User model
class ExtendeduserSerializer(serializers.ModelSerializer):
    #User = UserSerializer(read_only=True)

    class Meta:
        model = Extendeduser
        fields = ('id','Phone', 'Profile', 'Created_at', 'Updated_at')



# Serializer for password change endpoint.
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# --------------------------------------------------------------------------------------------


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'Title','User', 'Created_at', 'Updated_at')


class ListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItem
        fields = ('List', 'id', 'Task', 'Done','User', 'Created_at', 'Updated_at')


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageList
        fields = ('id', 'Title','User', 'Created_at', 'Updated_at')


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id','ImageList','User', 'Image', 'Created_at', 'Updated_at')


class NoteSerializer(serializers.ModelSerializer):
    User = serializers.ReadOnlyField(source='User.username')

    class Meta:
        model = Note
        Labels_list = Field(source='Labels_list')
        fields = ['id', 'Title', 'Description', 'User', 'List', 'Labels_list', 'Labels',
                  'ImageList', 'Background_color', 'Reminder', 'Created_at', 'Updated_at']
        extra_kwargs = {'Labels': {'write_only': True}}
