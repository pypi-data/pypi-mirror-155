# -*- coding:utf-8 -*-
import datetime
import decimal
import json
import uuid
import numpy

from django.utils.duration import duration_iso_string
from django.utils.functional import Promise


class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types, and
    UUIDs.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):

            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        elif isinstance(o, (decimal.Decimal, uuid.UUID, Promise)):
            return str(o)
        elif isinstance(o, (numpy.float64, numpy.float32, numpy.float16)):
            return float(o)
        elif isinstance(o, (numpy.int0, numpy.int8, numpy.int16, numpy.int32)):
            return int(o)
        else:
            return super().default(o)

