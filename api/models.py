from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

class Extendeduser(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Profile = models.OneToOneField('Image', on_delete=models.CASCADE)
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

class Image(models.Model):
    Name = models.CharField(max_length=250)
    Alt = models.TextField(null=True)
    Image = models.ImageField(upload_to=user_directory_path, default='notes/default.jpg')

    def __str__(self):
        return f'{self.Name}'

class ListItem(models.Model):
    Name = models.CharField(max_length=250)
    Done = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.Name}'


class List(models.Model):
    Items = models.ManyToManyField(ListItem, related_name='Lists')
    
    def __str__(self):
        return f'{self.Items}'

class Note(models.Model):
    Title = models.CharField(max_length=50)
    User = models.ForeignKey(Extendeduser, on_delete=models.CASCADE)
    List = models.ForeignKey(List,on_delete=models.CASCADE)
    Labels = models.CharField(max_length=30)
    Images = models.ManyToManyField(Image, related_name='Notes')
    Background_color = models.CharField(max_length=20, choices=COLOR_CHOICES, default=None)
    Description = models.TextField()
    Reminder = models.DateTimeField()
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Title}:{self.User}'

    @property
    def Labels_list(self):
        labels = self.Labels
        labels_list = labels.split(',')
        return labels_list


