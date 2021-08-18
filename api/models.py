from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
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
    Items = models.ManyToManyField(ListItem)
    

class Note(models.Model):
    Title = models.CharField(max_length=50)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Lists = models.ForeignKey(List,on_delete=models.CASCADE)
    Labels = models.ManyToManyField(Label)
    Images = models.ManyToManyField(Image, related_name='Notes')
    Background_image = models.ForeignKey(Image, on_delete=models.CASCADE, default=None)
    Background_color = models.CharField(max_length=20, choices=COLOR_CHOICES, default=None)
    Position = models.IntegerField()
    Description = models.TextField()
    Reminder = models.DateTimeField()
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Title}:{self.User}'


