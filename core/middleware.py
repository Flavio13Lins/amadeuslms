from datetime import datetime
from django.shortcuts import get_object_or_404
import json

from core.models import Log

class TimeSpentMiddleware(object):
	def __init__(self, get_response = None):
		self.get_response = get_response

	def process_request(self, request):
		if not request.is_ajax():
			log_id = request.session.get('log_id', None)

			if not log_id is None:
				log = get_object_or_404(Log, id = log_id)

				date_time_click = datetime.strptime(request.session.get('time_spent'), "%Y-%m-%d %H:%M:%S.%f")
				_now = datetime.now()
				
				time_spent = _now - date_time_click
				
				secs = time_spent.total_seconds()
				hours = int(secs / 3600)
				minutes = int(secs / 60) % 60
				secs = secs % 60

				log_context = json.loads(log.context)

				log_context['time_spent'] = {}
				log_context['time_spent']['hours'] = hours
				log_context['time_spent']['minutes'] = minutes
				log_context['time_spent']['seconds'] = secs

				log.context = json.dumps(log_context)

				log.save()

				request.session['log_id'] = None

