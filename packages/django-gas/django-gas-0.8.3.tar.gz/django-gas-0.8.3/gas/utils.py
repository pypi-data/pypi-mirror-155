import datetime
import json

from django.db.models import QuerySet
from django.utils.functional import Promise


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, QuerySet):
            return list(obj)
        if isinstance(obj, Promise):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
