from django.conf.urls import url
from land import views

urlpatterns = [
    url(r'^$', views.index, name='create_account'),
    url(r'^create-account/$', views.create_account, name='create_account'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^land/register/$', views.register_land, name='register_land'),
    url(r'^land/display/$', views.display_lands, name='display_lands'),
    url(r'^land/display/(?P<pk>[0-9])/$', views.land_detail, name='land_details'),
    url(r'^land/payment/(?P<pk>[0-9])/$', views.buy_land, name='buy_land'),
    url(r'^notifications/$', views.get_notification, name='notification'),
    url(r'^bought-lands/$', views.show_bought_land, name='lands_bought'),
    url(r'^transfer-land/(?P<pk>[0-9])/$', views.transfer_land, name='transfer_land'),
]