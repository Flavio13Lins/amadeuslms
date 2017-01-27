from django import template
import datetime
register = template.Library()

@register.filter(name = 'subject_count')
def subject_count(category, user):
	total = 0
	
	if not user.is_staff:
		for subject in category.subject_category.all():
			if user in subject.students.all() or user in subject.professor.all() or user in subject.category.coordinators.all():
				total += 1
	else:		
		total = category.subject_category.count()

	return total


@register.filter(name = 'aftertoday')
def after_today(date):
	if date > datetime.datetime.today().date():
		return True
	return False