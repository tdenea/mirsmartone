from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from user.models import User

class UserAdmin(BaseUserAdmin):
  pass

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
