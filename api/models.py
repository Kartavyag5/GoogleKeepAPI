from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'images/{0}'.format(filename)

class Label(models.Model):
    Name = models.CharField(max_length=20)

class Image(models.Model):
    Title = models.CharField(max_length=250)
    Alt = models.TextField(null=True)
    image = models.ImageField(upload_to=user_directory_path, default='notes/default.jpg ')

class ListItem(models.Model):
    Name = models.CharField(max_length=250)
    Done = models.BooleanField(default=False)
    Position = models.IntegerField(default=1)


class List(models.Model):
    Item = models.ManyToManyField(ListItem)
    

class Note(models.Model):
    Title = models.CharField(max_length=50)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Lists = models.ManyToManyField(List)
    Labels = models.ManyToManyField(Label)
    Images = models.ManyToManyField(Image)
    Position = models.IntegerField(max_length=10)
    Description = models.TextField()
    Reminder = models.DateTimeField()
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Title}:{self.User}'


