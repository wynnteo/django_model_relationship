from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
# Create your models here.


class Account(models.Model):
    account_number = models.CharField(max_length=30)
    account_type = models.CharField(max_length=20)
    open_date = models.DateField()
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='accounts',
                             on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
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
    username = None
    email = models.EmailField(verbose_name='email address', unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """ Return string representation of our user """
        return self.email

# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     sku = models.CharField(max_length=20)
#     price = models.DecimalField(default=0, decimal_places=2, max_digits=8)

# class Order(models.Model):
#     order_date = models.DateField()
#     status = models.CharField(max_length=20)
#     products = models.ManyToManyField(Product, related_name="products")


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=20)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)


class Order(models.Model):
    order_date = models.DateField()
    status = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, through="Detail")


class Detail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
