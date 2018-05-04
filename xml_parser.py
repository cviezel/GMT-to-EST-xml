import xml.etree.ElementTree as ET
from datetime import datetime
from pytz import timezone
import pytz
import time

# allows for parsing of xml file
tree = ET.parse('sample1.xml')
root = tree.getroot()

'''
for child in root:
    print child.tag, child.attrib
'''

#going through the xml file and setting variable ts to timestamp text and ip to the ip address as a string
for source in root.findall('Source'):
    ts = source.find('TimeStamp').text
    ip = source.find('IP_Address').text
    #print ip
    print 'Old Timestamp: ' + ts

#breaking the timestamp into an array of different values
str_breakdown = ts.replace('.0', '').replace('GMT', '').replace('-', ' ').replace(' ', ':').split(':')

#using pytz library to specify the different timezones we will use
gmt = pytz.timezone('GMT')
eastern = pytz.timezone('US/Eastern')
utc = pytz.utc
utc.zone
eastern.zone

#creating the format modifier
fmt = '%Y-%m-%d %H:%M:%S.0 %Z'

year = int(str_breakdown[0])
month = int(str_breakdown[1])
day = int(str_breakdown[2])
hour = int(str_breakdown[3])
minute = int(str_breakdown[4])
second = int(str_breakdown[5])

#adds an hour to the time if in correct time of year
if (time.localtime().tm_isdst):
    hour = hour + 1

#converting timestamp from gmt to eastern
loc_dt = utc.localize(datetime(year, month, day, hour, minute, second))
dateeastern = loc_dt.astimezone(eastern)

#ret is return value
ret = dateeastern.strftime(fmt)
print 'New Timestamp: ' + ret

#debug info
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

#modifying pytz time format into splunk's time format
new_date = ret.replace('.0', '').replace('GMT', '').replace('-', ' ').replace(' ', ':').split(':')


#subtracting a day to get yesterday
month = int(new_date[1])
day = int(new_date[2])
if(day == 1):
    if(month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
        yesterday = 31
    elif(month == 4 or month == 6 or month == 9 or month == 11):
        yesterday = 30
    elif(month == 2):
        yesterday = 28
else:
    yesterday = day-1

#creating earliest timestamp
new_ret = str(month) + "/" + str(yesterday) + "/" + new_date[0] + ":" + new_date[3] + ":" + new_date[4] + ":" + new_date[5]
data2 = ET.Element('Earliest_Timestamp')
data2.text = new_ret

#creating latest timestamp
new_ret2 = str(month) + "/" + str(day) + "/" + new_date[0] + ":" + new_date[3] + ":" + new_date[4] + ":" + new_date[5]
data3 = ET.Element('Latest_Timestamp')
data3.text = new_ret2

# create a new XML file with the results
mydata1 = ET.tostring(data1)
mydata2 = ET.tostring(data2)
mydata3 = ET.tostring(data3)
myfile = open("output.xml", "w")

myfile.write(mydata1)
myfile.write("\n")
myfile.write(mydata2)
myfile.write("\n")
myfile.write(mydata3)

print "Splunk-Formatted IP Address and Timestamp written to output.xml"
