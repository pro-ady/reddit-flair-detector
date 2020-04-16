import sys
import praw
import pandas as pd
import numpy as np
import string
import pickle
import os

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

import warnings
warnings.filterwarnings("ignore")

def process_url(URL):
    url = str(URL)
    
    if('/r/india/comments/' in url):
        count = 0
        final_string = ''
        
        for i in range(len(url)):
            if url[i] == '/':
                count += 1
                
            elif count == 5:
                final_string += url[i]
        split_words = final_string.split('_')
        final_title = ' '.join(word for word in split_words)
        
        return str(final_title)
    else:
        # print("Exception")
        return words


# Using Existing stopwords
nltk.download("stopwords", quiet=True)
stopwords = stopwords.words('english')

# Adding new stopwords to the Set
full_stopwords = ["says", "help", "wrote", "https", "http", "like", "19", "com", "www", "use", "ve",
	              "just", "does", "don", "t", "did"]
stopwords.extend(full_stopwords)

nltk.download("wordnet", quiet=True)
lemmatizer = WordNetLemmatizer()
tokenizer  = RegexpTokenizer(r'\w+')

def cleanText(text):
	text = str(text);

	tokens = tokenizer.tokenize(text)
	post = [lemmatizer.lemmatize(post) for post in tokens]
	text = " ".join(post)
	return text


def getData_usingPraw(URL):
	# INITIALISING PRAW INSTANCES
	# AS WELL AS CREATE AN OBJECT FOR THE SUBREDDIT
	reddit = praw.Reddit(client_id='bDeE8HyIL4WqVw',
                        	client_secret='R0X7ghLgpVwIjTyGdJPgJwF5rG4',
                        	user_agent='reddit-flair-detector',
                        	username='culifer_time')

	info_post = reddit.submission(url=str(URL))
	info_post.comments.replace_more(limit=0)
	posts = []

	comments = ""
	comment_limit = 50
	i = 0
	for comment in info_post.comments.list():
		comments += comment.body + " "
		i = i+1
		if(i > comment_limit):
			break

	posts.extend([info_post.title, 
				info_post.selftext, 
				comments, 
				info_post.permalink, 
				info_post.link_flair_text])

	posts[0] = cleanText(posts[0])
	posts[1] = cleanText(posts[1])
	posts[2] = cleanText(posts[2])
	posts[3] = process_url(posts[3])

	s = ""
	s = posts[0] + " " + posts[1] + " " + posts[2] + " " + posts[3]

	s = cleanText(s)

	return s,posts[4]



# url_string = sys.argv[1]
# X_test,flair_text = getData_usingPraw(url_string)

# dirname = os.path.dirname(__file__)
# filename = os.path.join(dirname, '../models/CVRF_allParams.sav')
# loaded_model = pickle.load(open(filename, 'rb'))

# result = loaded_model.predict([X_test])

# print(str(result[0]))
# # print("Hello ALL")
# sys.stdout.flush()

# print(os.path.dirnamse(__file__))