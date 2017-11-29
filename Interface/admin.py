from django.contrib import admin
from .models import User
from .models import HuntCommand
from .models import Landmarks
from .models import Game


admin.site.register(User)
admin.site.register(HuntCommand)
admin.site.register(Landmarks)
admin.site.register(Game)

