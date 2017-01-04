
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from categories.models import Category
from django.core.urlresolvers import reverse_lazy
from rolepermissions.verifications import has_role

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin

from rolepermissions.mixins import HasRoleMixin
from categories.forms import CategoryForm

from braces import views
from subjects.models import Subject

from log.mixins import LogMixin
from log.decorators import log_decorator_ajax
from log.models import Log

import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CreateSubjectForm
from users.models import User


class HomeView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("users:login")
    redirect_field_name = 'next'
    queryset = Subject.objects.all()
    template_name = 'subjects/initial.html'
    

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            subjects = Subject.objects.all()
        else:
            subjects = Subject.objects.all()
            subjects = [subject for subject in subjects if self.request.user in subject.students.all() or self.request.user in subject.professor.all()]
           
        paginator = Paginator(subjects, 2)

        page = self.request.GET.get('page')
        try:
            subjects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            subjects = paginator.page(1)

        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            subjects = paginator.page(paginator.num_pages)

        context['subjects'] = subjects
        return context


class IndexView(LoginRequiredMixin, ListView):

    login_url = reverse_lazy("users:login")
    redirect_field_name = 'next'
    queryset = Category.objects.all()
    template_name = 'subjects/list.html'
    context_object_name = 'categories'


    def get_queryset(self):
        result = super(IndexView, self).get_queryset()
        return result

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_staff:
            context['page_template'] = "categories/home_admin_content.html"
        else:
            context['page_template'] = "categories/home_teacher_student.html"

        context['title'] = _('Categories')

        if self.request.is_ajax():
            if self.request.user.is_staff:
                self.template_name = "categories/home_admin_content.html"
            else:
                self.template_name = "categories/home_teacher_student_content.html"

        return self.response_class(request = self.request, template = self.template_name, context = context, using = self.template_engine, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
             categories = self.get_queryset().order_by('name').filter(visible=True)
        else:
            if self.kwargs.get('option'):
                categories = self.get_queryset().order_by('name').filter(visible=True)
                context['all'] = True
                for category in categories:
                    category.subjects = Subject.objects.filter(category= category)
            else:
                context['all'] = False
                categories = self.get_queryset().filter(visible=True)
                for category in categories:
                    category.subjects = Subject.objects.filter(category= category)

                categories = [category for category in categories if category.subjects.count() > 0 or self.request.user in category.coordinators.all()] 
                #So I remove all categories that doesn't have the possibility for the user to be on
               
        
      
           
        
        context['categories'] = categories

        return context

class SubjectCreateView(CreateView):
    model = Subject
    template_name = "subjects/create.html"

    login_url = reverse_lazy('users:login')
    form_class = CreateSubjectForm
    
    success_url = reverse_lazy('subject:index')

    def get_initial(self):
        initial = super(SubjectCreateView, self).get_initial()
        initial['category'] = Category.objects.all().filter(slug=self.kwargs['slug'])
        
        return initial

    def get_context_data(self, **kwargs):
        context = super(SubjectCreateView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        context['template_extends'] = 'categories/list.html'
        return context
    def form_valid(self, form):
        
        self.object = form.save()
        self.object.category = Category.objects.get(slug=self.kwargs['slug'])
        self.object.save()
        

        return super(SubjectCreateView, self).form_valid(form)

    def get_success_url(self):

      
        objeto = self.object.name
        
        messages.success(self.request, _('Subject "%s" was registered on "%s" successfully!')%(objeto, self.kwargs['slug']))
        return reverse_lazy('subjects:index')


