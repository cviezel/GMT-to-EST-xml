import xml.etree.ElementTree as ET
from datetime import datetime
from pytz import timezone
import pytz
import time

tree = ET.parse('sample1.xml')
root = tree.getroot()

'''
for child in root:
    print child.tag, child.attrib
'''

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
hour = int(str_breakdown[3])
if (time.localtime().tm_isdst):
    hour = hour + 1
loc_dt = utc.localize(datetime(int(str_breakdown[0]), int(str_breakdown[1]), int(str_breakdown[2]), hour, int(str_breakdown[4]), int(str_breakdown[5])))
dateeastern = loc_dt.astimezone(eastern)
ret = dateeastern.strftime(fmt)
print 'New Timestamp: ' + ret

'''
for source in root.findall('Source'):
    source.find('TimeStamp').text = ret

for source in root.find('Content'):
    source.find('TimeStamp').text = ret


tree.write('sample1.xml')
print "Replaced Old Timestamp with New Timestamp"

'''

# create the file structure
data1 = ET.Element('IP_Address')
data1.text = ip
data2 = ET.Element('Timestamp')
data2.text = ret

# create a new XML file with the results
mydata1 = ET.tostring(data1)
mydata2 = ET.tostring(data2)
myfile = open("output.xml", "w")
myfile.write(mydata1)
myfile.write("\n")
myfile.write(mydata2)

print "IP Address and Timestamp written to output.xml"
