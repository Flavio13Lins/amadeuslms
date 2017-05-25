from django.conf.urls import url, include
from . import views


urlpatterns = [

	#"api" callls
	url(r'^most_used_tags/$', views.most_used_tags, name="most_used_tags"),
	url(r'^most_accessed_subjects/$', views.most_accessed_subjects, name="most_accessed_subjects"),
	url(r'^most_accessed_categories/$', views.most_accessed_categories, name = "most_accessed_categories"),
	url(r'^most_accessed_resources/$', views.most_accessed_resource_kind, name= "most_accessed_resources"),
	url(r'^most_active_users/$', views.most_active_users, name= "most_active_users"),
	url(r'^amount_active_users_per_day/$', views.most_active_users_in_a_month, name="most_active_users_in_a_month"),
	url(r'^get_days_of_the_week_log/$', views.get_days_of_the_week_log, name="get_days_of_the_week_log"),
	url(r'^get_category_tags/$', views.category_tags, name='get_category_tags'),
]