from django.conf.urls import url
from projects.views import ProjectList, ProjectCreate, ProjectUpdate, ProjectDelete, ProjectDetail, UploadView


urlpatterns = [
    url(r'^$', ProjectList.as_view(), name='project-list'),
    url(r'add/$', ProjectCreate.as_view(), name='project-add'),
    url(r'(?P<pk>[0-9]+)/update/$', ProjectUpdate.as_view(), name='project-update'),
    url(r'(?P<pk>[0-9]+)/$', ProjectDetail.as_view(), name='project-detail'),
    url(r'(?P<pk>[0-9]+)/delete/$', ProjectDelete.as_view(), name='project-delete'),

    url(r'(?P<pk>[0-9]+)/upload/$', UploadView.as_view(), name='project-upload'),

]
