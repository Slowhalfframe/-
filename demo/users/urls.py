from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sign_in/$', views.sign_in, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_info/$', views.user_info, name='user_info'),
    url(r'^code/$', views.code, name='code'),
    url(r'^off/$', views.off, name='off'),
    url(r'^edit/$', views.edit, name='edit'),
]