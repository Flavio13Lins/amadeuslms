from django.db import models
from autoslug.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from users.models import User

class Category(models.Model):
	"""Represents a Course """
	
	category_father = models.ForeignKey('Category', related_name =_("category_parent"), on_delete = models.CASCADE)
	name = models.CharField(_("Name"), max_length = 100)
	slug = AutoSlugField(_("Slug"),populate_from='name',unique=True)
	description = models.CharField(_("description"), max_length = 300)
	visible = models.BooleanField(_("visible"))
	coordinators = models.ManyToManyField(User, related_name = _("coordinators"))
	create_date = models.DateTimeField(_('Creation Date'), auto_now_add = True)
	modified_date = models.DateTimeField(_('Modified Date'), auto_now_add = True)

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')

	def __str__(self):
		return self.name