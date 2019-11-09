from flask import Flask, jsonify, url_for, request
import pandas as pd
# import numpy as np
# from nltk.corpus import stopwords
# from textblob import Word
# import re
# from sklearn import preprocessing
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics import accuracy_score
# from sklearn.pipeline import Pipeline
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import GridSearchCV
# import nltk
import pickle
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# from nltk import word_tokenize, sent_tokenize, pos_tag, wordpunct_tokenize
# from nltk.corpus import stopwords
# import string
# nltk.download("stopwords")
# nltk.download("wordnet")
# from textblob import Word
import uuid
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

# File imports
from database.survey_response import SurveyResponse
from database.survey import Survey
from routes import app, db, model, clean_text, decode_response


@app.route('/create_response/<public_id>', methods=['POST'])
@jwt_required
def create_response(public_id):
    if request.method == 'POST':
        survey = Survey.query.filter_by(public_id=public_id).first()
        if survey:
            request_json = request.get_json()
            public_id = str(uuid.uuid4())
            response = request_json.get('response')
            response1 = request_json.get('response1')
            response2 = request_json.get('response2')
            response3 = request_json.get('response3')
            response4 = request_json.get('response4')
            response5 = request_json.get('response5')
            survey_id = survey.survey_id
            responses = pd.DataFrame([response, response1, response2, response3, response4, response5])
            responses = responses.dropna()
            data = clean_text(responses)
            pred = model.best_estimator_.predict(data)
            emotions = decode_response(pred)
            emotion_model = []

            for emotion in emotions:
                emo = emotion
                emotion_model.append(emo)
            emotion = emotion_model[0]
            emotion1 = emotion_model[1]
            emotion2 = emotion_model[2]
            emotion3 = emotion_model[3]
            emotion4 = emotion_model[4]
            emotion5 = emotion_model[5]
            survey_response = SurveyResponse(public_id, response, emotion, response1, emotion1, response2, emotion2,
                                             response3, emotion3, response4, emotion4, response5, emotion5,
                                             survey_id)
            db.session.add(survey_response)
            db.session.commit()
            return jsonify({'message': 'Successfully recorded your response thank you'}), 201
        else:
            return jsonify({'message': 'The survey does not exist'}), 404


