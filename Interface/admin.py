from django.contrib import admin
from .models import User
from .models import HuntCommand

admin.site.register(User)
admin.site.register(HuntCommand)

