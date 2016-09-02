from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib import messages
from rolepermissions.mixins import HasRoleMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from rolepermissions.shortcuts import assign_role
from .models import User
from .forms import UserForm, ProfileForm

class UsersListView(HasRoleMixin, LoginRequiredMixin, generic.ListView):
	
	allowed_roles = ['system_admin']
	login_url = '/'
	redirect_field_name = 'next'
	template_name = 'list_users.html'
	context_object_name = 'users'
	paginate_by = 10

	def get_queryset(self):
		users = User.objects.exclude(username = self.request.user.username)
		return users

class Create(HasRoleMixin, LoginRequiredMixin, generic.edit.CreateView):

	allowed_roles = ['system_admin']
	login_url = '/'
	redirect_field_name = 'next'
	template_name = 'users/create.html'
	form_class = UserForm
	context_object_name = 'acc'
	success_url = reverse_lazy('app:user:manage')

	def form_valid(self, form):
		self.object = form.save(commit = False)

		if self.object.type_profile == 2:
			assign_role(self.object, 'student')
		elif self.object.type_profile == 1:
			assign_role(self.object, 'professor')
		elif self.object.is_staff:
			assign_role(self.object, 'system_admin')

		self.object.save()

		messages.success(self.request, _('User created successfully!'))

		return super(Create, self).form_valid(form)

class Update(HasRoleMixin, LoginRequiredMixin, generic.UpdateView):

	allowed_roles = ['system_admin']
	login_url = '/'
	redirect_field_name = 'next'
	template_name = 'users/update.html'
	slug_field = 'username'
	slug_url_kwarg = 'username'
	context_object_name = 'acc'
	model = User
	form_class = UserForm
	success_url = reverse_lazy('app:users:manage')

	def form_valid(self, form):
		self.object = form.save(commit = False)
		
		if self.object.type_profile == 2:
			assign_role(self.object, 'student')
		elif self.object.type_profile == 1:
			assign_role(self.object, 'professor')
		elif self.object.is_staff:
			assign_role(self.object, 'system_admin')

		self.object.save()
		
		messages.success(self.request, _('User edited successfully!'))

		return super(Update, self).form_valid(form)
	
class View(LoginRequiredMixin, generic.DetailView):

	login_url = '/'
	redirect_field_name = 'next'
	model = User
	context_object_name = 'acc'
	template_name = 'users/view.html'
	slug_field = 'username'
	slug_url_kwarg = 'username'

class Profile(LoginRequiredMixin, generic.DetailView):

	login_url = '/'
	redirect_field_name = 'next'
	context_object_name = 'user'
	template_name = 'users/profile.html'

	def get_object(self):
		user = get_object_or_404(User, username = self.request.user.username)
		return user	

class EditProfile(LoginRequiredMixin, generic.UpdateView):

	login_url = '/'
	redirect_field_name = 'next'
	template_name = 'users/edit_profile.html'
	form_class = UserForm
	success_url = reverse_lazy('app:users:edit_profile')

	def get_object(self):
		user = get_object_or_404(User, username = self.request.user.username)
		return user

	def form_valid(self, form):
		self.object = form.save(commit = False)
		
		if self.object.type_profile == 2:
			assign_role(self.object, 'student')
		elif self.object.type_profile == 1:
			assign_role(self.object, 'professor')
		elif self.object.is_staff:
			assign_role(self.object, 'system_admin')

		self.object.save()

		messages.success(self.request, _('Profile edited successfully!'))

		return super(EditProfile, self).form_valid(form)