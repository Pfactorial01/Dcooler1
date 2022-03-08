from django.contrib import admin
from .models import Issue, Personnel, Project
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Personnel)
admin.site.register(Issue)
