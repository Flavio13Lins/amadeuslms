from django.shortcuts import render

from django.views import generic
from django.db.models import Count
from django.core.urlresolvers import reverse_lazy

from subjects.models import Tag, Subject
from topics.models import Resource
from users.models import User
from django.http import HttpResponse, JsonResponse
from log.models import Log
import operator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect

from datetime import date, timedelta, datetime
import calendar
from collections import OrderedDict


class GeneralView(generic.TemplateView):
    template_name = "analytics/general.html"

    def dispatch(self, request, *args, **kwargs):
       
        if not request.user.is_staff:
            return redirect('analytics:view_category_data')
        return super(GeneralView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = {}

        context['months'] = [_('January'), _('February'), _('March'), _('April'), _('May'), _('June'), _('July'), _('August'), 
        _('September'), _('October'), _('November'), _('December')]
        
        return context



def most_used_tags(request):
   

    data = get_most_used_tags()
    data = sorted(data.values(), key = lambda x: x['count'], reverse=True )
    data = data[:15] #get top 15 tags
    return JsonResponse(data, safe= False) 

def get_most_used_tags():

    tags = Tag.objects.all()
    data = {}
    #grab all references to that tag
    for tag in tags:
        subjects_count =  Subject.objects.filter(tags = tag).count()
        if  subjects_count > 0:
            data[tag.name] = {'name': tag.name}
            data[tag.name]['count'] = subjects_count

        resources_count = Resource.objects.filter(tags = tag).count()
        if resources_count > 0:
            if data.get(tag.name):
                data[tag.name]['count'] = data[tag.name]['count']  + resources_count
            else:
                data[tag.name] = {'name': tag.name}
                data[tag.name]['count'] = resources_count
    return data


def most_active_users_in_a_month(request):
    params = request.GET
    days = get_days_of_the_month(params['month'])
    mappings = {_('January'): 1, _('February'): 2, _('March'): 3, _('April'): 4, _('May'): 5, _('June'): 6, _('July'): 7
    , _('August'): 8, _('September'): 9, _('October'): 10, _('November'): 11, _('December'): 12}
    
    days_list = []
    for day in days:
        built_date = date(date.today().year, mappings[params['month']],  day)
        days_list.append(built_date)
    data = activity_in_timestamp(days_list)
    data = [{"day": day.day, "count": day_count} for day, day_count in data.items()]
    return JsonResponse(data, safe=False)


def activity_in_timestamp(days):
    data = {}
    for day in days:
        day_count = Log.objects.filter(datetime__date = day).count()
        data[day] = day_count

    return data
"""
Subject view that returns a list of the most used subjects     """


def most_accessed_subjects(request):
    data = {} #empty response

    data = Log.objects.filter(resource = 'subject')
    subjects = get_log_count_of_resource(resource='subject')
    #order the values of the dictionary by the count in descendent order
    subjects = sorted(subjects.values(), key = lambda x: x['count'], reverse=True )
    subjects = subjects[:5]

    return JsonResponse(subjects, safe=False)

def get_log_count_of_resource(resource = ''):

    data = Log.objects.filter(resource = resource)
    items = {}
    for datum in data:
        if datum.context:
            item_id = datum.context[resource + '_id']
            if item_id in items.keys():
                items[item_id]['count'] = items[item_id]['count'] + 1
            else:
                items[item_id] = {'name': datum.context[resource+'_name'], 'count': 1}
    return items


def most_accessed_categories(request):
    data = {}

    data = Log.objects.filter(resource = 'category')
    categories = get_log_count_of_resource('category')

   

    categories = sorted(categories.values(), key = lambda x: x['count'], reverse = True)
    categories = categories[:5]
    return JsonResponse(categories, safe= False)


def get_resource_subclasses_count():
    """
        get the amount of objects in each sub_class of resource
    """
    resources = Resource.objects.distinct()
    data = {}
    for resource in resources:
        key = resource.__dict__['_my_subclass']
        if key in data.keys():
            data[key]['count'] = data[key]['count'] + 1
        else:
            data[key] = {'name': key, 'count': 1}

    return data


def most_accessed_resource_kind(request):

    data = get_resource_subclasses_count()

    data = sorted(data.values(), key = lambda x: x['count'], reverse= True)
    mapping = {}
    mapping['pdffile'] = str(_('PDF File'))
    mapping['goals'] = str(_('Topic Goals'))
    mapping['link'] = str(_('Link to Website'))
    mapping['filelink'] = str(_('File Link'))
    mapping['webconference'] = str(_('Web Conference'))
    mapping['ytvideo'] = str(_('YouTube Video'))
    mapping['webpage'] = str(_('WebPage'))

    data = [ {'name': mapping[resource['name']] , 'count': resource['count']} for resource in data]
    data =  data[:5]
    return JsonResponse(data, safe=False)


def most_active_users(request):
    fifty_users = Log.objects.values('user_id').annotate(count = Count('user_id')).order_by('-count')[:50]
    fifty_users = list(fifty_users)
    for user in fifty_users:
        user_object = User.objects.get(id=user['user_id'])
        user['image'] = user_object.image_url
        user['user'] = user_object.social_name
    return JsonResponse(fifty_users, safe=False)




def get_days_of_the_month(month):
 
    #get current year
    year = date.today().year
    mappings = {_('January'): 1, _('February'): 2, _('March'): 3, _('April'): 4, _('May'): 5, _('June'): 6, _('July'): 7
    , _('August'): 8, _('September'): 9, _('October'): 10, _('November'): 11, _('December'): 12}
  
    c = calendar.Calendar()
    days = c.itermonthdays(year, mappings[month])
    days_set = set()
    for day in days:
        days_set.add(day)

    days_set.remove(0) #because 0 is not aan actual day from that month
    return days_set 



def get_days_of_the_week_log(request):
    date = request.GET['date']
    date = datetime.strptime( date, '%m/%d/%Y',)
    days = get_days_of_the_week(date)
    data = activity_in_timestamp(days)
    data = [{"day": day.day, "count": day_count} for day, day_count in data.items()]

    return JsonResponse(data, safe= False)

def get_days_of_the_week(date):

    days_set = []
    days_set.append(date)
    for j in range(1, 7):
        days_set.append(date + timedelta(days=j))
    return days_set


class CategoryView(generic.TemplateView):
    template_name = "analytics/category.html"
