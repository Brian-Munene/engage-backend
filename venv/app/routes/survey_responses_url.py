from flask import Flask, jsonify, url_for, request
import uuid
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

# File imports
from database.survey_response import SurveyResponse
from database.survey import Survey
from routes import app, db


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
            survey_response = SurveyResponse(public_id, response, response1, response2, response3, response4, response5, survey_id)
            db.session.add(survey_response)
            db.session.commit()
            response_object = {
                'public_id': survey_response.public_id,
                'response': survey_response.response
            }
            return jsonify(response_object), 201
        else:
            return jsonify({'message': 'The survey does not exist'}), 404


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



