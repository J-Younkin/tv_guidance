from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create', views.create_user),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^shows$', views.success),
]