#!/usr/bin/python3

#Function to assign flair tag.
def flair_tag(days, legacy):
    #non-legacy
    streak = str(days)+' days, '
    #legacy flairs
    if(legacy == 'yes'):
        days = int(days/10) * 10
        streak = str(days)+'+ days, '
    if(days < 10):
        return("newbie")
    elif(days >= 10 and days < 20):
        return(streak+"double digits")
    elif(days >= 20 and days < 50):
        return(streak+"now we're streaking")
    elif(days >= 50 and days < 100):
        return(streak+"half a century")
    elif(days >= 100 and days < 150):
        return(streak+"triple digits")
    elif(days >= 150 and days < 300):
        return(streak+"whoa")
    elif(days >= 300 and days < 365):
        return(streak+"coming up on a year")
    elif(days >= 365 and days < 400):
        return(streak+"one year of streaking!")
    elif(days >= 400 and days < 500):
        return(streak+"almost half a thousand")
    elif(days >= 500 and days < 600):
        return(streak+"half way to the comma club")
    elif(days >= 600 and days < 730):
        return(streak+"coming up on two years")
    elif(days >= 730 and days < 800):
        return(streak+"two years!")
    elif(days >= 800 and days < 900):
        return(streak+"that's dedication")
    elif(days >= 900 and days < 1000):
        return(streak+"coming up on the comma")
    elif(days >= 100 and days < 1095):
        return(streak+"comma club!")
    elif(days >= 1095 and days < 1450):
        return(streak+"three years!")
    elif(days >= 1450 and days < 1825):
        return(streak+"four years!")
    elif(days >= 1825 and days < 2190):
        return(streak+"five years!")
    elif(days >= 2190 and days < 2555):
        return(streak+"six years!")
    elif(days >= 2555 and days < 2920):
        return(streak+"seven years!")
    elif(days >= 2920 and days < 3285):
        return(streak+"eight years!")
    elif(days >= 3285 and days < 3650):
        return(streak+"nine years!")
    elif(days >= 3650): 
        return(streak+"over ten years of streaking!")

#Functions to read and print out to files.
def get_array(input_string):
    with open("textfiles/"+input_string+".txt","r") as f:
        input_array = f.readlines()
        input_array = [x.strip("\n") for x in input_array]
        return(input_array)

def write_out(input_string,input_array):
    with open("textfiles/"+input_string+".txt","w") as f:
        for i in input_array:
            f.write(str(i)+"\n")
    return
