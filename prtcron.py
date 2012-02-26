#!/usr/bin/env python
# Copyright (c) 2010 Tim 'Shaggy' Bielawa <timbielawa@gmail.com>
# 	      2010 Andrew Butcher <abutcher@afrolegs.com>
# 	      2010 Ricky Hussmann <ricky.hussmann@gmail.com>
# 	      2010 Kel Cecil <kelcecil@praisechaos.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import urllib2;
import json;
import time;
import datetime;
import os;
import pprint

def main():
   # Perform the search GET
    nativeTweetData = TweetData()
    weatherData = WeatherData()

    for tweet in nativeTweetData[u'results']:

        tweetDate = datetime.datetime(*time.strptime(tweet[u'created_at'], "%a, %d %b %Y %H:%M:%S +0000")[0:6])
        delta = datetime.timedelta(hours=2)
        now = datetime.datetime(*time.localtime()[0:6])

        if tweetDate > now - delta:
            opts = []
            opts.append('datum[created_at]=\"%s\"' % tweet[u'created_at'])
            opts.append('datum[from_user]=\"%s\"' % tweet[u'from_user'])
            opts.append('datum[from_user_name]=\"%s\"' % tweet[u'from_user_name'])
            opts.append('datum[tweet_id]=\"%s\"' % tweet[u'id'])
            opts.append('datum[profile_image_url]=\"%s\"' % tweet[u'profile_image_url'])
            opts.append('datum[source]=\"%s\"' % tweet[u'source'])
            opts.append('datum[text]=\"%s\"' % tweet[u'text'])    
            opts.append('datum[humidity]=\"%s\"' % weatherData[u'atmosphere'][u'humidity'])
            opts.append('datum[pressure]=\"%s\"' % weatherData[u'atmosphere'][u'pressure'])
            opts.append('datum[visibility]=\"%s\"' % weatherData[u'atmosphere'][u'visibility'])
            opts.append('datum[temperature]=\"%s\"' % weatherData[u'condition'][u'temperature'])
            opts.append('datum[wind_direction]=\"%s\"' % weatherData[u'wind'][u'direction'])
            opts.append('datum[wind_speed]=\"%s\"' % weatherData[u'wind'][u'speed'])
            opts.append('datum[condition]=\"%s\"' % weatherData[u'condition'][u'text'])

            command = "curl "
            for opt in opts:
                command += "-d " + opt + " "
            command += "prtdata.afrolegs.com/data"
            os.system(command)

def PrintTweets(data):
    print data

def PrintTweetText(data):
    # This prints everything returned by the query.
    # If you're interested in locality, check out how I filter in KelsBagOWords(data)
    for Tweet in data[u'results']:
        print Tweet[u'from_user'], Tweet[u'text']

def TweetData():
    tweet_response = urllib2.urlopen('http://search.twitter.com/search.json?q=WVUDOT&from_user_id_str=85356593')
    tweet_data = tweet_response.read()
    nativeTweetData = json.loads(tweet_data)
    return nativeTweetData

def WeatherData():
    weather_response = urllib2.urlopen('http://weather.yahooapis.com/forecastjson?w=2454113')
    weather_data = weather_response.read()
    nativeWeatherData = json.loads(weather_data)
    return nativeWeatherData

if __name__ == "__main__":
    main()
