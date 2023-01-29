from django.contrib.auth.models import AbstractUser
import uuid
from .manager  import CustomUserManager
from django.db import models

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.uid, filename)


def image_directory_path(instance, filename):
    return 'image_{0}/{1}'.format(instance.uid, filename)

class User(AbstractUser):
    username = None
    uid = models.UUIDField(default = uuid.uuid4 , primary_key=True , editable=False)
    email = models.EmailField(unique= True)
    image = models.FileField(upload_to = user_directory_path)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Transfer(models.Model):
    uid = models.UUIDField(default = uuid.uuid4 , primary_key=True , editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver",null=True)
    amount = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f'{self.sender}-{self.amount}'

class Image(models.Model):
    uid = models.UUIDField(default = uuid.uuid4 , primary_key=True , editable=False)
    image = models.FileField(upload_to = image_directory_path)

    def __str__(self):
        return f'{self.uid}'