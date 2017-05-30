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

from categories.models import Category


from log.mixins import LogMixin
from log.decorators import log_decorator_ajax
from log.models import Log


class GeneralView(LogMixin, generic.TemplateView):
    template_name = "dashboards/general.html"

    log_component = "General_Dashboard"
    log_action = "view"
    log_resource = "General_Dashboard"
    log_context = {}

    def dispatch(self, request, *args, **kwargs):
       
        if not request.user.is_staff:
            return redirect('dashboards:view_categories')
        return super(GeneralView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = {}
        
        self.createLog(actor = self.request.user)
        context['months'] = self.get_last_twelve_months()
        context['child_template'] = "dashboards/general_body.html"
        context['javascript_files'] = ["analytics/js/charts.js", "dashboards/js/behavior.js"]
        return context

    def get_last_twelve_months(self):
        today = date.today()
        months = []
        month_mappings = { 1: _('January'), 2: _('February'), 3: _('March'), 4: _('April'), 5: _('May'), 6: _('June'), 7: _('July')
            , 8: _('August'), 9: _('September'), 10: _('October'), 11: _('November'), 12:  _('December')}
        date_used = today #the date used for solving the inital month problem
        offset = 0 #offset is the amount of weeks I had to shift so I could change the month if 4 weeks weren't enough
        for i in range(12):

            operation_date = today - timedelta(weeks= (4*i + offset))
            while date_used.month == operation_date.month:
                offset += 2
                operation_date = today - timedelta(weeks= (4*i + offset))

            months.append(month_mappings[date_used.month] + '/' + str(date_used.year))
            date_used = operation_date
        return months
    

class CategoryView(LogMixin, generic.TemplateView):
    template_name = "dashboards/category.html"
    
    log_component = "Category_Dashboard"
    log_action = "view"
    log_resource = "Category_Dashboard"
    log_context = {}

    def dispatch(self, request, *args, **kwargs):
        return super(CategoryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        self.createLog(actor = self.request.user)
        
        context['categories'] = self.categories_associated_with_user(self.request.user)
        context['javascript_files'] = ["analytics/js/charts.js", "dashboards/js/behavior.js"]
        
        return context

    def categories_associated_with_user(self, user):
        if user.is_staff:
            categories = Category.objects.all()
        else:
            categories = Category.objects.filter(coordinators__in = [user])
        return categories

class LogView(LogMixin, generic.TemplateView):
    template_name = "dashboards/general.html"

    log_component = "admin_log"
    log_action = "view"
    log_resource = "admin_log"
    log_context = {}

    def dispatch(self, request, *args, **kwargs):
        return super(LogView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        self.createLog(actor = self.request.user)
        
        context['javascript_files'] = ['dashboards/js/logbehavior.js']
        context['child_template'] = "dashboards/log.html"
        return context

    

def load_log_data(request):
    params = request.GET
    print(params)
    init_date = datetime.strptime(params['init_date'], '%Y-%m-%d %H:%M')

    end_date = datetime.strptime(params['end_date'], '%Y-%m-%d %H:%M')

    if params.get('category'):
        print("has category")
    logs = Log.objects.filter(datetime__range = (init_date, end_date) )
    logs = parse_log_queryset_to_JSON(logs)
    return JsonResponse(logs, safe=False)


def parse_log_queryset_to_JSON(logs):
    data = []
    for log in logs:
        datum = {}
        datum['user'] = log.user
        datum['resource'] = log.resource
        datum['datetime'] = log.datetime
        datum['action'] = log.action
        datum['context'] = log.context
        datum['component'] = log.component
        data.append(datum)
    return data