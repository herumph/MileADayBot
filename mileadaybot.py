#!/Users/sfdavis/anaconda3/bin/python

#Bot to add and edit flair for /r/amileaday. Increments user flair by 1 every day at 3AM. Last update 11/29/2016.
#Request for legacy flair (50+,100+,150+,...) and emojis for number of years streaking.

import praw
import re
from datetime import datetime
from sys import exit
from config_bot import *

#Getting reddit information.
r = praw.Reddit("mileadaybot 1.1 by herumph")
r.login(REDDIT_USERNAME,REDDIT_PASS)
#subreddit = r.get_subreddit("amileaday")
subreddit = r.get_subreddit("RumphyBot")
subreddit_comments = subreddit.get_comments()

time=str(datetime.now())
print('\n * * * * * * * * * * * * * * * * * * * * * * * * * * * \n')

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

#Looking through comments.
for comment in subreddit_comments:
	#Flair add requests.
	if(comment.body.lower().count("mileadaybot streak") and comment.id not in already_done and str(comment.author) not in edited_users):
		text = comment.body
		call_index = [n for n in range(len(text)) if text.find("mileadaybot streak",n) == n]
		text = text[call_index[0]:]
		text = text.split()
		#Taking only numbers from input.
		streak = re.search('\d+', text[2]).group()
		author = str(comment.author)
		subreddit.set_flair(author,flair_text=streak)
		already_done.append(comment.id)
		write_out('already_done',already_done)
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
		text = comment.body
		call_index = [n for n in range(len(text)) if text.find("!flair",n) == n]
		text = text[call_index[0]:]
		text = text.rsplit()
		author,streak = text[1],text[2]
		subreddit.set_flair(author,flair_text = streak)
		already_done.append(comment.id)
		write_out('already_done',already_done)
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
		text = comment.body
		call_index = [n for n in range(len(text)) if text.find("!remove",n) == n]
		text = text[call_index[0]:]
		text = text.split()
		subreddit.delete_flair(user=text[1])
		#Taking user off of streak_list once cleared.
		author_index = streak_list.index(text[1])
		del streak_list[author_index]
		del streak_list[author_index]
		already_done.append(comment.id)
		write_out('already_done',already_done)
		write_out('streak_list', streak_list)
		if(text[1] in edited_users):
			edited_users.remove(text[1])
			write_out('edited_users',edited_users)
		comment.reply("User's flair has been removed.")

#Incrementing all streaks at 3AM.
if(time[11:-10] == "03:00"):
	temp_list=[]
	for i in range(0,len(streak_list)-1,2):
		temp_list.append(streak_list[i])
		temp_list.append(int(streak_list[i+1])+1)
		subreddit.set_flair(temp_list[i],flair_text=temp_list[i+1])
	streak_list=temp_list
	write_out('streak_list',streak_list)
