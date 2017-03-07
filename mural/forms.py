# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.db.models import Q

from topics.models import Resource

from .models import GeneralPost, CategoryPost, SubjectPost, Comment

class Validation(forms.ModelForm):
	MAX_UPLOAD_SIZE = 5*1024*1024

	def clean_post(self):
		post = self.cleaned_data.get('post', '')
		cleaned_post = strip_tags(post)

		if cleaned_post == '':
			self._errors['post'] = [_('This field is required.')]

			return ValueError

		return post

	def clean_image(self):
		image = self.cleaned_data.get('image', False)

		if image:
			if hasattr(image, '_size'):
				if image._size > self.MAX_UPLOAD_SIZE:
					self._errors['image'] = [_("The image is too large. It should have less than 5MB.")]

					return ValueError

		return image

class GeneralPostForm(Validation):
	class Meta:
		model = GeneralPost
		fields = ['action', 'post', 'image']
		widgets = {
			'action': forms.RadioSelect,
			'post': forms.Textarea,
			'image': forms.ClearableFileInput(attrs={'accept':'image/*'}),
		}

class CategoryPostForm(Validation):
	class Meta:
		model = CategoryPost
		fields = ['action', 'post', 'image']
		widgets = {
			'action': forms.RadioSelect,
			'post': forms.Textarea,
			'image': forms.ClearableFileInput(attrs={'accept':'image/*'}),
		}

class SubjectPostForm(Validation):
	def __init__(self, *args, **kwargs):
		super(SubjectPostForm, self).__init__(*args, **kwargs)

		user = kwargs['initial'].get('user', None)
		subject = kwargs['initial'].get('subject', None)

		if not kwargs['instance'] is None:
			subject = self.instance.space

		if user.is_staff:
			self.fields['resource'].choices = [(r.id, str(r)) for r in Resource.objects.filter(Q(topic__subject = subject))]
		else:
			self.fields['resource'].choices = [(r.id, str(r)) for r in Resource.objects.filter(Q(topic__subject = subject) & (Q(all_students = True) | Q(students = user) | Q(groups__participants = user)))]

		self.fields['resource'].choices.append(("", _("Choose an especific resource")))

	class Meta:
		model = SubjectPost
		fields = ['action', 'resource', 'post', 'image']
		widgets = {
			'action': forms.RadioSelect,
			'post': forms.Textarea,
			'image': forms.ClearableFileInput(attrs={'accept':'image/*'}),
		}

class ResourcePostForm(Validation):
	class Meta:
		model = SubjectPost
		fields = ['action', 'post', 'image']
		widgets = {
			'action': forms.RadioSelect,
			'post': forms.Textarea,
			'image': forms.ClearableFileInput(attrs={'accept':'image/*'}),
		}

class CommentForm(forms.ModelForm):
	MAX_UPLOAD_SIZE = 5*1024*1024

	def clean_comment(self):
		comment = self.cleaned_data.get('comment', '')
		cleaned_comment = strip_tags(comment)

		if cleaned_comment == '':
			self._errors['comment'] = [_('This field is required.')]

			return ValueError

		return comment

	def clean_image(self):
		image = self.cleaned_data.get('image', False)

		if image:
			if hasattr(image, '_size'):
				if image._size > self.MAX_UPLOAD_SIZE:
					self._errors['image'] = [_("The image is too large. It should have less than 5MB.")]

					return ValueError

		return image

	class Meta:
		model = Comment
		fields = ['comment', 'image']
		widgets = {
			'image': forms.ClearableFileInput(attrs={'accept':'image/*'}),
		}
