from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone

#this is for rename the profile images with username
def user_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "images/profiles/Profile_%s.%s" % (instance.User, extension)
    return new_filename

# this model adds some extra fields to Django User model.
class Extendeduser(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Profile = models.ImageField(upload_to=user_directory_path, default='notes/default.jpg')
    Phone = models.CharField(max_length=15)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.User}'



#for choose Background color
COLOR_CHOICES =[
    ('white','White'),
    ('red','Red'),
    ('orange','Orange'),
    ('yellow','Yellow'),
    ('green','Green'),
    ('blue','Blue'),
    ('purple','Purple'),
    ('black','Black')
]

    
# this is for image rename
def user_directory_path2(instance, filename):
    new_filename = "images/Note_%s" % (instance.Image)
    return new_filename


class ImageList(models.Model):
    Title = models.CharField(max_length=30,default='Image-list')

    def __str__(self):
        return f'{self.Title}'

class Image(models.Model):
    ImageList = models.ForeignKey(ImageList,on_delete=models.CASCADE,default=None)
    Image = models.ImageField(upload_to=user_directory_path2, default='notes/default.jpg')

    def __str__(self):
        return f'{self.ImageList}: {self.Image}'

class List(models.Model):
    Title = models.CharField(max_length=30,default='Task-list')
    
    def __str__(self):
        return f'{self.Title}'

class ListItem(models.Model):
    List = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
    Task = models.CharField(max_length=30, default='task')
    Done = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.List}: {self.Task}'
        

class Note(models.Model):
    Title = models.CharField(max_length=50)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    List = models.ForeignKey(List, on_delete=models.CASCADE)
    ImageList = models.ForeignKey(ImageList, on_delete=models.CASCADE, default=None)
    Labels = models.CharField(max_length=30, null=True)
    Background_color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='white')
    Description = models.TextField()
    Reminder = models.DateTimeField(default=None, null=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Title}: {self.User}'

    @property
    def Labels_list(self):
        labels = self.Labels
        labels_list = labels.split(',')
        return labels_list


