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

# The most common single words

most_common_100_words= count_all.most_common(100)

most_common_25_words= count_all.most_common(25)

most_common_word_output = open(the_most_common_word_file, 'w')

most_common_word_output.write("%s\n" % '\n '.join(map(str, most_common_100_words)))

most_common_word_output.close()

# The most common hash tags

most_common_100_hash= count_all_hash.most_common(100)

most_common_25_hash= count_all_hash.most_common(25)

most_common_hash_output = open(the_most_common_hash_file, 'w')

most_common_hash_output.write("%s\n" % '\n '.join(map(str, most_common_100_hash)))

most_common_hash_output.close()

# The most common 100 bigrams

most_common_100_bigrams= count_all_bigram.most_common(100)

most_common_25_bigrams= count_all_bigram.most_common(25)

most_common_bigram_output = open(the_most_common_bigram_file, 'w')

most_common_bigram_output.write("%s\n" % '\n '.join(map(str, most_common_100_bigrams)))

most_common_bigram_output.close()

# The most common 100 bigrams

most_common_100_key_word_cooccurrence= count_search.most_common(100)

most_common_25_key_word_cooccurrence= count_search.most_common(25)

most_common_key_word_cooccurrence_output = open(the_most_common_key_word_count_file, 'w')

most_common_key_word_cooccurrence_output.write("%s\n" % '\n '.join(map(str, most_common_100_key_word_cooccurrence)))

most_common_key_word_cooccurrence_output.close()

# The most common donate words with the key words

most_common_100_donate_word_cooccurrence = count_donate.most_common(100)

most_common_25_donate_word_cooccurrence = count_donate.most_common(25)

most_common_donate_word_cooccurrence_output = open(the_most_common_donate_word_count_file, 'w')

most_common_donate_word_cooccurrence_output.write("%s\n" % '\n '.join(map(str, most_common_100_donate_word_cooccurrence)))

most_common_donate_word_cooccurrence_output.close()

# The most common volunteer words with the key words

most_common_100_volunteer_word_cooccurrence= count_volunteer.most_common(100)

most_common_25_volunteer_word_cooccurrence= count_volunteer.most_common(25)

most_common_volunteer_word_cooccurrence_output = open(the_most_common_volunteer_word_count_file, 'w')

most_common_volunteer_word_cooccurrence_output.write("%s\n" % '\n '.join(map(str, most_common_100_volunteer_word_cooccurrence)))

most_common_volunteer_word_cooccurrence_output.close()

#### Plot the most common words in a bar chart

words = [x[0] for x in most_common_25_words]

values = [int(x[1]) for x in most_common_25_words]

width=0.6
mybar = plt.bar(range(len(words)), values, color='green', alpha=0.4)
ax = plt.axes()
x_pos = list(range(len(words)))
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(words, rotation='50', fontsize=12) # make the most common word as angled labels 
plt.ylabel('Word Count',fontsize=20)
plt.title('Hillary Related Tweets: The 25 Most Common Word Chart',fontsize=20)
plt.legend()
plt.tight_layout()  # Give the x axis label more space
plt.savefig(the_most_common_word_plot)
plt.close()

#### Plot the most common hashs in a bar chart

hash = [z[0] for z in most_common_25_hash]

hash_values = [int(z[1]) for z in most_common_25_hash]

width=0.6
mybar = plt.bar(range(len(hash)), hash_values, color='green', alpha=0.4)
ax = plt.axes()
x_pos = list(range(len(hash)))
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(hash, rotation='70', fontsize=12) # make the most common word as angled labels 
plt.ylabel('Hashtag Count',fontsize=20)
plt.title('Hillary Related Tweets: The 25 Most Common Hashtags Chart',fontsize=20)
plt.legend()
plt.tight_layout()  # Give the x axis label more space
plt.savefig(the_most_common_hash_plot)
plt.close()

#### Plot the most common bigrams in a bar chart

bigram = [a[0] for a in most_common_25_bigrams]

bigram_values = [int(a[1]) for a in most_common_25_bigrams]

width=0.6
mybar = plt.bar(range(len(bigram)), bigram_values, color='green', alpha=0.4)
ax = plt.axes()
x_pos = list(range(len(bigram)))
ax.set_xticks([b + 0.4 * width for b in x_pos])
ax.set_xticklabels(bigram, rotation='55', fontsize=12) # make the most common word as angled labels 
plt.ylabel('Bigram Count',fontsize=20)
plt.title('Hillary Related Tweets: The 25 Most Common Bigrams Chart',fontsize=20)
plt.legend()
plt.tight_layout()  # Give the x axis label more space
plt.savefig(the_most_common_bigram_plot)
##plt.show()

elapsedTime = time.time()-startTime
print elapsedTime

    


