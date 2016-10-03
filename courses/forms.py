
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Category, Course, Subject, Topic


class CategoryForm(forms.ModelForm):

	class Meta:
		model = Category
		fields = ('name',)
		labels = {
			'name': _('Name')
		}
		help_texts = {
			'name': _('Category name')
		}


class CourseForm(forms.ModelForm):
	def clean_end_register_date(self):
		init_register_date = self.data['init_register_date']
		end_register_date = self.data['end_register_date']

		if init_register_date and end_register_date and end_register_date < init_register_date:
			raise forms.ValidationError(_('The end date may not be before the start date.'))
		return end_register_date

	def clean_init_date(self):
		end_register_date = self.data['end_register_date']
		init_date = self.data['init_date']

		if end_register_date and init_date and init_date <= end_register_date:
			raise forms.ValidationError(_('The course start date must be after the end of registration.'))
		return init_date

	def clean_end_date(self):
		init_date = self.data['init_date']
		end_date = self.data['end_date']

		if init_date and end_date and end_date < init_date:
			raise forms.ValidationError(_('The end date may not be before the start date.'))
		return end_date

	# init_register_date = forms.DateField(widget=forms.DateField)
	# end_register_date = forms.DateField(widget=forms.DateField)
	# init_date = forms.DateField(widget=forms.DateField)
	# end_date = forms.DateField(widget=forms.DateField)


	class Meta:
		model = Course
		fields = ('name', 'objectivies', 'content', 'max_students', 'init_register_date', 'end_register_date',
					'init_date', 'end_date', 'image', 'category',)
		labels = {
			'name': _('Name'),
			'objectivies': _('Objectives'),
			'content': _('Content'),
			'max_students': _('Number of studets maximum'),
			'init_register_date': _('Course registration start date'),
			'end_register_date': _('Course registration end date'),
			'init_date': _('Course start date'),
			'end_date': _('Course end date'),
			'image': _('Image'),
			'category': _('Category'),
		}
		help_texts = {
			'name': _('Course name'),
			'objectivies': _('Course objective'),
			'content': _('Course modules'),
			'max_students': _('Max number of students that a class can have'),
			'init_register_date': _('Date that starts the registration period of the course (dd/mm/yyyy)'),
			'end_register_date': _('Date that ends the registration period of the course (dd/mm/yyyy)'),
			'init_date': _('Date that the course starts (dd/mm/yyyy)'),
			'end_date': _('Date that the course ends (dd/mm/yyyy)'),
			'image': _('Representative image of the course'),
			'category': _('Category which the course belongs'),
		}

		widgets = {
			'categoy': forms.Select(),
			'objectivies': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
			'content': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
		}

class UpdateCourseForm(CourseForm):
	def __init__(self, *args, **kwargs):
		super(UpdateCourseForm, self).__init__(*args, **kwargs)
		self.fields["students"].required = False

	class Meta:
		model = Course
		fields = ('name', 'objectivies', 'content', 'max_students', 'init_register_date', 'end_register_date',
					'init_date', 'end_date', 'image', 'category','students',)
		labels = {
			'name': _('Name'),
			'objectivies': _('Objectives'),
			'content': _('Content'),
			'max_students': _('Number of studets maximum'),
			'init_register_date': _('Course registration start date'),
			'end_register_date': _('Course registration end date'),
			'init_date': _('Course start date'),
			'end_date': _('Course end date'),
			'image': _('Image'),
			'category': _('Category'),
			'students': _('Student'),
		}
		help_texts = {
			'name': _('Course name'),
			'objectivies': _('Course objective'),
			'content': _('Course modules'),
			'max_students': _('Max number of students that a class can have'),
			'init_register_date': _('Date that starts the registration period of the course (dd/mm/yyyy)'),
			'end_register_date': _('Date that ends the registration period of the course (dd/mm/yyyy)'),
			'init_date': _('Date that the course starts (dd/mm/yyyy)'),
			'end_date': _('Date that the course ends (dd/mm/yyyy)'),
			'image': _('Representative image of the course'),
			'category': _('Category which the course belongs'),
			'students': _("Course's Students"),
		}
		widgets = {
			'categoy': forms.Select(),
			'objectivies': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
			'content': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
		}

class SubjectForm(forms.ModelForm):

	class Meta:
		model = Subject
		fields = ('name', 'description', 'visible',)
		labels = {
			'name': _('Name'),
			'description': _('Description'),
			'visible': _('Is it visible?'),
		}
		help_texts = {
			'name': _("Subjects's name"),
			'description': _("Subjects's description"),
			'visible': _('Is the subject visible?'),
		}

class TopicForm(forms.ModelForm):

	class Meta:
		model = Topic
		fields = ('name', 'description',)
		labels = {
			'name': _('Name'),
			'description': _('Description'),
		}
		help_texts = {
			'name': _("Topic's name"),
			'description': _("Topic's description"),
		}

class ActivityFileForm(forms.ModelForm):
  name = forms.CharField(
            required=False,
            max_length=100,
            widget=forms.TextInput(attrs={
                'placeholder': 'Nome',
                'class': 'form-control'
              },
            )
          )
  pdf = forms.URLField(required=True, widget=S3DirectWidget(
       dest='activitys',
       html=(
           '<div class="s3direct" data-policy-url="{policy_url}">'
           '  <a class="file-link" target="_blank" href="{file_url}">{file_name}</a>'
           '  <a class="file-remove" href="#remove">Remover</a>'
           '  <input class="file-url" type="hidden" value="{file_url}" id="{element_id}" name="{name}" />'
           '  <input class="file-dest" type="hidden" value="{dest}">'
           '  <input class="file-input" type="file" />'
           '  <div class="progress">'
           '    <div class="progress-bar progress-bar-success progress-bar-striped active bar">'
           '    </div>'
           '  </div>'
           '</div>'
       )))

  class Meta:
    model = ActivityFile
    fields = ['pdf','name']

class ActivityForm(forms.ModelForm):  
  class Meta:
    model = Activity
    fields = ['id', 'user', 'stage']
