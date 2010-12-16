#!/usr/bin/env python
# Do it for the cross-platform baby...

# For performing the GET request
import urllib2;

# For parsing the JSON result
import json;

# For selecting what analysis method you want.
from optparse import OptionParser

# For weather xml parsing
from xml.dom import minidom

# Pretty print
from pprint import pprint

def main():
   # Perform the search GET
    nativeTweetData = TweetData()

    Madness = ParseArguments()

    # Until we get some more algos I'm making kels bag of words the default
    # Eventually there will be a class to register algos with called 'guess'.
    # You'll call it like guess.with('kels')
    # When you write an algo you'll register it with a name and a function reference
    # Like guess.register('kels', KelsBagOWords)
    if Madness.PrintTweets:
        PrintTweets(nativeTweetData)

    if Madness.PrintTweetText:
        PrintTweetText(nativeTweetData)

    if Madness.WeatherData:
        pprint(WeatherData("26506"))

    # Guess
    KelsBagOWords(nativeTweetData)


def ParseArguments():
    # Check sys.argv for arguments.
    parser = OptionParser()
    parser.add_option('--printtweets',
                      dest='PrintTweets',
                      action='store_true',
                      help='Print the information passed to the classifiers.  Useful if you want \
                            to know what\'s going into your classifier!')
    parser.add_option('--printtweettext',
                      dest='PrintTweetText',
                      action='store_true',
                      help='Print the plain text of the tweets returned by the Twitter query.')
    parser.add_option('--kelsbagofwords',
                      dest='KelsBagOWords',
                      action='store_true',
                      help='Kel\'s simple attempt at using a simple bag of words \
                            technique. Intended to inspire others to join in rather than giving \
                            any kind of useful data. (This is default)')
    parser.add_option('--weatherdata',
                       dest='WeatherData',
                       action='store_true',
                       help='Print weather information for Morgantown, WV.')

    (options, args) = parser.parse_args()
    return options

def PrintTweets(data):
    print data

def PrintTweetText(data):
    # This prints everything returned by the query.
    # If you're interested in locality, check out how I filter in KelsBagOWords(data)
    for Tweet in data[u'results']:
        print Tweet[u'from_user'], Tweet[u'text']

def WeatherData(zip_code):
    weather_url = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
    weather_ns = 'http://xml.weather.yahoo.com/ns/rss/1.0'

    url = weather_url % zip_code
    dom = minidom.parse(urllib2.urlopen(url))
    forecasts = []
    for node in dom.getElementsByTagNameNS(weather_ns, 'forecast'):
        forecasts.append({
            'date': node.getAttribute('date'),
            'low': node.getAttribute('low'),
            'high': node.getAttribute('high'),
            'condition': node.getAttribute('text')
            })
        ycondition = dom.getElementsByTagNameNS(weather_ns, 'condition')[0]
        return {
            'current_condition': ycondition.getAttribute('text'),
            'current_temp': ycondition.getAttribute('temp'),
            'forecasts': forecasts,
            'title': dom.getElementsByTagName('title')[0].firstChild.data
            }
    
def TweetData():
    tweet_response = urllib2.urlopen('http://search.twitter.com/search.json?q=geocode:39.633611,-79.950556,25mi%20PRT')
    tweet_data = tweet_response.read()
    nativeTweetData = json.loads(tweet_data)
    return nativeTweetData

# This approach simply attempts a bag of words approach with no temporal constraints(which is a bad thing here since there's so few tweets)
# I can promise before even writing that method will be the suck.
# Just throwing this in to get the ball rolling :)  I have a better idea I'll throw in later if someone else gives it a go.
def KelsBagOWords(data):
    # The idea behind a bag of words technique is that we simply look to see if word x occurs in a tweet.  If more negative words than positive, the PRT is down.
    # We don't consider temporal effects ( tweets that are older than a certain age shouldn't be considered)
    # or weighing some users more heavily than others (the official WVU prt twitter account over others).
    GoodWords = ['currently running', 'normal']
    BadWords = ['down','stop', 'hate', 'bus', 'out of service', 'closed']
    Balance = 0
    
    for tweet in data[u'results']:
        # Problem: Some people that are far, far away from Morgantown use :pRT frequently in their tweets for a reason normal humans can not comprehend.
        # Solution:  Ensure that the locations of tweets are in Morgantown or West Virginia.  This change filtered only the annoying :pRT messages and left the sensible messages alone.
        if "West Virginia" in tweet[u'location'] or "Morgantown" in tweet[u'location']:
            GoodSigns = 0
            BadSigns = 0
            for Good in GoodWords:
                #Weighting Good Signs since there seem to be fewer ways to express approval of the PRT.
                if Good in tweet[u'text']:
                    GoodSigns = GoodSigns + 3
            for Bad in BadWords:
                if Bad in tweet[u'text']:
                    BadSigns = BadSigns + 1
            if GoodSigns > BadSigns:
                Balance = Balance + 1
            elif BadSigns > GoodSigns:
                Balance = Balance - 1
        else:
            continue

    print "Kel's Bag O' Words method thinks..."
    if Balance > 0:
        print "The PRT is probably running (Score: " + str(abs(Balance)/len(data[u'results'])) + ")"
    elif Balance < 0:
        print "The PRT is probably not running (Score: " + str(abs(Balance)/len(data[u'results'])) + ")"
    else:
        print "that you should probably just go look for yourself... No one on Twitter seems to know..."

if __name__ == "__main__":
    main()
