from django.db.models import fields
from rest_framework import serializers, fields
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('Image',)

# User Serializer for use in extended serializer
class UserSerializer(serializers.ModelSerializer):
    notes = serializers.PrimaryKeyRelatedField(many=True, queryset=Note.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'notes')
        extra_kwargs = {'password': {'write_only': True}}



# this model is for adding more fields in Django User model
class ExtendeduserSerializer(serializers.ModelSerializer):
    User = UserSerializer(read_only=True)

    class Meta:
        model = Extendeduser
        fields = ('User', 'Phone', 'Profile', 'Created_at', 'Updated_at')


#Serializer for password change endpoint.
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

#--------------------------------------------------------------------------------------------

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
    User = serializers.ReadOnlyField(source='User.username')
    class Meta:
        model = Note
        Labels = fields.Field(source='Labels_list')
        fields = ('id', 'Title', 'Description', 'User', 'List', 'Labels_list',
                  'ImageList', 'Background_color', 'Reminder', 'Created_at', 'Updated_at')
