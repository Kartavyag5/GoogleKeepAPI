from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.utils import timezone

#this is for rename the profile images with username
def user_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    og_filename = filename.split('.')[0]
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


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {username}".format(username=reset_password_token.user.username),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

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

    
# this is for image rename to
def user_directory_path2(instance, filename):
    new_filename = "images/Note_%s" % (instance.Image)
    return new_filename


class Image(models.Model):
    Image = models.ImageField(upload_to=user_directory_path2, default='notes/default.jpg')

    def __str__(self):
        return f'{self.Image}'

class ListItem(models.Model):
    Name = models.CharField(max_length=250)
    Done = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.Name}'


class List(models.Model):
    Title = models.CharField(max_length=30,default='Task-list')
    Items = models.ManyToManyField(ListItem, related_name='Lists')
    
    def __str__(self):
        return f'List: {self.Title}'

class Note(models.Model):
    Title = models.CharField(max_length=50)
    User = models.ForeignKey(Extendeduser, on_delete=models.CASCADE)
    List = models.ForeignKey(List, on_delete=models.CASCADE)
    Labels = models.CharField(max_length=30)
    Images = models.ManyToManyField(Image, related_name='Notes', default=None)
    Background_color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='white')
    Description = models.TextField()
    Reminder = models.DateTimeField(default=None)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Title}: {self.User}'

    @property
    def Labels_list(self):
        labels = self.Labels
        labels_list = labels.split(',')
        return labels_list


