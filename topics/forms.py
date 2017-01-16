# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from subjects.models import Subject

from .models import Topic

class TopicForm(forms.ModelForm):
	subject = None

	def __init__(self, *args, **kwargs):
		super(TopicForm, self).__init__(*args, **kwargs)

		self.subject = kwargs['initial'].get('subject', None)

	def clean_name(self):
		name = self.cleaned_data.get('name', '')
		repo = self.cleaned_data.get('repository', False)
		
		if len(self.subject.topic_subject.filter(name = name)) > 0:
			if repo:
				self._errors['name'] = [_('This subject already has a repository')]
			else:
				self._errors['name'] = [_('This subject already has a topic with this name')]

			return ValueError

		return name

	class Meta:
		model = Topic
		fields = ['repository', 'name', 'description', 'visible' ]
		widgets = {
			'description': forms.Textarea,
		}