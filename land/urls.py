from django.conf.urls import url
from land import views

urlpatterns = [
    url(r'^create-account/$', views.create_account, name='create_account'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^land/register/$', views.register_land, name='register_land'),
    url(r'^land/display/$', views.display_lands, name='display_lands'),
]

