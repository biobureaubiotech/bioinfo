from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.analysis_list, name='analysis-list'),
    url(r'^tasks/$', views.task_list, name='task-list'),

    url(r'add/(?P<project_id>[0-9]+)/$', views.add, name='analysis-add'),
    # url(r'(?P<pk>[0-9]+)/update/$', ProjectUpdate.as_view(), name='project-update'),
    # url(r'(?P<pk>[0-9]+)/$', ProjectDetail.as_view(), name='project-detail'),
    # url(r'(?P<pk>[0-9]+)/delete/$', ProjectDelete.as_view(), name='project-delete'),
    # url(r'(?P<pk>[0-9]+)/upload/$', UploadView.as_view(), name='project-upload'),

    # url(r'^action/$', views.action, name='project-action'),
]
