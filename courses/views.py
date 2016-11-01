from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from rolepermissions.mixins import HasRoleMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from rolepermissions.verifications import has_role
from django.db.models import Q
import operator
from functools import reduce
from rolepermissions.verifications import has_object_permission
from django.http import HttpResponseRedirect, JsonResponse
from .forms import CourseForm, UpdateCourseForm, CategoryCourseForm, SubjectForm,TopicForm,ActivityForm
from .models import Course, Subject, CourseCategory,Topic, SubjectCategory,Activity, CategorySubject
from core.mixins import NotificationMixin
from users.models import User
from files.forms import FileForm
from files.models import TopicFile
from courses.models import Material
from django.urls import reverse

from datetime import date

class IndexView(LoginRequiredMixin, NotificationMixin, generic.ListView):

	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	queryset = Course.objects.all()
	template_name = 'course/index.html'
	context_object_name = 'courses'
	paginate_by = 10
	aparece = True


	def get_queryset(self):
		result = super(IndexView, self).get_queryset()

		course_search = self.request.GET.get('q', None)
		category_search = self.request.GET.get('category', None)
		if course_search:
			self.aparece = False
			query_list = course_search.split()
			result = result.filter(
			reduce(operator.and_,
				(Q(name__icontains=q) for q in query_list))
			)
		if category_search:
			self.aparece = False
			query_list = category_search.split()
			result = result.filter(
			reduce(operator.and_,
				(Q(category__name=category) for category in query_list))
			)
		return result

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		list_courses = None
		categorys_courses = None
		if has_role(self.request.user,'professor'):
			list_courses = Course.objects.filter(Q(professors = True)|Q(professors__name = self.request.user.name)).order_by('name')
			categorys_courses = CourseCategory.objects.filter(course_category__professors__name = self.request.user.name).distinct()
		elif has_role(self.request.user,'system_admin'):
			list_courses = queryset.order_by('name')
			categorys_courses = CourseCategory.objects.all()
		elif has_role(self.request.user, 'student'):
			list_courses = Course.objects.filter(Q(students = True)|Q(students__name = self.request.user.name)).order_by('name')
			categorys_courses = CourseCategory.objects.filter(course_category__students__name = self.request.user.name).distinct()

		paginator = Paginator(list_courses, self.paginate_by)
		page = self.request.GET.get('page')

		try:
		    list_courses = paginator.page(page)
		except PageNotAnInteger:
		    list_courses = paginator.page(1)
		except EmptyPage:
		    list_courses = paginator.page(paginator.num_pages)

		context['list_courses'] = list_courses
		context['categorys_courses'] = categorys_courses
		context['aparece'] = self.aparece

		return context

class AllCoursesView(LoginRequiredMixin, NotificationMixin, generic.ListView):

	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	queryset = Course.objects.all()
	template_name = 'course/index.html'
	context_object_name = 'courses'
	paginate_by = 5
	aparece = True


	def get_queryset(self):
		result = super(AllCoursesView, self).get_queryset()

		course_search = self.request.GET.get('q', None)
		category_search = self.request.GET.get('category', None)
		if course_search:
			self.aparece = False
			query_list = course_search.split()
			result = result.filter(
			reduce(operator.and_,
				(Q(name__icontains=q) for q in query_list))
			)
		if category_search:
			self.aparece = False
			query_list = category_search.split()
			result = result.filter(
			reduce(operator.and_,
				(Q(category__name=category) for category in query_list))
			)
		return result

	def get_context_data(self, **kwargs):
		context = super(AllCoursesView, self).get_context_data(**kwargs)
		list_courses = None
		categorys_courses = None
		list_courses = Course.objects.all().order_by('name')
		#categorys_courses = CourseCategory.objects.all().distinct().order_by('name')
		categorys_courses = CourseCategory.objects.all()
		paginator = Paginator(list_courses, self.paginate_by)
		page = self.request.GET.get('page')

		try:
		    list_courses = paginator.page(page)
		except PageNotAnInteger:
		    list_courses = paginator.page(1)
		except EmptyPage:
		    list_courses = paginator.page(paginator.num_pages)

		context['list_courses'] = list_courses
		context['categorys_courses'] = categorys_courses
		context['aparece'] = self.aparece

		return context
		
