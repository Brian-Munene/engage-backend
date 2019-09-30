from flask import Flask, jsonify, url_for, request
import uuid

# File imports
from database.survey_response import SurveyResponse
from database.survey import Survey
from routes import app, db


@app.route('/create_response/<public_id>', methods=['POST'])
def create_response(public_id):
    if request.method == 'POST':
        survey = Survey.query.filter_by(public_id=public_id).first()
        if survey:
            request_json = request.get_json()
            public_id = str(uuid.uuid4())
            response = request_json.get('response')
            user_id = request_json.get('user_id')
            survey_response = SurveyResponse(public_id, response, user_id)
            db.session.add(survey_response)
            db.session.commit()
            response_object = {
                'public_id': survey_response.public_id,
                'response': survey_response.response
            }
            return jsonify(response_object), 201
        else:
            return jsonify({'message': 'The survey does not exist'}), 404
