from django.conf.urls import url, include

from . import views
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='manage'),
	url(r'^create/$', views.CreateCourseView.as_view(), name='create'),
	url(r'^edit/(?P<slug>[\w_-]+)/$', views.UpdateCourseView.as_view(), name='update'),
	url(r'^(?P<slug>[\w_-]+)/$', views.CourseView.as_view(), name='view'),
	url(r'^delete/(?P<slug>[\w_-]+)/$', views.DeleteCourseView.as_view(), name='delete'),
	url(r'^category/(?P<slug>[\w_-]+)/$', views.FilteredView.as_view(), name='filter'),
	url(r'^categories/view/$', views.IndexCatView.as_view(), name='manage_cat'),
	url(r'^categories/create/$', views.CreateCatView.as_view(), name="create_cat"),
	url(r'^categories/edit/(?P<slug>[\w_-]+)/$', views.UpdateCatView.as_view(), name='update_cat'),
	url(r'^categories/(?P<slug>[\w_-]+)/$', views.ViewCat.as_view(), name='view_cat'),
	url(r'^categories/delete/(?P<slug>[\w_-]+)/$', views.DeleteCatView.as_view(), name='delete_cat'),
	url(r'^subjects/(?P<slug>[\w_-]+)/$', views.SubjectsView.as_view(), name='view_subject'),
	url(r'^subjects/create/(?P<slug>[\w_-]+)/$', views.CreateSubjectView.as_view(), name='create_subject'),
	url(r'^subjects/update/(?P<slug>[\w_-]+)/$', views.UpdateSubjectView.as_view(), name='update_subject'),
	url(r'^subjects/delete/(?P<slug>[\w_-]+)/$', views.DeleteSubjectView.as_view(), name='delete_subject'),
	url(r'^topics/create/(?P<slug>[\w_-]+)/$', views.CreateTopicView.as_view(), name='create_topic'),
	url(r'^topics/update/(?P<slug>[\w_-]+)/$', views.UpdateTopicView.as_view(), name='update_topic'),
	url(r'^topics/(?P<slug>[\w_-]+)/$', views.TopicsView.as_view(), name='view_topic'),
	url(r'^subjects/categories$',views.IndexSubjectCategoryView.as_view(), name='subject_category_index'),
	url(r'^topics/update/(?P<slug>[\w_-]+)/createlink/', include('links.urls',namespace='links')),
	url(r'^forum/', include('forum.urls', namespace = 'forum')),
	url(r'^poll/', include('poll.urls', namespace = 'poll')),

]
