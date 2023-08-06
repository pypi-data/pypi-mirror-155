import datetime
import pytz

tz = pytz.timezone('Europe/Madrid')

def asUtc(date):
    """
    If date is a naive date, take it as being UTC.
    If date is local, converts to the equivalent UTC.
    """
    if date.tzinfo is None:
        return pytz.utc.localize(date)
    return date.astimezone(pytz.utc)

def toLocal(date):
    """
    If date is a naive date, take it as being Madrid TZ.
    If date is local, converts to the equivalent Madrid TZ.
    """
    if date.tzinfo is None:
        return tz.localize(date)
    return date.astimezone(tz)

def parseLocalTime(string, isSummer=False, format="%Y-%m-%d %H:%M:%S"):
    naive = datetime.datetime.strptime(string, format)
    localized = tz.localize(naive)
    if not isSummer: return localized
    if localized.dst(): return localized
    onehour = datetime.timedelta(hours=1)
    lesser = tz.normalize(localized-onehour)
    return lesser if lesser.dst() else localized

def localisodate(string):
    """Takes a date string and returns it as local datetime (time set to 00:00:00CET/CEST)"""
    return string and toLocal(naiveisodate(string))

def utcisodate(string):
    """Takes a date string and returns it as utc datetime (time set to 00:00:00Z)"""
    return string and asUtc(naiveisodate(string))

def naiveisodate(string):
    """Takes a date string and returns it as naive datetime (time set to 00:00:00, no TZ)"""
    return string and datetime.datetime.strptime(string, "%Y-%m-%d")

def isodate(string):
    """Takes a date string and returns it as date (no time)"""
    return string and naiveisodate(string).date()

def localisodatetime(string):
    """Takes a date-time string and returns a local (CET/CEST) datetime.
    Timezoned strings are converted, naive strings are interpreted.
    Be aware that naive strings (no time zone), might be ambiguous
    or ilegal on daylight time changes.
    """
    return string and toLocal(isodatetime(string))

def utcisodatetime(string):
    """Takes a date-time string and returns it as utc datetime.
    Timezoned strings are converted, naive strings are interpreted.
    """
    return string and asUtc(isodatetime(string))

def isodatetime(string):
    """Takes a time-zoned (or naive) iso date-time string and returns it as a datetime"""
    import dateutil.parser
    return string and dateutil.parser.isoparse(string)

def dateToLocal(date):
    # TODO: optimize dateToLocal
    return localisodate(str(date))

def assertDate(name, date):
    assert type(date)==datetime.date, (
        "{} should be a datetime.date but it is {}"
        .format(name, date))
    return date

def assertDateOrNone(name, date):
    if date is None: return date
    assert type(date)==datetime.date, (
        "{} should be a datetime.date or None but it is {}"
        .format(name, date))
    return date

def assertNaiveTime(name, date):
    assert type(date)==datetime.datetime, (
        "{} should be a datetime.datetime with no timezone (naive) but it is {}"
        .format(name, date))
    return date

def assertLocalDateTime(name, value):
    assert isinstance(value, datetime.datetime), (
        "{} should be a datetime".format(name))
    assert value.tzinfo, (
        "{} should have timezone".format(name))
    assert value.tzname() in ('CET','CEST'), (
        "{} has {} timezone".format(name, value.tzname()))

def assertUtcDateTime(name, value):
    assert isinstance(value, datetime.datetime), (
        "{} should be a datetime".format(name))
    assert value.tzinfo, (
        "{} should have timezone".format(name))
    assert value.tzname() == 'UTC', (
        "{} has {} timezone".format(name, value.tzname()))

def addHours(dt, hours):
    hours = datetime.timedelta(hours=hours)
    return tz.normalize(dt + hours)

def addDays(date, ndays):
    resultday = date.date() + datetime.timedelta(days=ndays)
    naiveday = datetime.datetime.combine(resultday, datetime.time(0,0,0))
    return toLocal(naiveday)

def daterange(first_date, last_date):
    """
    Generates dates from first_date to last_date, both included.
    Additional parameters provides paramenters for the
    timedelta constructor to be used as step.
    """
    for n in range(int ((last_date - first_date).days + 1)):
        yield first_date + n*datetime.timedelta(days=1)



