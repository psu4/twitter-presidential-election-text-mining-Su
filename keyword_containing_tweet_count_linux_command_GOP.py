'''
The code is tested in python 2.7.6, Pandas 0.17.0, simplejson 3.8.1 in Windows 7 PC and Linux CentOS 5.0

Prepare by Dr.Pin-Chih Su on Nov 18th, 2015
'''

##import json
import simplejson as json
'''
(1)'simplejson' is faster and takes less memory than traditional json.
You can also use tradition 'json' here.
'ijson' is even quicker, but the script might need major modification
(2)Install simplejson:
(a)Windows: pip install simplejson
(b)Linux: pip install --target='directory_name' simplejson
(c)If not installed in Python directory, add the following in Linux .bash_profile or .bashrc:
PYTHONPATH="${PYTHONPATH}:${simplejson_directory}"
source .bash_profile or .bashrc
'''
import pandas as pd
##import matplotlib.pyplot as plt
import re
import time
import os
import sys, getopt

startTime=time.time()

#### Let the script take command-line inputs

def main(argv):
    
    inputfile = ''
   
    outputfile = ''

    try:
       
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
      
    except getopt.GetoptError:
       
        print 'python keyword_containing_tweet_count_linux_command.py -i <inputfile> -o <outputfile>'
      
        sys.exit(2)
      
    for opt, arg in opts:
       
        if opt == '-h':
          
            print '\n'+'(1) Usage: python keyword_containing_tweet_count_linux_command.py -i <inputfile> -o <outputfile>'

            sys.exit()
         
        elif opt in ("-i", "--ifile"):
          
            inputfile = arg
         
        elif opt in ("-o", "--ofile"):
          
            outputfile = arg

#### Define the keyword matching function

    def word_in_text(word, text):
        word = word.lower()             # make all word/text lower cases
        text = text.lower()
        b = r'(\s)'
        match = re.match(word+b, text)  # This '+b' will only search keyword+space, such as 'Bob ', 'Ted '
        if match:                       # O(1) - very fast
            return True
        return False

#### Define the file reading and counting
    
    text=[]
    tweets_data = []
    tweets_file = open(inputfile, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)


#The Windows 7, 8GB DDR3 RAM laptop (with 5.5GB free RAM) cannot load json files larger than 737 MB
#If the file is too large, this json.loads will stuck there for hours and show no error.
#If the file is too large, this simplejson.loads will show "memory error"
         
        except:

            continue

        if not all(x in tweet for x in ['text']): # Clean the tweets without "text" labels to avoid errors

            continue
        
        tweets_data.append(tweet)

    keyword_output = open(outputfile, 'w')

    keyword_output.write("Total, "+str(len(tweets_data)).strip('[]'))#Print total number of tweets in the output

    tweets = pd.DataFrame()

    tweets['text'] = [tweet['text'] for tweet in tweets_data]

    def keyword_in_tweet(keyword):

        try:
        
            tweets[keyword] = tweets['text'].apply(lambda tweet: word_in_text(keyword, tweet))
    
            keyword_list=tweets[keyword].value_counts()[True].tolist()  # Count how many 'True'

            keyword_output.write('\n'+keyword+','+str(keyword_list).strip('[]'))

            keyword_output.close

        except KeyError:

            '''
            If there is no any keyword in the file, print 'keyword,0'. If this part is removed,
            the script will stopped and print out a keyerror message when there is no keyword
            in the file
            '''

            keyword_output.write('\n'+keyword+','+str(0))

            keyword_output.close
        
            return

    '''
    These are 2016 GOP presidential canidiates.  The order needs to be firstlastname|lastname|firstname
    | = or
    '''
    keyword_in_tweet('bencarson|carson|ben')
    keyword_in_tweet('jebbush|bush|jeb') 
    keyword_in_tweet('chrischristie|christie|chris')
    keyword_in_tweet('tedcruz|cruz|ted') 
    keyword_in_tweet('carlyfiorina|fiorina|carly')
    keyword_in_tweet('jimgilmore|gilmore|jim')
    keyword_in_tweet('lindseygraham|graham|lindsey')
    keyword_in_tweet('mikehuckabee|huckabee|mike')
    keyword_in_tweet('bobbyjindal|jindal|bobby')
    keyword_in_tweet('johnkasich|kasich|john')
    keyword_in_tweet('georgepataki|pataki|george')
    keyword_in_tweet('randpaul|paul|rand')
    keyword_in_tweet('marcorubio|rubio|marco')
    keyword_in_tweet('ricksantorum|santorum|rick')
    keyword_in_tweet('donaldtrump|trump|donald')

    elapsedTime = time.time()-startTime

    keyword_output.write('\n'+str(elapsedTime))

    keyword_output.close

if __name__ == "__main__":
    
   main(sys.argv[1:])
