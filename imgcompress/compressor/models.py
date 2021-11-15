from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone


# Create your models here.
class UserAccountManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        
        user = self.model(email=email,**extra_fields)
        user.set_password(password) 
        user.save()
        return user
    def create_superuser(self,email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserAccounts(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['first_name','last_name']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    def get_short_name(self):
        return self.first_name
    def __str__(self):
        return self.email

ACTION_CHOICES = (
    ('compress','compress'),
    ('resize','resize'),
)

class Upload(models.Model):
    uploaded_image = models.ImageField(upload_to='photos',blank=True,null=True)
    current_size =models.CharField(max_length=200,blank=True,null=True)
    size_after = models.CharField(max_length=200,blank=True,null=True)
    action = models.CharField(max_length=50,choices=ACTION_CHOICES,default='compress')
    compress_percentage = models.IntegerField(blank=True,null=True,default=50)
    resize_measure_x = models.IntegerField(blank=True,null=True,default=500)
    resize_measure_y = models.IntegerField(blank=True,null=True,default=500)
    orignal_size_x_y = models.CharField(max_length=50,blank=True,null=True)
    will_be_delete_at = models.DateTimeField(blank=True,null=True)
    

    def save(self, *args,**kwargs):
        self.will_be_delete_at = timezone.now() + timedelta(minutes = 10)
        return super().save(*args,**kwargs)

    def __str__(self):
        return str(self.uploaded_image)
    
    def delete_old_item(self):
        super().delete()
