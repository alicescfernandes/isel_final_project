from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
admin.site.register(CustomUser, UserAdmin)

"""
CustomUser.objects.create_user(
    username="MyGroup",
    password="secure_password",
    member_emails="member1@example.com, member2@example.com"
)
"""