import praw
import os
import time

def botlogin():
    #logs in to reddit, using the username and password, which has been redacted
    print("Logging in...")
    r = praw.Reddit(client_id = 'ZSz_-H9B0mBB-w',
                client_secret = '3R-EQ6Gr9nLkp2Plyz-So1ymxKA',
                password = '#redacted',
                username = 'BoomSoonBot',
                user_agent = 'test')
    print("Logged in!")
    return r

def run_bot(r, posts_replied_to):
    #selects the subreddit and comment chains, with a 15 comment limit
    subreddit = r.subreddit('CFB')
    comments = subreddit.comments(limit=15)
    #searches for certain keywords
    keywords = {'BOOMER', 'Boomer', 'Sooner', 'SOONER',
                'BOOMER SOONER', 'OU', 'Oklahoma', 'OKLAHOMA'}
    replyformat = {"""BOOMER SOONER ALL DAY BABY!
                \n\nThis is an automatic Boomer Sooner reply.
                \n\n You are welcome."""}
    print("Getting 15 comments...")
    for comment in comments:
        for keyword in keywords:
            if keyword in comment.body and comment.id not in posts_replied_to and comment.author != r.user.me():
                print("Keyword found in ", comment.id, "!")
                comment.reply(replyformat)
                posts_replied_to.append(comment.id)

            with open("BS_posts_replied_to.txt", "a") as f:
                #adds the comment id to the text file, ensuring it doesn't
                #reply to a comment more than once
                if comment.id not in posts_replied_to:
                    f.write(comment.id + "\n")
    #I ran into an issue where reddit would kick the bot out for commenting
    #too often, requiring me to add the sleep language
    print("Sleeping for 5 minutes...")
    time.sleep(300)

def get_saved_posts():
    #looks to see if the text file exists, and if it doesn't it creates it
    if not os.path.isfile("BS_posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("BS_posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

        return posts_replied_to

r = botlogin()
posts_replied_to = get_saved_posts()
print(posts_replied_to)

while True:
    run_bot(r, posts_replied_to)
