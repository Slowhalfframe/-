from django.conf.urls import url
from . import views


urlpatterns = [
    url('^detail/$', views.detail, name='detail'),
    url('^add_course/$', views.add_course, name='add_course'),
    url('^update_course/$', views.update_course, name='update_course'),
    url('^study/$', views.study, name='study'),
    url('^comment/$', views.comment, name='comment'),
    url('^download/$', views.download, name='download'),
    url('^collect/$', views.collect, name='collect'),
    url('^search/$', views.search, name='search'),
    url('^del_course/$', views.del_course, name='del_course'),
    url('^type/$', views.type, name='type'),
]
