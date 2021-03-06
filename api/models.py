from django.db import models
from django.contrib.auth.models import User

# this is for rename the profile images with username


def user_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "images/profiles/Profile_%s.%s" % (instance.User, extension)
    return new_filename

# this model adds some extra fields to Django User model.


class Extendeduser(models.Model):
    User = models.ForeignKey(User,related_name='Extra_details',on_delete=models.CASCADE)
    Profile = models.ImageField(upload_to=user_directory_path, default='notes/default.jpg')
    Phone = models.CharField(max_length=15)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.User}'




# this is for image rename
def user_directory_path2(instance, filename):
    new_filename = "images/Image_%s" % (instance.Image)
    return new_filename


class ImageList(models.Model):
    User = models.ForeignKey(
        'auth.User', related_name='image_lists', on_delete=models.CASCADE, default='1')
    Title = models.CharField(max_length=30, default='Image-list')
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Title}'


class Image(models.Model):
    User = models.ForeignKey('auth.User', on_delete=models.CASCADE,default=None, null=True, blank=True)
    ImageList = models.ForeignKey(
        ImageList, on_delete=models.CASCADE, default=None)
    Image = models.ImageField(
        upload_to=user_directory_path2, default='notes/default.jpg')
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.ImageList}_{self.Image}'


class List(models.Model):
    User = models.ForeignKey(
        'auth.User', related_name='Task_lists', on_delete=models.CASCADE, default='1')
    Title = models.CharField(max_length=30, default='Task-list')
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Title}'


class ListItem(models.Model):
    User = models.ForeignKey('auth.User', on_delete=models.CASCADE,default=None, null=True, blank=True)
    List = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
    Task = models.CharField(max_length=30, default='task')
    Done = models.BooleanField(default=False)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.List}_{self.Task}'

# for choose Background color in Note model
COLOR_CHOICES = [
    ('white', 'White'),
    ('red', 'Red'),
    ('orange', 'Orange'),
    ('yellow', 'Yellow'),
    ('green', 'Green'),
    ('blue', 'Blue'),
    ('purple', 'Purple'),
    ('black', 'Black')
]

class Note(models.Model):
    Title = models.CharField(max_length=50, blank=True)
    User = models.ForeignKey(
        'auth.User', related_name='notes', on_delete=models.CASCADE)
    List = models.ForeignKey(List, on_delete=models.CASCADE, default=None, null=True, blank=True)
    ImageList = models.ForeignKey(
        ImageList, on_delete=models.CASCADE, default=None, null=True, blank=True)
    Labels = models.CharField(max_length=30, null=True)
    Background_color = models.CharField(
        max_length=20, choices=COLOR_CHOICES, default='white', blank=True)
    Description = models.TextField(blank=True)
    Reminder = models.DateTimeField(default=None,null=True, blank=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Title}: {self.User}'

    @property
    def Labels_list(self):
        labels = self.Labels
        labels_list = labels.split(',')
        return labels_list
