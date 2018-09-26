from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
# Create your models here.

class TimestamptedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True


class CustonUserModel(TimestamptedModel):
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    class Meta:

        verbose_name = "visiteur"
        unique_together = ("username", "email")

    def __str__(self):
        return self.username
