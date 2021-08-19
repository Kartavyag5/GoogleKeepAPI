from django.db.models import fields
from rest_framework import serializers, fields
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'Name', 'Image', 'Alt')

# User Serializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ExtendeduserSerializer(serializers.ModelSerializer):
    User = UserSerializer()
    Profile = ImageSerializer()
    class Meta:
        model = Extendeduser
        fields = ('User','Phone','Profile')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    Profile = ImageSerializer()
    class Meta:
        model = Extendeduser
        fields = ('id','user', 'username', 'email', 'password','Phone','Profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    #Serializer for password change endpoint.
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
        

class ListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItem
        fields = ('Name','Done')

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        ListItems = ListItemsSerializer(many=True)
        fields = ('Items','ListItems')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('Name','Image','Alt')

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        User = UserSerializer()
        Images = ImageSerializer(many=True)
        List = ListSerializer()
        Labels = fields.Field(source = 'Labels_list')
        fields = ('id','Title','Description','List','Labels_list','Images','Background_color','Reminder','Created_at','Updated_at')
