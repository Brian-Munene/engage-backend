from flask import Flask, jsonify, url_for, request
from sqlalchemy import func
import pandas as pd
import uuid
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

# File imports
from database.survey_response import SurveyResponse
from database.survey import Survey
from database.user import User
from database.company import Company
from routes import app, db, model, clean_text, decode_response


@app.route('/create_response/<public_id>', methods=['POST'])
@jwt_required
def create_response(public_id):
    if request.method == 'POST':
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        if user:
            company = Company.query.filter_by(company_code=user.company_code).first()
            survey = Survey.query.filter_by(company_id=company.company_id, public_id=public_id).first()
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
                survey_response = SurveyResponse(public_id, response, emotion, response1, emotion1, response2,
                                                 emotion2,
                                                 response3, emotion3, response4, emotion4, response5, emotion5,
                                                 survey_id)
                db.session.add(survey_response)
                db.session.commit()
                return jsonify({'message': 'Successfully recorded your response'}), 201

            else:
                return jsonify({'message': 'The survey does not exist'}), 404
        else:
            return jsonify({'message': 'User is unavailable'}), 400


@app.route('/view_all_responses', methods=['GET'])
@jwt_required
def view_all_responses():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    users = User.query.filter_by(company_code=user.company_code).all()
    users_count = len(users)
    if user:
        company = Company.query.filter_by(company_code=user.company_code).first()
        if not company:
            return jsonify({'message': 'Company is unavailable'}), 500
        surveys = Survey.query.filter_by(company_id=company.company_id).all()
        if not surveys:
            return jsonify({'message': 'Surveys are unavailable'}), 401
        survey_count = len(surveys)
        total_responses_count = 0
        happiness = 0
        hate = 0
        sadness = 0
        surveys_list = []
        for survey in surveys:
            survey_hate = 0
            survey_happiness = 0
            survey_sadness = 0
            survey_dict = {}
            survey_dict['survey'] = survey.name
            survey_dict['created_at'] = survey.created_at
            responses = SurveyResponse.query.filter_by(survey_id=survey.survey_id).all()
            if not responses:
                return jsonify({'message': 'No responses found'}), 404
            responses_count = len(responses)
            total_responses_count = total_responses_count + responses_count
            for response in responses:
                if response.emotion == 'happiness':
                    happiness = happiness + 1
                    survey_happiness = survey_happiness + 1
                elif response.emotion == 'hate':
                    hate = hate + 1
                    survey_hate = survey_hate + 1
                elif response.emotion1 == 'sadness':
                    sadness = sadness + 1
                    survey_sadness = survey_sadness + 1
                if response.emotion1 == 'happiness':
                    happiness = happiness + 1
                    survey_happiness = survey_happiness + 1
                elif response.emotion1 == 'hate':
                    hate = hate + 1
                    survey_hate = survey_hate + 1
                elif response.emotion1 == 'sadness':
                    sadness = sadness + 1
                    survey_sadness = survey_sadness + 1
                if response.emotion2 == 'happiness':
                    happiness = happiness + 1
                    survey_happiness = survey_happiness + 1
                elif response.emotion2 == 'hate':
                    hate = hate + 1
                    survey_hate = survey_hate + 1
                elif response.emotion2 == 'sadness':
                    sadness = sadness + 1
                    survey_sadness = survey_sadness + 1
                if response.emotion3 == 'happiness':
                    happiness = happiness + 1
                    survey_happiness = survey_happiness + 1
                elif response.emotion3 == 'hate':
                    hate = hate + 1
                    survey_hate = survey_hate + 1
                elif response.emotion3 == 'sadness':
                    sadness = sadness + 1
                    survey_sadness = survey_sadness + 1
                if response.emotion4 == 'happiness':
                    happiness = happiness + 1
                    survey_happiness = survey_happiness + 1
                elif response.emotion4 == 'hate':
                    hate = hate + 1
                    survey_hate = survey_hate + 1
                elif response.emotion4 == 'sadness':
                    sadness = sadness + 1
                    survey_sadness = survey_sadness + 1
                if response.emotion5 == 'happiness':
                    happiness = happiness + 1
                    survey_happiness = survey_happiness + 1
                elif response.emotion5 == 'hate':
                    hate = hate + 1
                    survey_hate = survey_hate + 1
                elif response.emotion5 == 'sadness':
                    sadness = sadness + 1
                    survey_sadness = survey_sadness + 1
            survey_dict['survey_happiness'] = survey_happiness
            survey_dict['survey_hate'] = survey_hate
            survey_dict['survey_sadness'] = survey_sadness
            surveys_list.append(survey_dict)
        return jsonify({'responses_count': total_responses_count,
                        'survey_count':    survey_count,
                        'users_count':     users_count,
                        'hate':            hate,
                        'sadness':         sadness,
                        'happiness':        happiness,
                        'surveys_list':    surveys_list
                        }), 200

    else:
        return jsonify({'message': 'User is unavailable'}), 400


@app.route('/view_single_survey_responses/<public_id>', methods=['GET'])
@jwt_required
def view_single_survey_responses(public_id):
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if user:
        company = Company.query.filter_by(company_code=user.company_code).first()
        survey = Survey.query.filter_by(company_id=company.company_id, public_id=public_id).first()
        survey_name = survey.name
        created_at = survey.created_at
        if survey:
            responses = SurveyResponse.query.filter_by(survey_id=survey.survey_id).all()
            responses_count = len(responses)
            if responses:
                happiness = 0
                hate = 0
                sadness = 0
                for response in responses:
                    if response.emotion == 'happiness':
                        happiness = happiness + 1
                    elif response.emotion == 'hate':
                        hate = hate + 1
                    elif response.emotion1 == 'sadness':
                        sadness = sadness + 1
                    if response.emotion1 == 'happiness':
                        happiness = happiness + 1
                    elif response.emotion1 == 'hate':
                        hate = hate + 1
                    elif response.emotion1 == 'sadness':
                        sadness = sadness + 1
                    if response.emotion2 == 'happiness':
                        happiness = happiness + 1
                    elif response.emotion2 == 'hate':
                        hate = hate + 1
                    elif response.emotion2 == 'sadness':
                        sadness = sadness + 1
                    if response.emotion3 == 'happiness':
                        happiness = happiness + 1
                    elif response.emotion3 == 'hate':
                        hate = hate + 1
                    elif response.emotion3 == 'sadness':
                        sadness = sadness + 1
                    if response.emotion4 == 'happiness':
                        happiness = happiness + 1
                    elif response.emotion4 == 'hate':
                        hate = hate + 1
                    elif response.emotion4 == 'sadness':
                        sadness = sadness + 1
                    if response.emotion5 == 'happiness':
                        happiness = happiness + 1
                    elif response.emotion5 == 'hate':
                        hate = hate + 1
                    elif response.emotion5 == 'sadness':
                        sadness = sadness + 1
                return jsonify({'survey_name': survey_name,
                                'created_at': created_at,
                                'hate': hate,
                                'hapiness': happiness,
                                'sadness': sadness,
                                'responses_count': responses_count
                                }), 200
            else:
                return jsonify({'message': 'No responses available'}), 404
        else:
            return jsonify({'message': 'The survey does not exist'}), 404
    else:
        return jsonify({'message': 'User is unavailable'}), 400


