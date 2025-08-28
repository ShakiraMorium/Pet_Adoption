# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from users.managers import CustomUserManager

# # Create your models here.

# class PetUser(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True)
#     address = models.TextField(blank=True, null=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)

#     USERNAME_FIELD = 'email' 
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email


# users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class PetUser(AbstractUser):
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    
    groups = models.ManyToManyField(
        Group,
        related_name="petuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="petuser_set_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
