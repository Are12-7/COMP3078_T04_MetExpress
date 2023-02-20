from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=205, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# Topic
class Debate(models.Model):
    topic = models.CharField(max_length=205)

    def __str__(self):
        return self.topic


class Village(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # change it to false in production
    thread = models.ForeignKey(Debate, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    # Change to False in production
    description = models.TextField(null=True, blank=True)
    # Many to many / change to false in production
    sophists = models.ManyToManyField(
        User, related_name='sophists', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title


class Message(models.Model):
    # one to many
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.content[0:40]
