from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list$', views.list, name='list'),
    url(r'^add_edit$', views.add_edit, name='add_edit'),
    url(r'^delete$', views.delete, name='delete')
]
