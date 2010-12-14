#!/usr/bin/env python
# Do it for the cross-platform baby...

# For performing the GET request
import urllib2;

# For parsing the JSON result
import json;

# For selecting what analysis method you want.
import argparse

def main():

    

    # Perform the search GET
    response = urllib2.urlopen('http://search.twitter.com/search.json?q=geocode:39.633611,-79.950556,25mi%20PRT')
    data = response.read()

    # Parse the JSON data and print it to the terminal
    # That's all for now...
    nativeData = json.loads(data)

    Madness = ParseArguments()

    if (Madness.PrintTweets == True):
        PrintTweets(nativeData)
    if (Madness.PrintTweetText == True):
        PrintTweetText(nativeData)
    if (Madness.KelsBagOWords == True):
        KelsBagOWords(nativeData)

def ParseArguments():
    # Check sys.argv for arguments.
    parser = argparse.ArgumentParser(description='A Python script to provide methods to determine if the PRT is running.  Cookies to he who creates the best method.  So say we all.')
    parser.add_argument('--printtweets',dest='PrintTweets', action='store_true',help='Print the information passed to the classifiers.  Useful if you want to know what\'s going into your classifier!')
    parser.add_argument('--printtweettext',dest='PrintTweetText', action='store_true',help='Print the plain text of the tweets returned by the Twitter query.')
    parser.add_argument('--kelsbagofwords',dest='KelsBagOWords', action='store_true',help='Kel\'s simple attempt at using a simple bag of words technique. Intended to inspire others to join in rather than giving any kind of useful data.')

    args = parser.parse_args()
    return args

def PrintTweets(data):
    print data

def PrintTweetText(data):
    # This prints everything returned by the query.
    # If you're interested in locality, check out how I filter in KelsBagOWords(data)
    for Tweet in data[u'results']:
        print Tweet[u'text']


# This approach simply attempts a bag of words approach with no temporal constraints(which is a bad thing here since there's so few tweets)
# I can promise before even writing that method will be the suck.
# Just throwing this in to get the ball rolling :)
def KelsBagOWords(data):
    for tweet in nativeData[u'results']:
        # Problem: Some people that are far, far away from Morgantown use :pRT frequently in their tweets for a reason normal humans can not comprehend.
        # Solution:  Ensure that the locations of tweets are in Morgantown or West Virginia.  This change filtered only the annoying :pRT messages and left the sensible messages alone.
        if "West Virginia" in tweet[u'location'] or "Morgantown" in tweet[u'location']:
            print tweet[u'text'];
        else:
            continue
    

if __name__ == "__main__":
    main()
