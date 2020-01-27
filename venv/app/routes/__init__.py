import nltk as nltk
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import  pickle
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from textblob import Word
import re
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import nltk
import pickle
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, sent_tokenize, pos_tag, wordpunct_tokenize
from nltk.corpus import stopwords
import string
nltk.download("stopwords")
nltk.download("wordnet")
from textblob import Word
# Load Model
model = pickle.load(open('engage-backend/venv/app/routes/emotion_logreg.pickle', 'rb'))
app = Flask(__name__)
CORS(app)


def clean_text(data):
    # remove '\\n'
    data = data[0].map(lambda x: re.sub('\\n', ' ', str(x)))

    # Making all letters lowercase
    data = data.apply(lambda x: " ".join(x.lower() for x in x.split()))

    # Removing Punctuation, Symbols
    data = data.str.replace('[^\w\s]', ' ')

    # Removing Stop Words using NLTK
    stop = stopwords.words('english')
    data = data.apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    # Lemmatisation
    data = data.apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

    # remove any text starting with User...
    data = data.map(lambda x: re.sub("\[\[User.*", '', str(x)))

    # remove IP addresses or user IDs
    data = data.map(lambda x: re.sub("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", '', str(x)))

    # remove http links in the text
    data = data.map(lambda x: re.sub("(http://.*?\s)|(http://.*)", '', str(x)))

    # Correcting Letter Repetitions
    def de_repeat(text):
        pattern = re.compile(r"(.)\1{2,}")
        return pattern.sub(r"\1\1", text)

    data = data.apply(lambda x: " ".join(de_repeat(x) for x in x.split()))
    return data


def decode_response(response):
    emotion_list = []
    for emotion in response:
        if emotion == 0:
            emotion_list.append('happiness')
        elif emotion == 1:
            emotion_list.append('hate')
        elif emotion == 2:
            emotion_list.append('sadness')
    return emotion_list
# Development database_uri
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:motongoria@127.0.0.1:5432/employee-engagement"

# Production Url
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://gbflabtamgibih:545172c3d798f194bb235abbb58def05ad798bb8c43cf7890f5da4fed7e6527e@ec2-54-243-44-102.compute-1.amazonaws.com:5432/d4n2pafqrnnn91"

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import Routes
from routes import base_urls, user_urls, google_login_url, company_urls, survey_urls, survey_responses_url

