from tweepy import *
import time

from tweepy import *

from Correction import *


def newMention(twt, id):
    if ('RT @' not in twt.text) and (not twt.retweeted):
        filename = 'since_id.txt'
        try:
            file = open(filename, 'r+')
        except IOError:
            file = open(filename, 'w+')

        fileid = file.readline()
        if fileid == '' or id > int(fileid):
            file = open(filename, 'w').close()
            file = open(filename, 'w')
            file.write(str(id))
            file.close()
            return True
    return False


def getFinalMsg(pct):
    if pct == 100.00:
        return "Incredible! Your profile gets an A+!"
    elif pct < 100.00 and pct >= 93.00:
        return "Congratulations! Your profile gets an A!"
    elif pct < 93.00 and pct >= 90.00:
        return "Great job! Your profile gets an A-!"
    elif pct < 90.00 and pct >= 87.00:
        return "Nice job! Your profile gets a B+!"
    elif pct < 87.00 and pct >= 83.00:
        return "Good job! Your profile gets a B."
    elif pct < 83.00 and pct >= 80.00:
        return "Good job! Your profile gets a B-. "
    elif pct < 80.00 and pct >= 77.00:
        return "Satisfactory handiwork. Your profile gets a C+."
    elif pct < 77.00 and pct >= 73.00:
        return "Satisfactory handiwork. Your profile gets a C."
    elif pct < 73.00 and pct >= 70.00:
        return "Satisfactory handiwork. Your profile gets a C-."
    elif pct < 70.00 and pct >= 67.00:
        return "Poor work. Your profile only earned a D+."
    elif pct < 67.00 and pct >= 63.00:
        return "Poor work. Your profile only earned a D."
    elif pct < 63.00 and pct >= 60.00:
        return "Poor work. Your profile only earned a D-."
    elif pct < 60.00:
        return "Sorry, but your profile gets an F. Try again once you've tweeted without mistakes!"


def getUserGrade(tweets):
    if len(tweets) > 0:
        misspelled = 0
        total = len(tweets)
        corrections = constructWords()
        for tweet in tweets:
            if tweetIsPermissable(tweet):
                for correction in corrections:
                    if correction.getMisspelled().upper() in tweet.text.upper():
                        misspelled += 1
                        break
        pct = (round(((misspelled / total) * 100), 2))
        finalPct = 100 - pct
        return "%d of your last %d tweets had a common misspelling therein.\nYour grade: %.2f%%\n%s" % (
        misspelled, total, finalPct, getFinalMsg(finalPct))
    else:
        return ""


def listen():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    handle = auth.get_username()

    api = tweepy.API(auth, wait_on_rate_limit=True)

    while True:
        time.sleep(60)
        results = api.search(handle)
        since_id = results.since_id
        for twt in results:
            if (newMention(twt, twt.id)):

                text = twt.text
                if (text.upper() == "@" + handle.upper() + " ME") or (text.upper() == "ME"):
                    # logic to check through all tweets
                    tweets = api.user_timeline(screen_name=twt.user.screen_name, count=200, include_rts=False)
                    response = getUserGrade(tweets)

                    if response != "":
                        m = "%s\n@%s" % (response, twt.user.screen_name)
                        try:
                            api.update_status(m, in_reply_to_status_id=twt.id)
                        except TweepError:
                            print(TweepError.reason)
                            continue


def main():
    listen()


if __name__ == "__main__":
    main()
