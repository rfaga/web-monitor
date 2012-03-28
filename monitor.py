#!/usr/bin/python
#
# @author http://github.com/rfaga
#
# A tool to monitoring connections on websites, and tweet when a fail is detected.
# 
# Any problem is sent as DM to my twitter, where I configured to notify in my email and send me a SMS too.


# Twitter users to be notified
NOTIFY_USERS = ("robertofagajr", )

import twitter, time, datetime, mechanize
global api

# Twitter credentials
api = twitter.Api(
    consumer_key='', 
    consumer_secret='', 
    access_token_key='',
    access_token_secret='')

# Send a tweet as DM to all users in NOTIFY_USERS
def tweet(msg):
	for user in NOTIFY_USERS:
		api.PostDirectMessage(user, msg)

# create status messages, I created these ones in Portuguese
URGENTE = "URGENTE" # urgent!!
IMPORTANTE = "importante" # important, but not urgent
FRACO = "problema fraco" # weak problem
NORMAL = "normal" # normal status


#########################
# Here I made a simple function to monitor each website, in different tests. 
# For this, I used the mechanize python package

def check_bar():
	url = "http://www.bar.com"
	browser = mechanize.Browser()

	# see if main page has the right title
	try:
		resp = browser.open(url)
	except:
		return IMPORTANTE, "Can't connect"
	if "Bar page" not in browser.title(): # server answered some page, but not what I'm looking for
		return URGENTE, "Main page is not the desired one!"
	
	# check if login is ok:
	resp = browser.open(url + "/authenticate", "login=test&password=test")
	raw = resp.read()
	if "robertofaga" not in raw: # if something that should be in login answer
		return URGENTE, "Login is not working"

	return NORMAL, ""

# Then we do the check of all these tests
def check(tries=0):
    # print current date to run this script and echo in a log file
	print datetime.datetime.now()
	status, msg = check_bar()
	# if status is urgent or I tried > 3 times, let's tweet this problem
	if status == URGENTE or tries > 3:
		tweet("Server problem detected: " + msg)
	# if not and status is not normal, let's try again (this could be some network temporary problem)
	elif status != NORMAL:
		print status, msg
		time.sleep(10)
		check(tries+1)

if __name__ == "__main__":
	check()
	