class CreateCourseView(LoginRequiredMixin, HasRoleMixin, NotificationMixin,generic.edit.CreateView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'course/create.html'
	form_class = CourseForm
	success_url = reverse_lazy('course:manage')

	def form_valid(self, form):
		self.object = form.save()
		self.object.professors.add(self.request.user)
		return super(CreateCourseView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(CreateCourseView, self).get_context_data(**kwargs)
		if has_role(self.request.user,'system_admin'):
			courses = Course.objects.all()
		elif has_role(self.request.user,'professor'):
			courses = self.request.user.courses_student.all()
		context['courses'] = courses
		context['title'] = _("Create Course")
		context['now'] = date.today()
		return context

class ReplicateCourseView(LoginRequiredMixin, HasRoleMixin, NotificationMixin,generic.edit.CreateView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'course/replicate.html'
	form_class = CourseForm
	success_url = reverse_lazy('course:manage')

	def form_valid(self, form):
		self.object = form.save()
		self.object.professors.add(self.request.user)
		return super(ReplicateCourseView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(ReplicateCourseView, self).get_context_data(**kwargs)
		course = get_object_or_404(Course, slug = self.kwargs.get('slug'))
		if has_role(self.request.user,'system_admin'):
			courses = Course.objects.all()
		elif has_role(self.request.user,'professor'):
			courses = self.request.user.courses_professors.all()
		categorys_courses = CourseCategory.objects.all()
		context['courses'] = courses
		context['course'] = course
		context['categorys_courses'] = categorys_courses
		context['title'] = _("Replicate Course")
		context['now'] = date.today()
		return context

	def get_success_url(self):
		return reverse_lazy('course:view', kwargs={'slug' : self.object.slug})

class UpdateCourseView(LoginRequiredMixin, HasRoleMixin, generic.UpdateView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'course/update.html'
	model = Course
	form_class = UpdateCourseForm

	def dispatch(self, *args, **kwargs):
		course = get_object_or_404(Course, slug = self.kwargs.get('slug'))
		if(not has_object_permission('update_course', self.request.user, course)):
			return self.handle_no_permission()
		return super(UpdateCourseView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(UpdateCourseView, self).get_context_data(**kwargs)
		course = get_object_or_404(Course, slug = self.kwargs.get('slug'))

		if has_role(self.request.user,'system_admin'):
			courses = Course.objects.all()
		elif has_role(self.request.user,'professor'):
			courses = self.request.user.courses.all()
		context['courses'] = courses
		context['title'] = course.name
		context['now'] = date.today()
		return context

	def get_success_url(self):
		return reverse_lazy('course:view', kwargs={'slug' : self.object.slug})

class DeleteCourseView(LoginRequiredMixin, HasRoleMixin, generic.DeleteView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	model = Course
	template_name = 'course/delete.html'
	success_url = reverse_lazy('course:manage')

	def dispatch(self, *args, **kwargs):
		course = get_object_or_404(Course, slug = self.kwargs.get('slug'))
		if(not has_object_permission('delete_course', self.request.user, course)):
			return self.handle_no_permission()
		return super(DeleteCourseView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(DeleteCourseView, self).get_context_data(**kwargs)
		course = get_object_or_404(Course, slug = self.kwargs.get('slug'))

		if has_role(self.request.user,'system_admin'):
			courses = Course.objects.all()
		elif has_role(self.request.user,'professor'):
			courses = self.request.user.courses.all()
		context['courses'] = courses
		context['title'] = course.name

		return context


class CourseView(NotificationMixin, generic.DetailView):

	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	model = Course
	context_object_name = 'course'
	template_name = 'course/view.html'

	def get_context_data(self, **kwargs):
		subjects = None
		courses = None
		context = super(CourseView, self).get_context_data(**kwargs)
		course = get_object_or_404(Course, slug = self.kwargs.get('slug'))

		category_sub = self.kwargs.get('category', None)

		if has_role(self.request.user,'system_admin'):
			subjects = course.subjects.all()
		elif has_role(self.request.user,'professor'):
			subjects = course.subjects.filter(professors__in=[self.request.user])
		elif has_role(self.request.user, 'student') or self.request.user is None:
			subjects = course.subjects.filter(visible=True)

		if not category_sub is None:
			cat = get_object_or_404(CategorySubject, slug = category_sub)
			subjects = subjects.filter(category = cat)
				
		context['subjects'] = subjects

		if has_role(self.request.user,'system_admin'):
			courses = Course.objects.all()
		elif has_role(self.request.user,'professor'):
			courses = self.request.user.courses_professors.all()
		elif has_role(self.request.user, 'student'):
			courses = self.request.user.courses_student.all()
		else:
			courses = Course.objects.filter(public = True)

		categorys_subjects = None
		if has_role(self.request.user,'professor') or has_role(self.request.user,'system_admin'):
			categorys_subjects = CategorySubject.objects.filter(subject_category__professors__name = self.request.user.name).distinct()
		elif has_role(self.request.user, 'student'):
			categorys_subjects = CategorySubject.objects.filter(subject_category__students__name = self.request.user.name).distinct()
		else:
			categorys_subjects = CategorySubject.objects.all().distinct()

		subjects_category = Subject.objects.filter(category__name = self.request.GET.get('category'))

		context['category'] = category_sub
		context['categorys_subjects'] = categorys_subjects
		context['courses'] = courses
		context['course'] = course
		context['title'] = course.name

		return context

class DeleteView(LoginRequiredMixin, HasRoleMixin, NotificationMixin, generic.DeleteView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	model = Course
	template_name = 'course/delete.html'
	success_url = reverse_lazy('course:manage')

	def render_to_response(self, context, **response_kwargs):
		messages.success(self.request, _('Course deleted successfully!'))

		return self.response_class(request=self.request, template=self.get_template_names(), context=context, using=self.template_engine)

@login_required
def subscribe_course(request, slug):
	course = get_object_or_404(Course, slug = slug)

	course.students.add(request.user)

	if request.user in course.students.all():
		return JsonResponse({"status": "ok", "message": _("Successfully subscribed to the course!")})
	else:
		return JsonResponse({"status": "erro", "message": _("An error has occured. Could not subscribe to this course, try again later")})

class FilteredView(LoginRequiredMixin, generic.ListView):

	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'course/filtered.html'
	context_object_name = 'courses'
	paginate_by = 3

	def get_queryset(self):
		category = get_object_or_404(CourseCategory, slug = self.kwargs.get('slug'))
		return Course.objects.filter(category = category)

	def get_context_data(self, **kwargs):
		category = get_object_or_404(CourseCategory, slug = self.kwargs.get('slug'))
		context = super(FilteredView, self).get_context_data(**kwargs)
		context['categories'] = CourseCategory.objects.all()
		context['cat'] = category

		return context

class IndexCatView(LoginRequiredMixin, generic.ListView):

	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	queryset = CourseCategory.objects.all()
	template_name = 'category/index.html'
	context_object_name = 'categories'
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super(IndexCatView, self).get_context_data(**kwargs)
		list_cat = CourseCategory.objects.filter(course_category = True).order_by('name')
		paginator = Paginator(list_cat, self.paginate_by)
		page = self.request.GET.get('page')

		try:
		    list_cat = paginator.page(page)
		except PageNotAnInteger:
		    list_cat = paginator.page(1)
		except EmptyPage:
		    list_cat = paginator.page(paginator.num_pages)

		context['list_cat'] = list_cat

		return context

class CreateCatView(LoginRequiredMixin, HasRoleMixin, generic.edit.CreateView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'category/create.html'
	form_class = CategoryCourseForm
	success_url = reverse_lazy('course:manage_cat')

	def get_success_url(self):
		messages.success(self.request, _('Category created successfully!'))
		return reverse_lazy('course:manage_cat')

class UpdateCatView(LoginRequiredMixin, HasRoleMixin, generic.UpdateView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'category/update.html'
	model = CourseCategory
	form_class = CategoryCourseForm

	def get_success_url(self):
		messages.success(self.request, _('Category updated successfully!'))
		return reverse_lazy('course:update_cat', kwargs={'slug' : self.object.slug})

class DeleteCatView(LoginRequiredMixin, HasRoleMixin, generic.DeleteView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	model = CourseCategory
	template_name = 'category/delete.html'

	def dispatch(self, *args, **kwargs):
		category = get_object_or_404(CourseCategory, slug = self.kwargs.get('slug'))
		if(not has_object_permission('delete_category', self.request.user, category)):
			return self.handle_no_permission()
		return super(DeleteCatView, self).dispatch(*args, **kwargs)


	def get_context_data(self, **kwargs):
		context = super(DeleteCatView, self).get_context_data(**kwargs)
		context['course'] = self.object.course_category
		context['category'] = self.object
		return context

	def get_success_url(self):
		messages.success(self.request, _('Category deleted successfully!'))
		return reverse_lazy('course:manage_cat')

class SubjectsView(LoginRequiredMixin, generic.ListView):

	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'subject/index.html'
	context_object_name = 'subjects'
	model = Subject

	def dispatch(self, *args, **kwargs):
		subject = get_object_or_404(Subject, slug = self.kwargs.get('slug'))

		if(not has_object_permission('view_subject', self.request.user, subject)):
			return self.handle_no_permission()

		return super(SubjectsView, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		subject = get_object_or_404(Subject, slug = self.kwargs.get('slug'))
		course = subject.course
		context = course.subjects.filter(visible=True)
		if (self.request.user in subject.professors.all() or has_role(self.request.user,'system_admin')):
			context = course.subjects.all()
		return context

	def get_context_data(self, **kwargs):

		context = super(SubjectsView, self).get_context_data(**kwargs)
		subject = get_object_or_404(Subject, slug = self.kwargs.get('slug'))
		context['course'] = subject.course
		context['subject'] = subject
		context['topics'] = Topic.objects.filter(subject = subject)
		if has_role(self.request.user,'professor') or has_role(self.request.user,'system_admin'):
			context['files'] = TopicFile.objects.filter(professor__name = self.request.user.name)
		else:
			context['files'] = TopicFile.objects.filter(students__name = self.request.user.name)
		return context

class UploadMaterialView(LoginRequiredMixin, generic.edit.CreateView):
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'

	template_name = 'files/create_file.html'
	form_class = FileForm

	def form_invalid(self, form):
		context = super(UploadMaterialView, self).form_invalid(form)
		context.status_code = 400

		return context

	def get_success_url(self):
		self.success_url = reverse('course:view_subject', args = (self.object.slug, ))

		return self.success_url

class TopicsView(LoginRequiredMixin, generic.ListView):

	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'topic/index.html'
	context_object_name = 'topics'
	model = Topic

	def dispatch(self, *args, **kwargs):
		topic = get_object_or_404(Topic, slug = self.kwargs.get('slug'))

		if(not has_object_permission('view_topic', self.request.user, topic)):
			return self.handle_no_permission()

		return super(TopicsView, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		topic = get_object_or_404(Topic, slug = self.kwargs.get('slug'))
		subject = topic.subject
		topics_q = Topic.objects.filter(subject = subject, visible=True)
		
		return topics_q

	def get_context_data(self, **kwargs):
		topic = get_object_or_404(Topic, slug = self.kwargs.get('slug'))
		context = super(TopicsView, self).get_context_data(**kwargs)
		activitys = Activity.objects.filter(topic__name = topic.name)
		students_activit = User.objects.filter(activities__in = Activity.objects.all())
		materials = Material.objects.filter(topic = topic)
		print(materials)
		context['topic'] = topic
		context['subject'] = topic.subject
		context['activitys'] = activitys
		context['students_activit'] = students_activit
		context['materials'] = materials
		context['form'] = ActivityForm
		
		return context


class CreateTopicView(LoginRequiredMixin, HasRoleMixin, NotificationMixin, generic.edit.CreateView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'topic/create.html'
	form_class = TopicForm

	def get_success_url(self):
		return reverse_lazy('course:view_subject', kwargs={'slug' : self.object.subject.slug})

	def get_context_data(self, **kwargs):
		context = super(CreateTopicView, self).get_context_data(**kwargs)
		subject = get_object_or_404(Subject, slug = self.kwargs.get('slug'))
		context['course'] = subject.course
		context['subject'] = subject
		context['subjects'] = subject.course.subjects.all()
		return context

	def form_valid(self, form):
		subject = get_object_or_404(Subject, slug = self.kwargs.get('slug'))

		self.object = form.save(commit = False)
		self.object.subject = subject
		self.object.owner = self.request.user
		self.object.save()
		action = super(CreateTopicView, self).createorRetrieveAction("create Topic")
		super(CreateTopicView, self).createNotification("Topic "+ self.object.name + " was created", 
			resource_name=self.object.name, resource_link= reverse('course:view_topic',args=[self.object.slug]),
			 actor=self.request.user, users = self.object.subject.course.students.all() )
		
		return super(CreateTopicView, self).form_valid(form)

class UpdateTopicView(LoginRequiredMixin, HasRoleMixin, generic.UpdateView):

	allowed_roles = ['professor','system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'topic/update.html'
	form_class = TopicForm

	def dispatch(self, *args, **kwargs):
		topic = get_object_or_404(Topic, slug = self.kwargs.get('slug'))
		if(not has_object_permission('edit_topic', self.request.user, topic)):
			return self.handle_no_permission()
		return super(UpdateTopicView, self).dispatch(*args, **kwargs)

	def get_object(self, queryset=None):
		return get_object_or_404(Topic, slug = self.kwargs.get('slug'))

	def get_success_url(self):
		return reverse_lazy('course:view_subject', kwargs={'slug' : self.object.subject.slug})

	def get_context_data(self, **kwargs):
		context = super(UpdateTopicView, self).get_context_data(**kwargs)
		topic = get_object_or_404(Topic, slug = self.kwargs.get('slug'))
		context['course'] = topic.subject.course
		context['subject'] = topic.subject
		context['subjects'] = topic.subject.course.subjects.filter(Q(visible=True) | Q(professors__in=[self.request.user]))
		if (has_role(self.request.user,'system_admin')):
			context['subjects'] = topic.subject.course.subjects.all()
		return context

class CreateSubjectView(LoginRequiredMixin, HasRoleMixin, NotificationMixin, generic.edit.CreateView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'subject/create.html'
	form_class = SubjectForm

	def get_success_url(self):
		return reverse_lazy('course:view_subject', kwargs={'slug' : self.object.slug})

	def get_context_data(self, **kwargs):
		context = super(CreateSubjectView, self).get_context_data(**kwargs)
		course = get_object_or_404(Course, slug = self.kwargs.get('slug'))
		context['course'] = course
		context['subjects'] = course.subjects.filter(Q(visible=True) | Q(professors__in=[self.request.user]))
		if (has_role(self.request.user,'system_admin')):
			context['subjects'] = course.subjects.all()
		return context

	def form_valid(self, form):
		course = get_object_or_404(Course, slug = self.kwargs.get('slug'))

		self.object = form.save(commit = False)
		self.object.course = course
		self.object.save()
		self.object.professors.add(self.request.user)
		if self.object.visible:
			super(CreateSubjectView, self).createNotification( " created subject " + self.object.name, resource_name=self.object.name,
			 resource_slug = self.object.slug, actor=self.request.user, users= self.object.course.students.all(),
			 resource_link = reverse('course:view_subject', args=[self.object.slug]))

		return super(CreateSubjectView, self).form_valid(form)


class UpdateSubjectView(LoginRequiredMixin, HasRoleMixin, generic.UpdateView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	template_name = 'subject/update.html'
	form_class = SubjectForm

	def dispatch(self, *args, **kwargs):
		subject = get_object_or_404(Subject, slug = self.kwargs.get('slug'))
		if(not has_object_permission('edit_subject', self.request.user, subject)):
			return self.handle_no_permission()
		return super(UpdateSubjectView, self).dispatch(*args, **kwargs)

	def get_object(self, queryset=None):
		context = get_object_or_404(Subject, slug = self.kwargs.get('slug'))
		return context

	def get_success_url(self):
		return reverse_lazy('course:view_subject', kwargs={'slug' : self.object.slug})

	def get_context_data(self, **kwargs):
		context = super(UpdateSubjectView, self).get_context_data(**kwargs)
		context['course'] = self.object.course
		context['subject'] = self.object
		context['subjects'] = self.object.course.subjects.filter(Q(visible=True) | Q(professors__in=[self.request.user]))
		if (has_role(self.request.user,'system_admin')):
			context['subjects'] = self.object.course.subjects.all()
		return context

class DeleteSubjectView(LoginRequiredMixin, HasRoleMixin, generic.DeleteView):

	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	model = Subject
	template_name = 'subject/delete.html'

	def dispatch(self, *args, **kwargs):
		subject = get_object_or_404(Subject, slug = self.kwargs.get('slug'))
		if(not has_object_permission('delete_subject', self.request.user, subject)):
			return self.handle_no_permission()
		return super(DeleteSubjectView, self).dispatch(*args, **kwargs)


	def get_context_data(self, **kwargs):
		context = super(DeleteSubjectView, self).get_context_data(**kwargs)
		context['course'] = self.object.course
		context['subject'] = self.object
		context['subjects'] = self.object.course.subjects.filter(Q(visible=True) | Q(professors__in=[self.request.user]))
		if (has_role(self.request.user,'system_admin')):
			context['subjects'] = self.object.course.subjects.all()
		return context

	def get_success_url(self):
		return reverse_lazy('course:view', kwargs={'slug' : self.object.course.slug})

@login_required
def subscribe_subject(request, slug):
	subject = get_object_or_404(Subject, slug = slug)

	if request.user in subject.course.students.all():
		subject.students.add(request.user)

		if request.user in subject.students.all():
			return JsonResponse({"status": "ok", "message": _("Successfully subscribed to the subject!")})
		else:
			return JsonResponse({"status": "erro", "message": _("An error has occured. Could not subscribe to this subject, try again later")})
	else:
		return JsonResponse({"status": "erro", "message": _("You're not subscribed in the course yet.")})

class IndexSubjectCategoryView(LoginRequiredMixin, generic.ListView):
	allowed_roles = ['professor', 'system_admin']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	model = SubjectCategory
	template_name = 'subject_category/index.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(IndexSubjectCategoryView, self).get_context_data(**kwargs)
		context['subject_categories'] = SubjectCategory.objects.all()
		return context

class FileMaterialView(LoginRequiredMixin, generic.DetailView):

	allowed_roles = ['professor', 'system_admin', 'student']
	login_url = reverse_lazy("core:home")
	redirect_field_name = 'next'
	model = Material
	context_object_name = 'file'
	template_name = 'topic/file_material_view.html'