from django.conf.urls import url, include
from . import views


urlpatterns = [
	url(r'^view/general/$', views.GeneralView.as_view(), name='view_general'),
	
]