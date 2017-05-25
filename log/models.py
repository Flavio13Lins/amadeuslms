from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

class Log(models.Model):
	component = models.TextField(_('Component (Module / App)'))
	context = JSONField(_('Context'), blank = True)
	action = models.TextField(_('Action'))
	resource = models.TextField(_('Resource'))
	user = models.CharField(_('Actor'), max_length = 100)
	user_id = models.IntegerField(_('Actor id'))
	user_email = models.EmailField(_('Actor Mail'))
	datetime = models.DateTimeField(_("Date and Time of action"), auto_now_add = True)

	class Meta:
		verbose_name = _('Log')
		verbose_name_plural = _('Logs')

	def __str__(self):
		return str(self.user) + ' / ' + self.component