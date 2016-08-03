from django.conf.urls import url
from projects.views import ProjectList, ProjectCreate, ProjectUpdate, ProjectDelete, ProjectDetail, UploadView

from . import views

urlpatterns = [
    url(r'^$', ProjectList.as_view(), name='project-list'),
    url(r'add/$', ProjectCreate.as_view(), name='project-add'),


    url(r'(?P<pk>[0-9]+)/update/$', ProjectUpdate.as_view(), name='project-update'),
    url(r'(?P<pk>[0-9]+)/$', ProjectDetail.as_view(), name='project-detail'),
    url(r'(?P<pk>[0-9]+)/delete/$', ProjectDelete.as_view(), name='project-delete'),
    url(r'(?P<pk>[0-9]+)/upload/$', UploadView.as_view(), name='project-upload'),

    url(r'^(?P<project_id>[0-9]+)/import/$', views.import_files, name='project-import'),

    url(r'^action/$', views.action, name='project-action'),

]
