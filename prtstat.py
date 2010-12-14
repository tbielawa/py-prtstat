#!/usr/bin/python

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
print nativeData
