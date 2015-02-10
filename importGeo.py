import sys, itertools
import re
import geoip2.database
import codecs
from collections import Counter

__author__ = "Rongbing Miao"


reader = geoip2.database.Reader('/root/devhomework/GeoLite2-City.mmdb')
y = []

## Regex for the input Apache log file
parts = [
    r'(?P<host>\S+)',                   # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',               # referer "%{Referer}i"
    r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
]
pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

'''
Ignore those requests for images, CSS and JavaScript.
..and ignore those paths ending with .css and .atom
'''
def notIgnored(hit):
    if '/css/' in hit.split()[1]:
        return False

    if  '/images/' in hit.split()[1]:
        return False

    if '/js/' in hit.split()[1]:
        return False

    if '/entry-images/' in hit.split()[1]:
        return False

    if '/user-images/' in hit.split()[1]:
        return False

    if '/static/' in hit.split()[1]:
        return False

    if '/robots.txt' in hit.split()[1]:
        return False

    if '/favicon.ico' in hit.split()[1]:
        return False

    if '.rss' in hit.split()[1]:
        return False

    if '.atom' in hit.split()[1]:
        return False

    return True

'''
Check whether visitors are from US.
'''
def isUS(x):
    '''
    Input: an IP of a host
    Output: hosts come from US
    >>>
    >>> response = reader.city('128.101.101.101')
    >>>
    >>> response.country.iso_code
    'US'
    >>> response.country.name
    'United States'
    >>>
    >>> response.subdivisions.most_specific.name
    'Minnesota'
    >>> response.subdivisions.most_specific.iso_code
    'MN'
    >>>
    >>> response.city.name
    'Minneapolis'
    >>>
    >>> response.postal.code
    '55455'
    >>>
    '''
    response = reader.city(x)
    if response.country.iso_code == 'US':
        return True
    
'''
Read in access.log,
Pase the apache log file to create a list with all
qualifications - ignore css, images, static, favicon.ico, etc
'''

with codecs.open("/root/devhomework/access.log", encoding='utf-8') as f:
    for line in f: 
        m = pattern.match(line)
        res = m.groupdict()
        if notIgnored(res["request"]):
            y.append(res["host"])
        else:
            continue


'''
Create a list for visitors from United States,
Print out top 10 cities with number of vistors
'''
print("\n\nCalculating top 10 US cities....")
usList = []
for element in y:
    if isUS(element):
        cityRes = reader.city(element)
        usList.append(cityRes.subdivisions.most_specific.name)
    else:
        continue

usCityList = Counter(usCity for usCity in usList)
top10 = usCityList.most_common(10)
print("\n\nTop 10 US states:\n")
print("\tVisitors\tStates")
for p in top10:
    print("\t%r\t\t%s " % p[::-1])

'''
Create a list for visitors from top 10 countries,
Print out top 10 counties with number of visitors.
'''
countryList = []
for element in y:
    countryRes = reader.city(element)
    countryList.append(countryRes.country.name)

countryList = Counter(country for country in countryList)
top10 = countryList.most_common(10)
print("\n\nTop 10 countries: \n")
print("\tVisitors\tCountry")
for p in top10:
    print("\t%r\t\t%s" % p[::-1])

