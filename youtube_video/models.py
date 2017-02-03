from django.db import models
from django.utils.translation import ugettext_lazy as _

from topics.models import Resource

class YTVideo(Resource):
	url = models.URLField(_('URL'), max_length = 250)

	class Meta:
		verbose_name = _('YTVideo')
		verbose_name_plural = _('YTVideos')

	def __str__(self):
		return self.name

	def access_link(self):
		if self.show_window:
			return 'youtube:window_view'

		return 'youtube:view'

	def update_link(self):
		return 'youtube:update'

	def delete_link(self):
		return 'youtube:delete'

	def delete_message(self):
		return _('Are you sure you want delete the YouTube Video')

	def get_embed_url(self):
		if not "embed" in self.url:
			parts = self.url.split("=")

			if parts[1]:
				return "https://www.youtube.com/embed/" + parts[1]

		return self.url

