from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Q, DocType, Text, Date, Integer, Long, Object, Search, MultiSearch
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from django.utils import formats, timezone
from . import models

conn = connections.create_connection(hosts=['https://32ee85x1wy:p44kph0n9k@amadeus-elastic-6982239049.us-east-1.bonsaisearch.net'])

class LogIndex(DocType):    
    component = Text()
    action = Text()
    resource = Text()
    user = Text()
    user_id = Long()
    datetime = Date()
    context = Object()
    
    class Index:        
        name = 'log-index'

def bulk_indexing():
    LogIndex.init()

    es = Elasticsearch()

    logs = models.Log.objects.filter(datetime__date__gte = timezone.now() - timedelta(days = 7), datetime__date__lt = timezone.now()).all()

    bulk(client=es, actions=(b.indexing() for b in logs.iterator()))

def count_logs(resources, userid = 0):
    s = Search().extra(size=0)
    
    conds = []

    for res in resources:
        conds.append(Q('match', **{'context__' + res._my_subclass + '_id': res.id}))

    if userid != 0:
        s = s.query('bool', must=[Q("range", datetime={'gte': 'now-7d', 'lte': 'now-1d'}), Q("match", component="resources"), Q('bool', should=conds), Q('match', user_id=userid)])
    else:
        s = s.query('bool', must=[Q("range", datetime={'gte': 'now-7d', 'lte': 'now-1d'}), Q("match", component="resources"), Q('bool', should=conds)])

    return s

def resource_accessess(resource, userid = 0):
    s = Search().extra(size=0)

    if userid != 0:
        s = s.query('bool', must=[Q("range", datetime={'gte': 'now-7d', 'lte': 'now-1d'}), Q("match", component="resources"), Q('match', **{'context__' + resource._my_subclass + '_id': resource.id}), Q('match', user_id=userid)])
    else:
        s = s.query('bool', must=[Q("range", datetime={'gte': 'now-7d', 'lte': 'now-1d'}), Q("match", component="resources"), Q('match', **{'context__' + resource._my_subclass + '_id': resource.id})])

    return s

def user_last_interaction(userid):
    s = Search().extra(size=1)

    s = s.query("match", user_id=userid).sort("-datetime")

    return s

def multi_search(searchs):
    ms = MultiSearch(using=conn, index='log-index')

    for search in searchs:
        ms = ms.add(search)

    response = ms.execute()

    return response