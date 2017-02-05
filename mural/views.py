from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count

from users.models import User

from .models import GeneralPost, CategoryPost, SubjectPost, MuralVisualizations
from .forms import GeneralPostForm

class GeneralIndex(LoginRequiredMixin, generic.ListView):
	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'mural/list.html'
	model = GeneralPost
	context_object_name = "posts"
	paginate_by = 10

	totals = {}

	def get_queryset(self):
		user = self.request.user

		general = GeneralPost.objects.extra(select={"most_recent": "greatest(last_update, (select max(mural_comment.last_update) from mural_comment where mural_comment.post_id = mural_generalpost.mural_ptr_id))"}).order_by("-most_recent")
		
		self.totals['general'] = MuralVisualizations.objects.filter(Q(user = user) & Q(viewed = False) & (Q(post__generalpost__isnull = False) | Q(comment__post__generalpost__isnull = False))).distinct().count()
		self.totals['category'] = MuralVisualizations.objects.filter(Q(user = user) & Q(viewed = False) & (Q(post__categorypost__space__coordinators = user) | Q(comment__post__categorypost__space__coordinators = user) | Q(post__categorypost__space__subject_category__professor = user) | Q(post__categorypost__space__subject_category__students = user) | Q(comment__post__categorypost__space__subject_category__professor = user) | Q(comment__post__categorypost__space__subject_category__students = user))).distinct().count()
		self.totals['subject'] = MuralVisualizations.objects.filter(Q(user = user) & Q(viewed = False) & (Q(post__subjectpost__space__professor = user) | Q(comment__post__subjectpost__space__professor = user) | Q(post__subjectpost__space__students = user) | Q(comment__post__subjectpost__space__students = user))).distinct().count()

		return general

	def get_context_data(self, **kwargs):
		context = super(GeneralIndex, self).get_context_data(**kwargs)

		context['title'] = _('Mural')
		context['totals'] = self.totals
		context['mural_menu_active'] = 'subjects_menu_active'

		return context

class GeneralCreate(LoginRequiredMixin, generic.edit.CreateView):
	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'mural/_form.html'
	form_class = GeneralPostForm

	def form_invalid(self, form):
		context = super(GeneralCreate, self).form_invalid(form)
		context.status_code = 400

		return context

	def form_valid(self, form):
		self.object = form.save(commit = False)

		self.object.user = self.request.user

		self.object.save()

		users = User.objects.all().exclude(id = self.request.user.id)
		entries = []

		for user in users:
			entries.append(MuralVisualizations(viewed = False, user = user, post = self.object)) 

		MuralVisualizations.objects.bulk_create(entries)

		return super(GeneralCreate, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(GeneralCreate, self).get_context_data(*args, **kwargs)

		context['form_url'] = reverse_lazy("mural:create_general")

		return context

	def get_success_url(self):
		return reverse_lazy('mural:render_post_general', args = (self.object.id, ))

def render_gen_post(request, post):
	post = get_object_or_404(GeneralPost, id = post)

	context = {}
	context['post'] = post

	html = render_to_string("mural/_view.html", context, request)

	return JsonResponse({'message': _('Your post was published successfully!'), 'view': html})
