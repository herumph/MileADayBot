#!/usr/bin/python3

#Bot to add and edit flair for /r/amileaday. Increments user flair by 1 every day at 3AM. Last update 11/29/2016.
#Request for legacy flair (50+,100+,150+,...) and emojis for number of years streaking.

import praw
import re
from datetime import datetime
from datetime import timedelta
from sys import exit
from config_bot import *

#Getting reddit information.
r = praw.Reddit(user_agent = 'mileadaybot 2.0 by herumph',
    client_id = ID,
    client_secret = SECRET,
    username = REDDIT_USERNAME,
    password = REDDIT_PASS)
#reddit.login(REDDIT_USERNAME,REDDIT_PASS)
#subreddit = r.get_subreddit("amileaday")
#subreddit = r.get_subreddit("RumphyBot")
subreddit = r.subreddit('amileaday')
subreddit_comments = subreddit.comments

#print('\n * * * * * * * * * * * * * * * * * * * * * * * * * * * \n')
#print(list(subreddit_comments))

#Function to assign flair tag.
def flair_tag(days):
    if(days < 10):
        return("newbie")
    elif(days >= 10 and days < 20):
        return("double digits")
    elif(days >= 20 and days < 50):
        return("now we're streaking")
    elif(days >= 50 and days < 100):
        return("half a century")
    elif(days >= 100 and days < 150):
        return("triple digits")
    elif(days >= 150 and days < 300):
        return("whoa")
    elif(days >= 300 and days < 365):
        return("coming up on a year")
    elif(days >= 365 and days < 400):
        return("one year of streaking!")
    elif(days >= 400 and days < 500):
        return("almost half a thousand")
    elif(days >= 500 and days < 600):
        return("half way to the comma club")
    elif(days >= 600 and days < 730):
        return("coming up on two years")
    elif(days >= 730 and days < 800):
        return("two years!")
    elif(days >= 800 and days < 900):
        return("that's dedication")
    elif(days >= 900 and days < 1000):
        return("coming up on the comma")
    elif(days >= 100 and days < 1095):
        return("comma club!")
    elif(days >= 1095 and days < 1450):
        return("three years!")
    elif(days >= 1450 and days < 1825):
        return("four years!")
    elif(days >= 1825 and days < 2190):
        return("five years!")
    elif(days >= 2190 and days < 2555):
        return("six years!")
    elif(days >= 2555 and days < 2920):
        return("seven years!")
    elif(days >= 2920 and days < 3285):
        return("eight years!")
    elif(days >= 3285 and days < 3650):
        return("nine years!")
    elif(days >= 3650): 
        return("over ten years of streaking!")

#Functions to read and print out to files.
def get_array(input_string):
    with open(input_string+".txt","r") as f:
        input_array = f.readlines()
        input_array = [x.strip("\n") for x in input_array]
        return(input_array)

def write_out(input_string,input_array):
    with open(input_string+".txt","w") as f:
        for i in input_array:
            f.write(str(i)+"\n")
    return

#Getting arrays.
streak_list = get_array('streak_list')
edited_users = get_array('edited_users')
already_done = get_array('already_done')
allowed_users = get_array('allowed_users')

#Time stuff
time=datetime.now()
timearr = get_array("last_updated")
update = datetime.strptime(timearr[0], "%Y-%m-%d %H:%M:%S")

#Looking through comments.
for comment in r.subreddit('amileaday').comments(limit=25):
	#Flair add requests.
	if(comment.body.lower().count("mileadaybot streak") and comment.id not in already_done and str(comment.author) not in edited_users):
		already_done.append(comment.id)
		write_out("already_done",already_done)
		text = comment.body
		call_index = [n for n in range(len(text)) if text.find("mileadaybot streak",n) == n]
		text = text[call_index[0]:]
		text = text.split()
		#Taking only numbers from input.
		streak = re.search('\d+', text[2]).group()
		author = str(comment.author)
		subreddit.flair.set(author,streak)
		#Getting rid of user in streak_list.txt if they already had a streak.
		if(streak_list.count(author)):
			author_index = streak_list.index(author)
			del streak_list[author_index]
			del streak_list[author_index]
			streak_list.append(author)
			streak_list.append(streak)
			write_out('streak_list',streak_list)
			comment.reply("Streak updated to "+streak+" days!")
		else:
			streak_list.append(author)
			streak_list.append(streak)
			write_out('streak_list',streak_list)
			comment.reply("Flair saved! Your streak is "+streak+" days!")

	#Responding to edited user.
	if(comment.body.lower().count("mileadaybot streak") and comment.id not in already_done and str(comment.author) in edited_users):
		already_done.append(comment.id)
		write_out('already_done',already_done)
		comment.reply("Your flair has been edited by a mod and cannot be changed. Please contact a moderator for assistance.")

	#Allowed user editing flair.
	if(str(comment.author) in allowed_users and comment.id not in already_done and comment.body.lower().count("!flair")):
		already_done.append(comment.id)
		write_out("already_done",already_done)
		text = comment.body
		call_index = [n for n in range(len(text)) if text.find("!flair",n) == n]
		text = text[call_index[0]:]
		text = text.rsplit()
		author,streak = text[1],text[2]
		subreddit.flair.set(author,streak)
		if(streak_list.count(author)):
			author_index = streak_list.index(author)
			del streak_list[author_index]
			del streak_list[author_index]
			streak_list.append(author)
			streak_list.append(streak)
		else:
			streak_list.append(author)
			streak_list.append(streak)
		edited_users.append(author)
		write_out('edited_users',edited_users)
		write_out('streak_list',streak_list)
		comment.reply("Edited user's flair.")

	#Allowed user clearing flair.
	if(str(comment.author) in allowed_users and comment.id not in already_done and comment.body.lower().count("!remove")):
		already_done.append(comment.id)
		write_out("already_done",already_done)
		text = comment.body
		call_index = [n for n in range(len(text)) if text.find("!remove",n) == n]
		text = text[call_index[0]:]
		text = text.split()
		subreddit.flair.delete(text[1])
		#Taking user off of streak_list once cleared.
		author_index = streak_list.index(text[1])
		del streak_list[author_index]
		del streak_list[author_index]
		write_out('streak_list', streak_list)
		if(text[1] in edited_users):
			edited_users.remove(text[1])
			write_out('edited_users',edited_users)
		comment.reply("User's flair has been removed.")

	if(str(comment.author) in allowed_users and comment.id not in already_done and comment.body.lower().count("!mileadaybot increment")):
		temp_list=[]
		already_done.append(comment.id)
		write_out("already_done",already_done)
		for i in range(0,len(streak_list)-1,2):
			temp_list.append(streak_list[i])
			temp_list.append(int(streak_list[i+1])+1)
			tag = flair_tag(temp_list[i+1])
			subreddit.flair.set(temp_list[i],str(temp_list[i+1])+' days, '+tag)
		streak_list=temp_list
		write_out('streak_list',streak_list)
		comment.reply("All flairs updated!")

#Incrementing all streaks at 3AM. 
if(time > (update + timedelta(days=1))):
    temp_list=[]
    timearr[0] = update + timedelta(days=1)
    for i in range(0,len(streak_list)-1,2):
        temp_list.append(streak_list[i])
        temp_list.append(int(streak_list[i+1])+1)
        tag = flair_tag(temp_list[i+1])
        subreddit.flair.set(temp_list[i],str(temp_list[i+1])+' days, '+tag)
    streak_list=temp_list
    write_out('streak_list',streak_list)
    write_out('last_updated',timearr)
