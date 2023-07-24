import re

data = 'FG100E|Ping.(Ping)|Down.(before:.Down.(Partial))|.(The.sensor.shows.a.Down.status.because.of.a.simulated.error..To.resolve.this.issue,.right-click.the.sensor.and.select."Resume".from.the.context.menu..(code:.PE034))|Sensor.:.|15439'

values = dict()

header_re = r'(.*(?<!\\)\|){,7}(.*)'
res = re.search(header_re, data)

if res:
    header = res.group(1)
    extension = res.group(2)

    spl = re.split(r'(?<!\\)\|', header)

    values["device"] = spl[0]
    values["SensorName"] = spl[1]
    values["status"] = spl[2]
    values["message"] = spl[3]
    values["sensor"] = spl[4]
    values["sensori"] = spl[5]

    result = dict()

    for key in values.keys():
        result[key] = values[key]


    if len(spl) > 6:
        values["DeviceSeverity"] = spl[6]

    dictkey = values.values()

    for str in dictkey:
        print(str)


