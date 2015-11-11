# The code is tested in python 2.7, nltk 3.1, matplotlib.pyplot-1.3.1 in Windows 7 PC and Linux CentOS 5.0

# Prepare by Pin-Chih Su on Oct 30th,2015

import json
import operator 
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.util import bigrams 
import string
import time
import matplotlib.pyplot as plt

startTime=time.time()

# The tweet json file to process
tweets_data_path = 'hillary.txt'

# Variables area
the_most_common_word_file = 'hillary_most_common_100_words.txt'
the_most_common_word_plot = 'hillary_most_common_25_words.jpg'
the_most_common_hash_file = 'hillary_most_common_100_hash.txt'
the_most_common_hash_plot = 'hillary_most_common_25_hash.jpg'
the_most_common_bigram_file = 'hillary_most_common_100_bigram.txt'
the_most_common_bigram_plot = 'hillary_most_common_25_bigram.jpg'
the_most_common_donate_word_count_file = 'hillary_most_common_100_donation.txt'
the_most_common_volunteer_word_count_file = 'hillary_most_common_100_volunteer.txt'
donate_word = 'donation' #['donate','donation','donating','donations']
volunteer_word = 'voluntary'
the_most_common_key_word_count_file = 'hillary_most_common_100_key_word_cooccurence.txt'

################## Tokenize function
import re
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

## This tokenize function part is published by Dr. Marco Bonzanini at http://marcobonzanini.com/.  No need to re-invent the wheel.   
##tweet = "RT @marcobonzanini: just an example! :D http://example.com #NLP"
##print(preprocess(tweet))
##['RT', '@marcobonzanini', ':', 'just', 'an', 'example', '!', ':D', 'http://example.com', '#NLP']

################## Data cleaning variable areas
tweets_data = []
tweets_file = open(tweets_data_path, "r")
terms_bigram = []
com_max = []
count_all = Counter()
count_all_hash = Counter()
count_all_bigram = Counter()
count_search = Counter()
count_donate = Counter()
count_volunteer= Counter()

################## Stop and unwanted words definition

punctuation = list(string.punctuation)

# Extra terms to remove
# rt, RT (retweet), via (retweet)

stop = stopwords.words('english') + punctuation + ['rt','via','gt','https','http','amp','#']

################## Count word frequency and co-occurence

for line in tweets_file:

    try:

        tweet= json.loads(line)

        terms_stops = [term.lower() for term in preprocess(tweet['text']) if term.lower() not in stop ]

#### After encode into utf-8, there are null characters such as '\xe2\x80\xa6', '\xed\xa0\xbd'.  So we try to exclude them.

        terms_stops_utf=[x.decode('unicode_escape').encode('utf-8','ignore') for x in terms_stops]

#### Count bigram frequency

        terms_bigram = list(bigrams(terms_stops_utf))
        
#### Count hash tag only frequency:

        terms_hash = [hash for hash in terms_stops_utf if hash.startswith('#') ]

        count_all.update(terms_stops_utf)
        
        count_all_hash.update(terms_hash)
        
        count_all_bigram.update(terms_bigram)

#### Count key word co-occurence

        if donate_word in terms_stops_utf:
            
            count_donate.update(terms_stops_utf)

        if volunteer_word in terms_stops_utf:

            count_volunteer.update(terms_stops_utf)
        
    except:
        continue

#### Define output text files and figures

def common_text_plot_output(count,output_file,rotation_angle,y_lable_text,title_text,fig_output_name):

    # Write output files

    most_common_100= count.most_common(100)

    most_common_25= count.most_common(25)

    most_common_output = open(output_file, 'w')

    most_common_output.write("%s\n" % '\n '.join(map(str, most_common_100)))

    most_common_output.close()

    # Plot the most common words/bigrams/hashtags

    words = [x[0] for x in most_common_25]

    values = [int(x[1]) for x in most_common_25]

    width=0.6
    
    mybar = plt.bar(range(len(words)), values, color='green', alpha=0.4)
    
    ax = plt.axes()
    
    x_pos = list(range(len(words)))
    
    ax.set_xticks([p + 0.4 * width for p in x_pos])
    
    ax.set_xticklabels(words, rotation=rotation_angle, fontsize=12) # make the most common word as angled labels
    
    plt.ylabel(y_lable_text,fontsize=20)
    
    plt.title(title_text,fontsize=20)
    
    plt.legend()
    
    plt.tight_layout()  # Give the x axis label more space
    
    plt.savefig(fig_output_name)
    
    plt.close()

    return

#### Define output text files

def common_text_output(count,output_file):

    # Write output files

    most_common_100= count.most_common(100)

    most_common_25= count.most_common(25)

    most_common_output = open(output_file, 'w')

    most_common_output.write("%s\n" % '\n '.join(map(str, most_common_100)))

    most_common_output.close()

    return

#### The most common single words outputs

#common_info_output(count, output_file, plot: x-axis legend rotation_angle, plot: y_lable_text, plot: title_text):

common_text_plot_output(count_all,the_most_common_word_file,'50','Word Count','Hillary Related Tweets: The 25 Most Common Word Chart',the_most_common_word_plot)

#### The most common hash tags outputs

#common_info_output(count, output_file, plot: x-axis legend rotation_angle, plot: y_lable_text, plot: title_text):

common_text_plot_output(count_all_hash,the_most_common_hash_file,'70','Hashtag Count','Hillary Related Tweets: The 25 Most Common Hashtags Chart',the_most_common_hash_plot)

#### The most common 100 bigrams

#common_info_output(count, output_file, plot: x-axis legend rotation_angle, plot: y_lable_text, plot: title_text):

common_text_plot_output(count_all_bigram,the_most_common_bigram_file,'55','Bigram Count','Hillary Related Tweets: The 25 Most Common Bigrams Chart',the_most_common_bigram_plot)


#### The most common 100 bigrams

#common_text_output(count,output_file)

common_text_output(count_search,the_most_common_key_word_count_file)


#### The most common donate words with the key words

#common_text_output(count,output_file)

common_text_output(count_donate,the_most_common_donate_word_count_file)


# The most common volunteer words with the key words

#common_text_output(count,output_file)

common_text_output(count_volunteer,the_most_common_volunteer_word_count_file)


elapsedTime = time.time()-startTime

print elapsedTime

    


