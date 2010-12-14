#!/usr/bin/env python
# Do it for the cross-platform baby...

# For performing the GET request
import urllib2;

# For parsing the JSON result
import json;

# Perform the search GET
response = urllib2.urlopen('http://search.twitter.com/search.json?q=geocode:39.633611,-79.950556,25mi%20PRT')
data = response.read()

# Parse the JSON data and print it to the terminal
# That's all for now...
nativeData = json.loads(data)

for tweet in nativeData[u'results']:
    # Problem: Some people that are far, far away from Morgantown use :pRT frequently in their tweets for a reason normal humans can not comprehend.
    # Solution:  Ensure that the locations of tweets are in Morgantown or West Virginia.  This change filtered only the annoying :pRT messages and left the sensible messages alone.
    if "West Virginia" in tweet[u'location'] or "Morgantown" in tweet[u'location']:
        print tweet[u'text'];
    else:
        continue
