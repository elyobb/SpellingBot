from random import shuffle
import random
import tweepy

from data import data as d

consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_SECRET'

class Correction:
    def __init__(self, misspelled, correctionData):
        mispChoices = [x.strip() for x in misspelled.split(',')]   
        wordData = correctionData[0]             
        wordChoices = [x.strip() for x in wordData.split(',')]
        
        if(len(mispChoices) > 1):
            randIdx = random.randint(0, 1)
        else:
            randIdx = 0
            
        if(len(wordChoices)> 1):
            wordIdx = randIdx
        else:
            wordIdx = 0
            
        self.misspelled = mispChoices[randIdx]
        self.word = wordChoices[wordIdx]        
        self.correction = correctionData[1]

    def getMisspelled(self):
        return self.misspelled
    
    def getWord(self):
        return self.word
    
    def getCorrection(self):
        return self.correction
    
def correctATweet(correction):   
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    twt = api.search(q=correction.getMisspelled(), lang="en")
    shuffle(twt)
    while(twt):      
        s = twt.pop()
        print(s.text)
        sn = s.user.screen_name
        id_str = s.id_str
        print(sn)
        url = "https://twitter.com/" + sn + "/status/" + id_str

        msg = "'%s' has been misspelled as '%s' by @%s\n%s\n\nRemember: %s" % (correction.getWord(), correction.getMisspelled(), sn, url, correction.getCorrection())
        if(len(msg) <= 140):
            s = api.update_status(msg)
            return True
    return False     

def constructWords():
    words = []
    for key in d:
        corr = Correction(key, d[key])
        words.append(corr)
    return words
   
def main():
    words = constructWords()
    shuffle(words)
    # try up to 5 different words before quitting       
    for x in range(5):
        word = words.pop()
        if(correctATweet(word)):
            # success, add user and misspelled word to history file
            return
          
if __name__ == "__main__":
    main()
    
