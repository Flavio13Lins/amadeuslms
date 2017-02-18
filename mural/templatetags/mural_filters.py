from django import template
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from mural.models import MuralFavorites, MuralVisualizations

register = template.Library()

@register.filter(name = 'is_edited')
def is_edited(post):
	if post.edited:
		return _("(Edited)")

	return ""

@register.filter(name = 'action_icon')
def action_icon(action):
	icon = ""

	if action == "comment":
		icon = "fa-commenting-o"
	elif action == "help":
		icon = "fa-comments-o"

	return icon

@register.filter(name = 'fav_label')
def fav_label(post, user):
	if MuralFavorites.objects.filter(post = post, user = user).exists():
		return _('Unfavorite')

	return _('Favorite')

@register.filter(name = 'fav_action')
def fav_action(post, user):
	if MuralFavorites.objects.filter(post = post, user = user).exists():
		return "unfavorite"

	return "favorite"

@register.filter(name = 'fav_class')
def fav_class(post, user):
	if MuralFavorites.objects.filter(post = post, user = user).exists():
		return "btn_unfav"

	return "btn_fav"

@register.filter(name = 'unviewed')
def unviewed(category, user):
	count = MuralVisualizations.objects.filter(Q(user = user) & Q(viewed = False) & (Q(post__categorypost__space = category) | Q(comment__post__categorypost__space = category))).count()

	return count

@register.filter(name = 'sub_unviewed')
def sub_unviewed(subject, user):
	count = MuralVisualizations.objects.filter(Q(user = user) & Q(viewed = False) & (Q(post__subjectpost__space = subject) | Q(comment__post__subjectpost__space = subject))).count()

	return count

@register.filter(name = 'show_settings')
def show_settings(post, user):
	if user.is_staff:
		return True

	if post.user == user:
		return True

	if post._my_subclass == "categorypost":
		if user in post.categorypost.space.coordinators.all():
			return True

	if post._my_subclass == "subjectpost":
		if user in post.subjectpost.space.professor.all():
			return True

		if user in post.subjectpost.space.category.coordinators.all():
			return True

	return False

@register.filter(name = 'show_settings_comment')
def show_settings_comment(comment, user):
	if user.is_staff:
		return True

	if comment.user == user:
		return True

	if comment.post._my_subclass == "categorypost":
		if user in comment.post.categorypost.space.coordinators.all():
			return True

	if comment.post._my_subclass == "subjectpost":
		if user in comment.post.subjectpost.space.professor.all():
			return True

		if user in comment.post.subjectpost.space.category.coordinators.all():
			return True

	return False

@register.filter(name = 'has_resource')
def has_resource(post):
	if post._my_subclass == 'subjectpost':
		if post.subjectpost.resource:
			return _("about") + " <span class='post_resource'>" + str(post.subjectpost.resource) + "</span>"

	return ""