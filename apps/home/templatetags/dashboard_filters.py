from django import template
register = template.Library()

@register.filter()
def time_normalization(date):
    try:
        hour = str(date.hour) if len(str(date.hour)) > 1 else '0' + str(date.hour)
        minute = str(date.minute) if len(str(date.minute)) > 1 else '0' + str(date.minute)
        day = str(date.day) if len(str(date.day)) > 1 else '0' + str(date.day)
        month = str(date.month) if len(str(date.month)) > 1 else '0' + str(date.month)
        year = str(date.year)

        return day + '/' + month + '/' + year + ' ' + hour + ':' + minute
    except:

        return date

@register.filter()
def time_normalization2(date):
    print(date)
    try:
        datetime = date.split(' ')
        _date = datetime[0].split('-')
        time = datetime[1].split(':')
        hour = time[0]
        minute = time[1]
        day = _date[2]
        month = _date[1]
        year = _date[0]

        return day + '/' + month + '/' + year + ' ' + hour + ':' + minute
    except:

        return date

@register.filter()
def time_normalization_date(date):
    try:
        day = str(date.day) if len(str(date.day)) > 1 else '0' + str(date.day)
        month = str(date.month) if len(str(date.month)) > 1 else '0' + str(date.month)
        year = str(date.year)

        return day + '/' + month + '/' + year
    except:

        return date

@register.filter()
def datetime_to_timestamp(date):
    
    return date.replace(tzinfo=None)

@register.filter()
def validation_status(status):
    if status == 0:
        return 'Done'
    else:
        return f' Waiting ({status:,} rows)'

@register.filter()
def thousands_separators(value):
    try:
        return f'{int(value):,}'
    except:
        return ""

@register.filter()
def milisecond_to_minute(value):
    try:
        return f'{round(value / 60000, 2):,}'
    except:
        return ""
    
@register.filter()
def second_to_minute(value):
    try:
        return f'{round(value / 60, 2):,}'
    except:
        return ""

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg