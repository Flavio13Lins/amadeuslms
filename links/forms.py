# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError

from subjects.models import Tag
from subjects.forms import ParticipantsMultipleChoiceField

from pendencies.forms import PendenciesForm
from .models import Link

class LinkForm(forms.ModelForm):
	subject = None
	MAX_UPLOAD_SIZE = 10*1024*1024

	students = ParticipantsMultipleChoiceField(queryset = None)
	
	def __init__(self, *args, **kwargs):
		super(LinkForm, self).__init__(*args, **kwargs)

		self.subject = kwargs['initial'].get('subject', None)
		
		if self.instance.id:
			self.subject = self.instance.topic.subject
			self.initial['tags'] = ", ".join(self.instance.tags.all().values_list("name", flat = True))
		
		self.fields['students'].queryset = self.subject.students.all()
		self.fields['groups'].queryset = self.subject.group_subject.all()

	tags = forms.CharField(label = _('Tags'), required = False)
	link_url = forms.URLField(label = _('Website URL'),required=True)
	
	class Meta:
		model = Link
		fields = ['name','link_url', 'brief_description', 'all_students', 'students', 'groups', 'visible']
		labels = {
			'name': _('Link name'),
			'end_view' : _('End View'),
			'end_view_date': _('End View Date')
		}
		widgets = {
			'brief_description': forms.Textarea,
			'students': forms.SelectMultiple,
			'groups': forms.SelectMultiple,
		}

	def clean(self):

		cleaned_data = self.cleaned_data

	
		return cleaned_data
	

	def clean_name(self):
		name = self.cleaned_data.get('name', '')
		
		topics = self.subject.topic_subject.all()

		for topic in topics:
			if self.instance.id:
				same_name = topic.resource_topic.filter(name__unaccent__iexact = name).exclude(id = self.instance.id).count()
			else:
				same_name = topic.resource_topic.filter(name__unaccent__iexact = name).count()
		
			if same_name > 0:
				self._errors['name'] = [_('There is already a link with this name on this subject')]

				return ValueError

		return name


	

	def save(self, commit = True):
		super(LinkForm, self).save(commit = True)

		self.instance.save()

		previous_tags = self.instance.tags.all()

		tags = self.cleaned_data['tags'].split(",")

        #Excluding unwanted tags
		for prev in previous_tags:
			if not prev.name in tags:
				self.instance.tags.remove(prev)
        
		for tag in tags:
			tag = tag.strip()

			exist = Tag.objects.filter(name = tag).exists()

			if exist:
				new_tag = Tag.objects.get(name = tag)
			else:
				new_tag = Tag.objects.create(name = tag)

			if not new_tag in self.instance.tags.all():
				self.instance.tags.add(new_tag)

		return self.instance