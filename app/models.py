from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    dob = models.DateField()
    mobile = models.CharField(max_length=30)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('Email can not be null.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    pass
    # add additional fields in here
    username = None
    email = models.EmailField(verbose_name='email address', unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """ Return string representation of our user """
        return self.email
