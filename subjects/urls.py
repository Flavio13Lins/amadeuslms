from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^create/(?P<slug>[\w_-]+)/$', views.SubjectCreateView.as_view(), name='create'),
]