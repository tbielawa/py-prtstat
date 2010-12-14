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
# Just throwing this in to get the ball rolling :)  I have a better idea I'll throw in later if someone else gives it a go.
def KelsBagOWords(data):
    # The idea behind a bag of words technique is that we simply look to see if word x occurs in a tweet.  If more positive words than negative, the PRT is down.
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
        print "The PRT is probably running: "+abs(Balance)/len(data[u'results'])
    elif Balance < 0:
        print "The PRT is probably not running: "+abs(Balance)/len(data[u'results'])
    else:
        print "that you should probably just go look for yourself... No one on Twitter seems to know..."

if __name__ == "__main__":
    main()
