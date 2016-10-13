from django.db import models
from django.utils.translation import ugettext_lazy as _

from courses.models import Activity

"""
	Function to return the path where the file should be saved
"""
def file_path(instance, filename):
	return '/'.join([instance.topic.subject.course.slug, instance.topic.subject.slug, instance.topic.slug, filename])


"""
	It's one kind of activity available for a Topic.
	It's like a support material for the students.
"""
class TopicFiles(Activity):
	file_url = models.FileField(verbose_name = _("File"), upload_to = file_path)

	class Meta:
		verbose_name = _("File")
		verbose_name_plural = _("Files")

	def __str__(self):
		return self.name