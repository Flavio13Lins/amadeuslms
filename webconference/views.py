from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from amadeus.permissions import has_subject_permissions, has_resource_permissions

import time
from log.models import Log
from log.mixins import LogMixin

from topics.models import Topic

from pendencies.forms import PendenciesForm

from .forms import WebconferenceForm
from .models import Webconference

class NewWindowView(LoginRequiredMixin,
 # '''LogMixin,'''
 generic.DetailView):
	# log_component = 'resources'
	# log_action = 'view'
	# log_resource = 'webpage'
	# log_context = {}

    login_url = reverse_lazy("users:login")
    redirect_field_name = 'next'

    template_name = 'webconference/window_view.html'
    model = Webconference
    context_object_name = 'webconference'

    def dispatch(self, request, *args, **kwargs):
    	slug = self.kwargs.get('slug', '')
    	webconference = get_object_or_404(Webconference, slug = slug)

    	if not has_resource_permissions(request.user, webconference):
    		return redirect(reverse_lazy('subjects:home'))

    	return super(NewWindowView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
    	context = super(NewWindowView, self).get_context_data(**kwargs)
    	context['title'] = _("%s - Web Conference")%(self.object.name)
    	# self.log_context['category_id'] = self.object.topic.subject.category.id
    	# self.log_context['category_name'] = self.object.topic.subject.category.name
    	# self.log_context['category_slug'] = self.object.topic.subject.category.slug
    	# self.log_context['subject_id'] = self.object.topic.subject.id
    	# self.log_context['subject_name'] = self.object.topic.subject.name
    	# self.log_context['subject_slug'] = self.object.topic.subject.slug
    	# self.log_context['topic_id'] = self.object.topic.id
    	# self.log_context['topic_name'] = self.object.topic.name
    	# self.log_context['topic_slug'] = self.object.topic.slug
    	# self.log_context['webpage_id'] = self.object.id
    	# self.log_context['webpage_name'] = self.object.name
    	# self.log_context['webpage_slug'] = self.object.slug
    	# self.log_context['timestamp_start'] = str(int(time.time()))

    	# super(NewWindowView, self).createLog(self.request.user, self.log_component, self.log_action, self.log_resource, self.log_context)
        #
    	# self.request.session['log_id'] = Log.objects.latest('id').id

    	return context

class Conference(LoginRequiredMixin,generic.TemplateView):

    login_url = reverse_lazy("users:login")
    redirect_field_name = 'next'

    template_name = 'webconference/jitsi.html'


    def get_context_data(self, **kwargs):
        context = super(Conference, self).get_context_data(**kwargs)
        context['name_room'] = kwargs.get('slug')
        context['user_image'] = 'http://localhost:8000'+str(self.request.user.image.url)
        return context

def saiu(request):
    url = {'url': 'http://localhost:8000' + str(reverse_lazy('webconferences:view', kwargs = {'slug': request.GET['roomName']}))}
    return JsonResponse(url, safe=False)


class InsideView(LoginRequiredMixin,
# '''LogMixin,'''
generic.DetailView):
	# log_component = 'resources'
	# log_action = 'view'
	# log_resource = 'webpage'
	# log_context = {}

	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'webconference/view.html'
	model = Webconference
	context_object_name = 'webconference'

	def dispatch(self, request, *args, **kwargs):
		slug = self.kwargs.get('slug', '')
		webconference = get_object_or_404(Webconference, slug = slug)

		if not has_resource_permissions(request.user, webconference):
			return redirect(reverse_lazy('subjects:home'))

		return super(InsideView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(InsideView, self).get_context_data(**kwargs)

		context['title'] = self.object.name

		context['topic'] = self.object.topic
		context['subject'] = self.object.topic.subject

		# self.log_context['category_id'] = self.object.topic.subject.category.id
		# self.log_context['category_name'] = self.object.topic.subject.category.name
		# self.log_context['category_slug'] = self.object.topic.subject.category.slug
		# self.log_context['subject_id'] = self.object.topic.subject.id
		# self.log_context['subject_name'] = self.object.topic.subject.name
		# self.log_context['subject_slug'] = self.object.topic.subject.slug
		# self.log_context['topic_id'] = self.object.topic.id
		# self.log_context['topic_name'] = self.object.topic.name
		# self.log_context['topic_slug'] = self.object.topic.slug
		# self.log_context['webpage_id'] = self.object.id
		# self.log_context['webpage_name'] = self.object.name
		# self.log_context['webpage_slug'] = self.object.slug
		# self.log_context['timestamp_start'] = str(int(time.time()))
        #
		# super(InsideView, self).createLog(self.request.user, self.log_component, self.log_action, self.log_resource, self.log_context)
        #
		# self.request.session['log_id'] = Log.objects.latest('id').id

		return context

class CreateView(LoginRequiredMixin,
 # '''LogMixin,'''
 generic.edit.CreateView):
	# log_component = 'resources'
	# log_action = 'create'
	# log_resource = 'webpage'
	# log_context = {}
    login_url = reverse_lazy("users:login")
    redirect_field_name = 'next'

    template_name = 'webconference/create.html'
    form_class = WebconferenceForm

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', '')
        topic = get_object_or_404(Topic, slug = slug)

        if not has_subject_permissions(request.user, topic.subject):
            return redirect(reverse_lazy('subjects:home'))
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        slug = self.kwargs.get('slug', '')
        topic = get_object_or_404(Topic, slug = slug)
        pendencies_form = PendenciesForm(initial = {'subject': topic.subject.id, 'actions': [("", "-------"),("view", _("Visualize"))]})
        return self.render_to_response(self.get_context_data(form = form, pendencies_form = pendencies_form))

    def post(self, request, *args, **kwargs):
        self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        slug = self.kwargs.get('slug', '')
        topic = get_object_or_404(Topic, slug = slug)

        pendencies_form = PendenciesForm(self.request.POST, initial = {'subject': topic.subject.id, 'actions': [("", "-------"),("view", _("Visualize"))]})

        if (form.is_valid() and pendencies_form.is_valid()):
            return self.form_valid(form, pendencies_form)
        else:
            return self.form_invalid(form, pendencies_form)

    def get_initial(self):
        initial = super(CreateView, self).get_initial()

        slug = self.kwargs.get('slug', '')

        topic = get_object_or_404(Topic, slug = slug)
        initial['subject'] = topic.subject

        return initial

    def form_invalid(self, form, pendencies_form):
        return self.render_to_response(self.get_context_data(form = form, pendencies_form = pendencies_form))

    def form_valid(self, form, pendencies_form):

        self.object = form.save(commit = False)
        slug = self.kwargs.get('slug', '')
        topic = get_object_or_404(Topic, slug = slug)

        self.object.topic = topic
        self.object.order = topic.resource_topic.count() + 1

        if not self.object.topic.visible and not self.object.topic.repository:
        	self.object.visible = False

        self.object.save()
        pend_form = pendencies_form.save(commit = False)
        pend_form.resource = self.object

        if not pend_form.action == "":
        	pend_form.save()

		# self.log_context['category_id'] = self.object.topic.subject.category.id
		# self.log_context['category_name'] = self.object.topic.subject.category.name
		# self.log_context['category_slug'] = self.object.topic.subject.category.slug
		# self.log_context['subject_id'] = self.object.topic.subject.id
		# self.log_context['subject_name'] = self.object.topic.subject.name
		# self.log_context['subject_slug'] = self.object.topic.subject.slug
		# self.log_context['topic_id'] = self.object.topic.id
		# self.log_context['topic_name'] = self.object.topic.name
		# self.log_context['topic_slug'] = self.object.topic.slug
		# self.log_context['webpage_id'] = self.object.id
		# self.log_context['webpage_name'] = self.object.name
		# self.log_context['webpage_slug'] = self.object.slug
        #
		# super(CreateView, self).createLog(self.request.user, self.log_component, self.log_action, self.log_resource, self.log_context)

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
    	context = super(CreateView, self).get_context_data(**kwargs)

    	context['title'] = _('Create Web Conference')

    	slug = self.kwargs.get('slug', '')
    	topic = get_object_or_404(Topic, slug = slug)

    	context['topic'] = topic
    	context['subject'] = topic.subject

    	return context

    def get_success_url(self):
    	messages.success(self.request, _('The Web conference "%s" was added to the Topic "%s" of the virtual environment "%s" successfully!')%(self.object.name, self.object.topic.name, self.object.topic.subject.name))

    	success_url = reverse_lazy('webconferences:view', kwargs = {'slug': self.object.slug})

    	if self.object.show_window:
    		self.request.session['resources'] = {}
    		self.request.session['resources']['new_page'] = True
    		self.request.session['resources']['new_page_url'] = reverse('webconferences:window_view', kwargs = {'slug': self.object.slug})

    		success_url = reverse_lazy('subjects:view', kwargs = {'slug': self.object.topic.subject.slug})

    	return success_url

class UpdateView(LoginRequiredMixin,
# ''' LogMixin,'''
generic.UpdateView):
	# log_component = 'resources'
	# log_action = 'update'
	# log_resource = 'webpage'
	# log_context = {}

	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'webconference/update.html'
	model = Webconference
	form_class = WebconferenceForm

	def dispatch(self, request, *args, **kwargs):
		slug = self.kwargs.get('topic_slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		if not has_subject_permissions(request.user, topic.subject):
			return redirect(reverse_lazy('subjects:home'))

		return super(UpdateView, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		slug = self.kwargs.get('topic_slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		pend_form = self.object.pendencies_resource.all()

		if len(pend_form) > 0:
			pendencies_form = PendenciesForm(instance = pend_form[0], initial = {'subject': topic.subject.id, 'actions': [("", "-------"),("view", _("Visualize"))]})
		else:
			pendencies_form = PendenciesForm(initial = {'subject': topic.subject.id, 'actions': [("", "-------"),("view", _("Visualize"))]})

		return self.render_to_response(self.get_context_data(form = form, pendencies_form = pendencies_form))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		slug = self.kwargs.get('topic_slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		pend_form = self.object.pendencies_resource.all()

		if len(pend_form) > 0:
			pendencies_form = PendenciesForm(self.request.POST, instance = pend_form[0], initial = {'subject': topic.subject.id, 'actions': [("", "-------"),("view", _("Visualize"))]})
		else:
			pendencies_form = PendenciesForm(self.request.POST, initial = {'subject': topic.subject.id, 'actions': [("", "-------"),("view", _("Visualize"))]})

		if (form.is_valid() and pendencies_form.is_valid()):
			return self.form_valid(form, pendencies_form)
		else:
			return self.form_invalid(form, pendencies_form)

	def form_invalid(self, form, pendencies_form):
		return self.render_to_response(self.get_context_data(form = form, pendencies_form = pendencies_form))

	def form_valid(self, form, pendencies_form):
		self.object = form.save(commit = False)

		if not self.object.topic.visible and not self.object.topic.repository:
			self.object.visible = False

		self.object.save()

		pend_form = pendencies_form.save(commit = False)
		pend_form.resource = self.object

		if not pend_form.action == "":
			pend_form.save()

		# self.log_context['category_id'] = self.object.topic.subject.category.id
		# self.log_context['category_name'] = self.object.topic.subject.category.name
		# self.log_context['category_slug'] = self.object.topic.subject.category.slug
		# self.log_context['subject_id'] = self.object.topic.subject.id
		# self.log_context['subject_name'] = self.object.topic.subject.name
		# self.log_context['subject_slug'] = self.object.topic.subject.slug
		# self.log_context['topic_id'] = self.object.topic.id
		# self.log_context['topic_name'] = self.object.topic.name
		# self.log_context['topic_slug'] = self.object.topic.slug
		# self.log_context['webpage_id'] = self.object.id
		# self.log_context['webpage_name'] = self.object.name
		# self.log_context['webpage_slug'] = self.object.slug
        #
		# super(UpdateView, self).createLog(self.request.user, self.log_component, self.log_action, self.log_resource, self.log_context)

		return redirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(UpdateView, self).get_context_data(**kwargs)

		context['title'] = _('Update Web Conference')

		slug = self.kwargs.get('topic_slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		context['topic'] = topic
		context['subject'] = topic.subject

		return context

	def get_success_url(self):
		messages.success(self.request, _('The Web conference "%s" was updated successfully!')%(self.object.name))

		success_url = reverse_lazy('webconferences:view', kwargs = {'slug': self.object.slug})

		if self.object.show_window:
			self.request.session['resources'] = {}
			self.request.session['resources']['new_page'] = True
			self.request.session['resources']['new_page_url'] = reverse('webconferences:window_view', kwargs = {'slug': self.object.slug})

			success_url = reverse_lazy('subjects:view', kwargs = {'slug': self.object.topic.subject.slug})

		return success_url

class DeleteView(LoginRequiredMixin,
# ''' LogMixin,'''
generic.DeleteView):
	# log_component = 'resources'
	# log_action = 'delete'
	# log_resource = 'webpage'
	# log_context = {}

	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'resources/delete.html'
	model = Webconference
	context_object_name = 'resource'

	def dispatch(self, request, *args, **kwargs):
		slug = self.kwargs.get('slug', '')
		webconference = get_object_or_404(Webconference, slug = slug)

		if not has_subject_permissions(request.user, webconference.topic.subject):
			return redirect(reverse_lazy('subjects:home'))

		return super(DeleteView, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		messages.success(self.request, _('The web conference "%s" was removed successfully from virtual environment "%s"!')%(self.object.name, self.object.topic.subject.name))

		# self.log_context['category_id'] = self.object.topic.subject.category.id
		# self.log_context['category_name'] = self.object.topic.subject.category.name
		# self.log_context['category_slug'] = self.object.topic.subject.category.slug
		# self.log_context['subject_id'] = self.object.topic.subject.id
		# self.log_context['subject_name'] = self.object.topic.subject.name
		# self.log_context['subject_slug'] = self.object.topic.subject.slug
		# self.log_context['topic_id'] = self.object.topic.id
		# self.log_context['topic_name'] = self.object.topic.name
		# self.log_context['topic_slug'] = self.object.topic.slug
		# self.log_context['webpage_id'] = self.object.id
		# self.log_context['webpage_name'] = self.object.name
		# self.log_context['webpage_slug'] = self.object.slug
        #
		# super(DeleteView, self).createLog(self.request.user, self.log_component, self.log_action, self.log_resource, self.log_context)

		return reverse_lazy('subjects:view', kwargs = {'slug': self.object.topic.subject.slug})