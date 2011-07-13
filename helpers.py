from google.appengine.api import users
from google.appengine.ext import db
import datetime
import time

def allmonths():
    return ['January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December',
            ]

def seasons():
    return {'Winter' : ['December', 'January', 'February'],
            'Spring' : ['March', 'April', 'May'],
            'Summer' : ['June', 'July', 'August'],
            'Fall'   : ['September', 'October', 'November'],
            }

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_dict(model):
    output = {}

    for key, prop in model.properties().iteritems():
        value = getattr(model, key)

        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            # Convert date/datetime to ms-since-epoch ("new Date()").
            ms = time.mktime(value.utctimetuple()) * 1000
            ms += getattr(value, 'microseconds', 0) / 1000
            output[key] = int(ms)
        elif isinstance(value, db.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output


def loginout_url(request):
    url = users.create_login_url(request.url)
    text = "Login"
    if users.is_current_user_admin():
        url = users.create_logout_url(request.url)
        text = "Logout"
    return {'loginout_url' : url,
            'loginout_txt' : text}

def uniq(seq, key=lambda x: x):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if key(x) not in seen and not seen_add(key(x))]

