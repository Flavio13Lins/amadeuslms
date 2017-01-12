from django.db import models
from django.utils.translation import ugettext_lazy as _

def validate_img_extension(value):
	valid_formats = ['image/jpeg','image/x-citrix-jpeg','image/png','image/x-citrix-png','image/x-png']
	
	if hasattr(value.file, 'content_type'):
		if not value.file.content_type in valid_formats:
			raise ValidationError(_('File not supported.'))

class Themes(models.Model):
	title = models.CharField(_("Title"), max_length = 200, default = "Projeto Amadeus")
	small_logo = models.ImageField(verbose_name = _("Small Logo"), blank = True, upload_to = 'themes/', default = 'logo_pequena_amadeus.png', validators = [validate_img_extension])
	large_logo = models.ImageField(verbose_name = _("Large Logo"), blank = True, upload_to = 'themes/', default = 'logo_grande_amadeus.png', validators = [validate_img_extension])
	footer_note = models.TextField(_("Footer Note"), blank = True)
	css_style = models.CharField(_("Css Style"), max_length = 50, default = "green", choices = (("green", _('Green')), ("red", _('Red')), ("black", _('Black'))))

	class Meta:
		verbose_name = _("Theme")
		verbose_name_plural = _("Themes")

	def __str__(self):
		return self.title
