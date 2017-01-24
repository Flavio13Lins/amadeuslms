from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	url(r'^create/(?P<slug>[\w_-]+)/$', views.CreateView.as_view(), name = 'create'),
	url(r'^download/(?P<slug>[\w_-]+)/$', views.DownloadFile.as_view(), name = 'download'),
]
