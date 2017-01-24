from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from os import path
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from amadeus.permissions import has_subject_permissions, has_resource_permissions

from topics.models import Topic

from pendencies.forms import PendenciesForm

from .forms import FileLinkForm
from .models import FileLink

class DownloadFile(LoginRequiredMixin, generic.DetailView):
	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	model = FileLink

	def dispatch(self, request, *args, **kwargs):
		slug = self.kwargs.get('slug', '')
		file_link = get_object_or_404(FileLink, slug = slug)

		if not has_resource_permissions(request.user, file_link):
			return redirect(reverse_lazy('subjects:home'))

		return super(DownloadFile, self).dispatch(request, *args, **kwargs)

	def render_to_response(self, context, **response_kwargs):
		slug = self.kwargs.get('slug', '')
		file_link = get_object_or_404(FileLink, slug = slug)

		response = HttpResponse(open(file_link.file_content.path, 'rb').read())
		response['Content-Type'] = 'application/force-download'
		response['Pragma'] = 'public'
		response['Expires'] = '0'
		response['Cache-Control'] = 'must-revalidate, post-check=0, pre-check=0'
		response['Content-Disposition'] = 'attachment; filename=%s' % file_link.name
		response['Content-Transfer-Encoding'] = 'binary'
		response['Content-Length'] = str(path.getsize(file_link.file_content.path))
		
		return response

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'file_links/create.html'
	form_class = FileLinkForm

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

		self.object.show_window = True
		self.object.topic = topic
		self.object.order = topic.resource_topic.count() + 1

		if not self.object.topic.visible and not self.object.topic.repository:
			self.object.visible = False

		self.object.save()

		pend_form = pendencies_form.save(commit = False)
		pend_form.resource = self.object
		
		if not pend_form.action == "":
			pend_form.save() 
		
		return redirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(CreateView, self).get_context_data(**kwargs)

		context['title'] = _('Create File Link')

		slug = self.kwargs.get('slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		context['topic'] = topic
		context['subject'] = topic.subject

		return context

	def get_success_url(self):
		messages.success(self.request, _('The File Link "%s" was added to the Topic "%s" of the virtual environment "%s" successfully!')%(self.object.name, self.object.topic.name, self.object.topic.subject.name))

		return reverse_lazy('subjects:view', kwargs = {'slug': self.object.topic.subject.slug})