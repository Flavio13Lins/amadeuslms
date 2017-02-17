from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.GeneralIndex.as_view(), name='manage_general'),
	url(r'^categories/$', views.CategoryIndex.as_view(), name='manage_category'),
	url(r'^subjects/$', views.SubjectIndex.as_view(), name='manage_subject'),
	url(r'^create_gen/$', views.GeneralCreate.as_view(), name='create_general'),
	url(r'^create_cat/(?P<slug>[\w_-]+)/$', views.CategoryCreate.as_view(), name='create_category'),
	url(r'^create_sub/(?P<slug>[\w_-]+)/$', views.SubjectCreate.as_view(), name='create_subject'),
	url(r'^update_gen/(?P<pk>[\w_-]+)/$', views.GeneralUpdate.as_view(), name='update_general'),
	url(r'^update_cat/(?P<pk>[\w_-]+)/$', views.CategoryUpdate.as_view(), name='update_category'),
	url(r'^update_sub/(?P<pk>[\w_-]+)/$', views.SubjectUpdate.as_view(), name='update_subject'),
	url(r'^delete_gen/(?P<pk>[\w_-]+)/$', views.GeneralDelete.as_view(), name='delete_general'),
	url(r'^delete_cat/(?P<pk>[\w_-]+)/$', views.CategoryDelete.as_view(), name='delete_category'),
	url(r'^delete_sub/(?P<pk>[\w_-]+)/$', views.SubjectDelete.as_view(), name='delete_subject'),
	url(r'^load_category/([\w_-]+)/$', views.load_category_posts, name='load_category'),
	url(r'^load_subject/([\w_-]+)/$', views.load_subject_posts, name='load_subject'),
	url(r'^favorite/([\w_-]+)/$', views.favorite, name='favorite'),
	url(r'^deleted/$', views.deleted_post, name='deleted_post'),
	url(r'^comment/(?P<post>[\w_-]+)/$', views.CommentCreate.as_view(), name='create_comment'),
	url(r'^update_comment/(?P<pk>[\w_-]+)/$', views.CommentUpdate.as_view(), name='update_comment'),
	url(r'^delete_comment/(?P<pk>[\w_-]+)/$', views.CommentDelete.as_view(), name='delete_comment'),
	url(r'^deleted_comment/$', views.deleted_comment, name='deleted_comment'),
	url(r'^render_comment/([\w_-]+)/([\w_-]+)/$', views.render_comment, name='render_comment'),
	url(r'^render_post/([\w_-]+)/([\w_-]+)/([\w_-]+)/$', views.render_post, name='render_post'),
	url(r'^load_comments/([\w_-]+)/([\w_-]+)/$', views.load_comments, name='load_comments'),
	url(r'^suggest_users/$', views.suggest_users, name='suggest_users'),
]