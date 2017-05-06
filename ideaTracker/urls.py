from django.conf.urls import url

from . import views

app_name = 'ideaTracker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'add', views.add, name='add'),
    url(r'edit', views.edit, name='edit'),
    url(r'^(?P<idea_id>[0-9]+)/$', views.detail, name='detail'),
]
