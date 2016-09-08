from django.conf import settings
from .models import Action, Resource, Action_Resource, Log, Notification

class LogMixin(object):
	log_action = ""
	log_resource = ""

	def dispatch(self, request, *args, **kwargs):
		action = Action.objects.filter(name = self.log_action)
		resource = Resource.objects.filter(name = self.log_resource)

		action_resource = Action_Resource.objects.filter(action = action, resource = resource)[0]

		log = Log()
		log.user = request.user
		log.action_resource = action_resource

		log.save()

		return super(LogMixin, self).dispatch(request, *args, **kwargs)



class NotificationMixin(object):
	message = ""
	read = False

	def dispatch(self, request, *args, **kwargs):
	    action = Action.objects.filter(name = self.log_action)
	    resource = Resource.objects.filter(name = self.log_resource)

	    action_resource = Action_Resource.objects.filter(action = action, resource = resource)[0]

	    notification = Notification()
	    notification.action_resource = action_resource
	    notification.user = request.user #We still have to handle the notification to be sent to an amount of Users

	    notification.read = read
	    notification.message = ""
	    


