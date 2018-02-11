
# Create your models here.
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    edit_date = models.DateTimeField(
            blank=True, null=True)
    enable = models.SmallIntegerField(default=0)

    def set_enable(self, k):  # 0-можно 1-нельзя юзеру 2-нельзя админу
        self.enable = k

    def last_edited(self):
        self.edit_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class ListUsers(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    enable_user = models.BooleanField(default=False)

    def enable(self, k=False):
        self.enable_user = k
        self.save()

    def __str__(self):
        return self.title
