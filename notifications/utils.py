from datetime import date
from django.utils import timezone
from django.db.models import Q
from dateutil.parser import parse

from log.models import Log
from pendencies.models import Pendencies
from users.models import User

from .models import Notification

def get_resource_users(resource):
	if resource.all_students:
		return resource.topic.subject.students.all()

	return User.objects.filter(Q(resource_students = resource) | Q(group_participants__resource_groups = resource)).distinct()

def set_notifications():
	pendencies = Pendencies.objects.filter(begin_date__date__lte = timezone.now(), resource__visible = True)

	for pendency in pendencies:
		users = get_resource_users(pendency.resource)
		subject_begin_date = pendency.resource.topic.subject.init_date
		pend_action = pendency.action
		resource_type = pendency.resource._my_subclass
		resource_key = resource_type + "_id"
		resource_id = pendency.resource.id

		for user in users:
			prev_notify = Notification.objects.filter(user = user, task = pendency).order_by("-creation_date")
			notify_type = 1
			meta = None

			if prev_notify.count() > 0:
				last_notify = prev_notify[0]

				if last_notify.creation_date == date.today():
					continue

				if last_notify.meta:
					if last_notify.creation_date < date.today() < last_notify.meta.date():
						continue

					meta = last_notify.meta
					notify_type = 2

			has_action = Log.objects.filter(user_id = user.id, action = pend_action, resource = resource_type, context__contains = {resource_key: resource_id}, datetime__date__gte = subject_begin_date).exists()

			if not has_action:
				if pendency.end_date:
					if timezone.now() > pendency.end_date:
						notify_type = 3

				if pendency.limit_date:
					if timezone.now() > pendency.limit_date:
						notify_type = 4
				
				notification = Notification()
				notification.user = user
				notification.level = notify_type
				notification.task = pendency
				notification.meta = meta

				notification.save()

def get_order_by(order):
	if not order:
		return ["-creation_date"]

	if "creation_date" in order:
		if "-" in order:
			return ["-creation_date"]
		else:
			return ["creation_date"]
	elif "resource" in order:
		if "-" in order:
			return ["-task__resource__name"]
		else:
			return ["task__resource__name"]
	elif "task" in order:
		if "-" in order:
			return ["-task__action"]
		else:
			return ["task__action"]
	elif "final_date" in order:
		if "-" in order:
			return ["-task__limit_date", "-task__end_date"]
		else:
			return ["task__limit_date", "task__end_date"]
	elif "notification" in order:
		if "-" in order:
			return ["-level"]
		else:
			return ["level"]
	elif "obs" in order:
		if "-" in order:
			return ["-meta"]
		else:
			return ["meta"]

def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False