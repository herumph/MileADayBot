#!/usr/bin/python3

import mileadaybot
import praw
import re
from datetime import datetime
from datetime import timedelta
from config_bot import *

#Reddit stuff
r = praw.Reddit(user_agent = 'mileadaybot 2.1 by herumph',
        client_id = ID,
        client_secret = SECRET,
        username = REDDIT_USERNAME,
        password = REDDIT_PASS)
sub = 'amileaday'
#sub = 'rumphybot'
subreddit = r.subreddit(sub)

#initial arrays needed
already_done = mileadaybot.get_array("already_done")
mod_list = r.subreddit(sub).moderator()
streak_list = mileadaybot.get_array("streak_list")

#adding/editing user streaks
def edit_streak(comment, author):
    index = comment.index('!flair')
    #taking only numbers and checking legacy
    if(comment[index+1] == 'legacy'):
        streak = comment[index+2]
        streak = ''.join(x for x in streak if x.isdigit())
        legacy = 'yes'
    else:
        streak = comment[index+1]
        streak = ''.join(x for x in streak if x.isdigit())
        legacy = 'no'
    flair = mileadaybot.flair_tag(int(streak), legacy)
    subreddit.flair.set(author,flair)
    #getting rid of user in streak_list if they already had a streak
    if(streak_list.count(author)):
        index = streak_list.index(author)
        del streak_list[index]
        del streak_list[index]
        del streak_list[index]
        streak_list.append(author)
        streak_list.append(streak)
        streak_list.append(legacy)
        message = "Streak updated to "+streak+" days!"
    else:
        streak_list.append(author)
        streak_list.append(streak)
        streak_list.append(legacy)
        message = "Flair saved! Your streak is "+streak+" days!"
    mileadaybot.write_out("streak_list",streak_list)
    return(message)

#removing streaks
def remove(comment, author):
    index = comment.index('!remove')
    person = comment[index+1]
    #No deleting someone else's streak (unless a mod)
    if(author in mod_list or author == person):
        index = streak_list.index(person)
        del streak_list[index]
        del streak_list[index]
        del streak_list[index]
        mileadaybot.write_out("streak_list", streak_list)
        message = person+"'s flair has been removed"
    else:
        message = "You cannot delete someone else's flair."
    return(message)

#incrementing or decrementing streaks
def increment(inc, streak_list):
    temp = []
    for i in range(0,len(streak_list)-1,3):
        temp.append(streak_list[i])
        temp.append(int(streak_list[i+1])+inc)
        temp.append(streak_list[i+2])
        flair = mileadaybot.flair_tag(temp[i+1], temp[i+2])
        subreddit.flair.set(temp[i],flair)
    streak_list = temp
    mileadaybot.write_out("streak_list", streak_list)
    return

def main():
    #comments
    for comment in r.subreddit(sub).comments(limit=25):
        if(comment.id not in already_done and str(comment.author).lower() != "mileadaybot"):
            already_done.append(comment.id)
            #keeping already_done small
            del already_done[0]
            mileadaybot.write_out("already_done", already_done)

            #saving comment
            comment_list = str(comment.body)
            comment_list = comment_list.split()
            author = str(comment.author)

            #flair editing and requests
            if(comment_list.count("!flair")):
                message = edit_streak(comment_list, author)
                comment.reply(message)
                return

            #removing flair
            if(comment_list.count("!remove")):
                message = remove(comment_list, author)
                comment.reply(message)
                return

            #incrementing/decrementing (mod only)
            if(comment_list.count("!increment") and author in mod_list):
                index = comment_list.index('!increment')
                increment(int(comment_list[index+1]), streak_list)
                comment.reply("All flairs updated by "+comment_list[index+1])
                return
            elif(comment_list.count("!increment") and author not in mod_list):
                comment.reply("You are not allowed to increment flairs.")
                return

    #incrementing all streaks at 3AM
    time = datetime.now()
    timearr = mileadaybot.get_array("last_updated")
    update = datetime.strptime(timearr[0], "%Y-%m-%d %H:%M:%S")
    if(time > (update + timedelta(days=1))):
        timearr[0] = update + timedelta(days=1)
        increment(1, streak_list)
        mileadaybot.write_out("last_updated", timearr)
        return

main()
