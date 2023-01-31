import re



data = '<35>Aug 11 10:11:12|FG100E|Ping.(Ping)|Down.(before:.Down.(Partial))|.(The.sensor.shows.a.Down.status.because.of.a.simulated.error..To.resolve.this.issue,.right-click.the.sensor.and.select."Resume".from.the.context.menu..(code:.PE034))|Sensor.:.|15439'

values = dict()

header_re = r'(.*(?<!\\)\|){,7}(.*)'
res = re.search(header_re, data)

if res:
    header = res.group(1)
    extension = res.group(2)

    spl = re.split(r'(?<!\\)\|', header)

    values["test0"] = spl[0]
    values["test1"] = spl[1]
    values["test2"] = spl[2]
    values["test3"] = spl[3]
    values["test4"] = spl[4]
    if len(spl) > 6:
        values["DeviceSeverity"] = spl[6]