# @app.route('/predict', methods=['POST'])
# def predict():
#     model = pickle.load(open('emotion_logreg.pickle', 'rb'))
#     responses = []
#     responses = responses[0].apply(lambda x: x.lower())
    # data = pd.read_csv('text_emotion.csv')
    # data = data.drop('author', axis=1)
    # data = data.drop(data[data.sentiment == 'boredom'].index)
    # data = data.drop(data[data.sentiment == 'empty'].index)
    # data = data.drop(data[data.sentiment == 'fun'].index)
    # data = data.drop(data[data.sentiment == 'relief'].index)
    # data = data.drop(data[data.sentiment == 'surprise'].index)
    # data = data.drop(data[data.sentiment == 'worry'].index)
    # data = data.drop(data[data.sentiment == 'enthusiasm'].index)
    # data = data.drop(data[data.sentiment == 'neutral'].index)
    # data = data.drop(data[data.sentiment == 'love'].index)
    # data = data.drop(data[data.sentiment == 'anger'].index)
    # # Making all letters lowercase
    # data['content'] = data['content'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    # # Removing Punctuation, Symbols
    # data['content'] = data['content'].str.replace('[^\w\s]', ' ')
    # # Removing Stop Words using NLTK
    # stop = stopwords.words('english')
    # data['content'] = data['content'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    # # Lemmatisation
    # data['content'] = data['content'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    # # remove any text starting with User...
    # data['content'] = data['content'].map(lambda x: re.sub("\[\[User.*", '', str(x)))
    # # remove IP addresses or user IDs
    # data['content'] = data['content'].map(lambda x: re.sub("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", '', str(x)))
    # # remove http links in the text
    # data['content'] = data['content'].map(lambda x: re.sub("(http://.*?\s)|(http://.*)", '', str(x)))
    #
    # # Correcting Letter Repetitions
    # def de_repeat(text):
    #     pattern = re.compile(r"(.)\1{2,}")
    #     return pattern.sub(r"\1\1", text)
    # data['content'] = data['content'].apply(lambda x: " ".join(de_repeat(x) for x in x.split()))
    # # Encoding output labels 'sadness' as '1' & 'happiness' as '0'
    # lbl_enc = preprocessing.LabelEncoder()
    # y = lbl_enc.fit_transform(data.sentiment.values)
    # # Splitting into training and testing data in 90:10 ratio
    # X_train, X_test, y_train, y_test = train_test_split(data.content.values, y, stratify=y, random_state=42,
    #                                                     test_size=0.1, shuffle=True)
    # # Code to find the top 10,000 rarest words appearing in the data
    # freq = pd.Series(' '.join(data['content']).split()).value_counts()[-10000:]
    # # Removing all those rarely appearing words from the data
    # freq = list(freq.index)
    # data['content'] = data['content'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
    # logreg_pipe = Pipeline([
    #     ('tvec', TfidfVectorizer()),
    #     ('logreg', LogisticRegression())
    # ])
    #
    # logreg_pipe.fit(X_train, y_train)
    # logreg_params = {
    #     'tvec__max_features':  [100, 2000],
    #     'tvec__ngram_range':   [(1, 1), (1, 2), (2, 2)],
    #     'tvec__stop_words':    [None, 'english'],
    #     'logreg__C':           [1],
    #     'logreg__solver':      ['lbfgs'],
    #     'logreg__multi_class': ['multinomial'],
    #     'logreg__max_iter':    [1000],
    #     'logreg__penalty':     ['l2']
    # }
    # logreg_gs = GridSearchCV(logreg_pipe, param_grid=logreg_params, cv=5, verbose=1, n_jobs=-1)
    # logreg_gs.fit(X_train, y_train)
    # logreg_gs.score(X_train, y_train)
    # logreg_gs.score(X_test, y_test)
    #
    # tweets = pd.DataFrame(['I am very unhappy today! The atmosphere looks gloom',
    #                        'Things are looking great. It was such a perfect day',
    #                        'Success is right around the corner. Lets do this guys',
    #                        'Everything is more beautiful when you experience them with a smile!',
    #                        'Now this is my worst, okay? But I am gonna get better.',
    #                        'I am tired, boss. Tired of being on the road, lonely as a sparrow in the rain. I am tired of all the pain I feel',
    #                        'This is quite depressing. I am filled with sorrow',
    #                        'I am so excited about tonight I cannot wait to get home',
    #                        'His death broke my heart. It was a sad day',
    #                        'He makes me so angry sometimes',
    #                        'I hate working here',
    #                        'I dislike deal with my workmates anymore'])
    #
    # tweets = tweets[0].apply(lambda x: x.lower())
    # print(tweets)
    # logreg_tfid_tweet = logreg_gs.best_estimator_.predict(tweets)
    # print(lbl_enc.inverse_transform(logreg_tfid_tweet))
    # print(tweets)
    #
    # logreg_classifier = open("emotion_logreg.pickle", 'wb')
    # pickle.dump(logreg_gs, logreg_classifier)
    # logreg_classifier.close()


@app.route('/view_all_responses', methods=['GET'])
def view_all_responses():
    responses = SurveyResponse.query.all()
    if responses:
        responses_list = []
        for response in responses:
            response_dict = {
                'survey_id':    response.survey_id,
                'public_id':    response.public_id,
                'date_created': response.date_created
            }
            responses_list.append(response_dict)
        return jsonify(responses_list), 200
    else:
        return jsonify({'message': 'No responses found'}), 404


@app.route('/view_single_survey_responses/<public_id>', methods=['GET'])
def view_single_survey_responses(public_id):
    survey = Survey.query.filter_by(public_id=public_id).first()
    if survey:
        responses = SurveyResponse.query.filter_by(survey_id=survey.survey_id).all()
        if responses:
            response_list = []
            for response in responses:
                response_dict = {
                    'survey_id':    response.survey_id,
                    'public_id':    response.public_id,
                    'date_created': response.date_created
                }
                response_list.append(response_dict)
            return jsonify(response_list), 200
        else:
            return jsonify({'message': 'No responses available'}), 404
    else:
        return jsonify({'message': 'The survey does not exist'}), 404



