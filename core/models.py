from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User
# Create your models here.




class Action(models.Model):
    """
	It represents an Action on the program by a User such as "create post", 
	"visualize post", etc. It is supposed to be created everytime we want an aciton
    """

    name = models.CharField(_('Name'), max_length = 100)
    created_date = models.DateField(_('Created Date'), auto_now_add=True)
    

    def __init__(self, name):
    	self.name = name

    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"

    def __str__(self):
        pass
    

class Resource(models.Model):
    """
		It represents the resource where the action was applied on.
		Example: Pool was answered (Resource: Pool), PDF was visualized(Resource: PDF).
    """

    name = models.CharField(_('Name'), max_length =100)
    created_date = models.DateField(_('Created Date'), auto_now_add=True)
    
    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"    

    def __str__(self):
        pass	


class Action_Resource(models.Model):
    
    action = models.ForeignKey(Action , verbose_name= _('Action_Applied'))
    resource = models.ForeignKey(Resource, verbose_name = _('Resource'))
    
    class Meta:
        verbose_name = "Action_Resource"
        verbose_name_plural = "Action_Resources"

    def __str__(self):
        pass
    

class Notification(models.Model):
    message = models.TextField(_('message'))
    user = models.ForeignKey(User, verbose_name= _('Actor'))
    read = models.BooleanField(_('Read'), default=False)
    action_resource = models.ForeignKey(Action_Resource, verbose_name = _('Action_Resource'))

    class Meta:
        verbose_name = "Action_Resource"
        verbose_name_plural = "Action_Resources"

    def __str__(self):
        pass
