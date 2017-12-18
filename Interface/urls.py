from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='login'),
    url(r'^terminal/', views.terminal, name='terminal'),
    url(r'^validate/', views.validate, name="validate",),
    url(r'^user$', views.user, name="user",), #was user$
]