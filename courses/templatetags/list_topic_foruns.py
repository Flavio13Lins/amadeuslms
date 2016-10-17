from django import template

from forum.models import Forum
from poll.models import Poll
from files.models import TopicFile
register = template.Library()

"""
 Template tag to load all the foruns of a post
"""

@register.inclusion_tag('topic/list_topic_foruns.html')
def list_topic_foruns(request, topic):
    context = {
        'request': request,
    }

    context['foruns'] = Forum.objects.filter(topic = topic)

    return context

@register.inclusion_tag('subject/poll_item_actions.html')
def list_topic_poll(request, topic):
    context = {
        'request': request,
    }

    context['polls'] = Poll.objects.filter(topic = topic)
    context['topic'] = topic

    return context

@register.inclusion_tag('topic/list_file.html')
def list_topic_file(request, topic):
    context = {
        'request': request,
    }

    context['files'] = TopicFile.objects.filter(topic = topic)
    context['topic'] = topic

    return context

@register.inclusion_tag('topic/list_file_edit.html')
def list_topic_file_edit(request, topic):
    context = {
        'request': request,
    }

    context['files'] = TopicFile.objects.filter(topic = topic)
    context['topic'] = topic

    return context
