import xml.etree.ElementTree as ET
from datetime import datetime
from pytz import timezone
import pytz

tree = ET.parse('sample1.xml')
root = tree.getroot()

#for child in root:
#    print child.tag, child.attrib

for source in root.findall('Source'):
    ts = source.find('TimeStamp').text
    ip = source.find('IP_Address').text
    #print ip
    print 'Old Timestamp: ' + ts

str_breakdown = ts.replace('.0', '').replace('GMT', '').replace('-', ' ').replace(' ', ':').split(':')

gmt = pytz.timezone('GMT')
eastern = pytz.timezone('US/Eastern')
utc = pytz.utc
utc.zone
eastern.zone
fmt = '%Y-%m-%d %H:%M:%S.0 %Z'
loc_dt = utc.localize(datetime(int(str_breakdown[0]), int(str_breakdown[1]), int(str_breakdown[2]), int(str_breakdown[3]) + 1, int(str_breakdown[4]), int(str_breakdown[5])))
dateeastern = loc_dt.astimezone(eastern)
ret = dateeastern.strftime(fmt)
print 'New Timestamp: ' + ret

for source in root.findall('Source'):
    source.find('TimeStamp').text = ret

tree.write('sample1.xml')
print "Replaced Old Timestamp with New Timestamp"
