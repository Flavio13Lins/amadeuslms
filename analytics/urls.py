from django.conf.urls import url, include
from . import views


urlpatterns = [
	url(r'^view/general/$', views.GeneralView.as_view(), name='view_general'),

	#"api" callls
	url(r'^most_used_tags/$', views.most_used_tags, name="most_used_tags"),
]