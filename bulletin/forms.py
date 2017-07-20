# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags

from subjects.models import Tag

from .models import Bulletin

from resubmit.widgets import ResubmitFileWidget

class BulletinForm(forms.ModelForm):
    subject = None
    MAX_UPLOAD_SIZE = 1024*1024

    def __init__(self, *args, **kwargs):
        super(BulletinForm, self).__init__(*args, **kwargs)

        self.subject = kwargs['initial'].get('subject', None)

        if self.instance.id:
            self.subject = self.instance.topic.subject
            self.initial['tags'] = ", ".join(self.instance.tags.all().values_list("name", flat = True))

        self.fields['groups'].queryset = self.subject.group_subject.all()

    tags = forms.CharField(label = _('Tags'), required = False)

    class Meta:
        model = Bulletin
        fields = ['name', 'content', 'brief_description', 'all_students', 'groups', 'show_window', 'visible','file_content']
        labels = {
            'name': _('Bulletin name'),
            'content': _('Bulletin content'),
        }
        widgets = {
            'content': forms.Textarea,
            'brief_description': forms.Textarea,
            'groups': forms.SelectMultiple,
            'all_students': forms.HiddenInput(),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '')

        topics = self.subject.topic_subject.all()

        for topic in topics:
            if self.instance.id:
                same_name = topic.resource_topic.filter(name__unaccent__iexact = name).exclude(id = self.instance.id).count()
            else:
                same_name = topic.resource_topic.filter(name__unaccent__iexact = name).count()

            if same_name > 0:
                self._errors['name'] = [_('This subject already has a bulletin with this name')]

                return ValueError

        return name

    def clean_all_students(self):
        all_students = True
        return all_students
        

    def clean_file_content(self):
        file_content = self.cleaned_data.get('file_content', False)

        if file_content:
        	if hasattr(file_content, '_size'):
        		if file_content._size > self.MAX_UPLOAD_SIZE:
        			self._errors['file_content'] = [_("The file is too large. It should have less than 1MB.")]

        			return ValueError

        elif not self.instance.pk:
        	self._errors['file_content'] = [_('This field is required.')]

        	return ValueError

        return file_content

    def save(self, commit = True):
        super(BulletinForm, self).save(commit = True)

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

class FormModalMessage(forms.Form):
    MAX_UPLOAD_SIZE = 5*1024*1024

    comment = forms.CharField(widget=forms.Textarea,label=_("Message"))
    image = forms.FileField(widget=ResubmitFileWidget(attrs={'accept':'image/*'}),required=False)

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
