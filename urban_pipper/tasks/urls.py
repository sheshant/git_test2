from django.conf.urls import url, include
from django.views.generic import TemplateView

from tasks import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^tasks/$', views.task_list, name='task_list'),
    url(r'^tasks/create/$', views.task_create, name='task_create'),
    url(r'^tasks/(?P<pk>\d+)/update/$', views.task_update, name='task_update'),
    url(r'^tasks/(?P<pk>\d+)/delete/$', views.task_delete, name='task_delete'),
]
