from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	url(r'^create/(?P<slug>[\w_-]+)/$', views.CreateView.as_view(), name = 'create'),
	url(r'^update/(?P<sub_slug>[\w_-]+)/(?P<slug>[\w_-]+)/$', views.UpdateView.as_view(), name = 'update'),
	url(r'^update_order/$', views.update_order, name = 'update_order'),
]
