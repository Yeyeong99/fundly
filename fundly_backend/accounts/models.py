from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, username, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address.')
        
        user = self.model(
            username=username,
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username=None, nickname=None, email=None, provider='Fundly', password=None, **extra_fields):
        superuser = self.create_user(
            username=username,
            email=email,
            provider=provider,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    social_id = models.CharField(max_length=50, null=True, blank=True)
    provider = models.CharField(max_length=10, default='fundly')
    birth_date = models.DateField(null=True)
    work_type = models.CharField(max_length=20, null=True, blank=True)
    assets = models.CharField(max_length=50, null=True, blank=True)
    salary = models.CharField(max_length=50, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]