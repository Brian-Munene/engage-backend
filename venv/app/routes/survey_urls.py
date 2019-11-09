from flask import Flask, jsonify, url_for, request
import uuid
import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt

# File imports
from database.survey import Survey
from database.user import User
# from database.company import Company
from routes import app, db


@app.route('/create_survey', methods=['POST'])
@jwt_required
def create_survey():
    if request.method == 'POST':
        request_json = request.get_json()
        public_id = str(uuid.uuid4())
        name = request_json.get('name')
        description = request_json.get('description')
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        company = Company.query.filter_by(company_code=user.company_code).first()
        if not company.company_id:
            return jsonify({'message': 'Company does not exist'})
        q0 = request_json.get('question0')
        q1 = request_json.get('question1')
        q2 = request_json.get('question2')
        q3 = request_json.get('question3')
        q4 = request_json.get('question4')
        q5 = request_json.get('question5')
        survey = Survey(public_id, name, description, company.company_id, q0, q1, q2, q3, q4, q5)
        db.session.add(survey)
        db.session.commit()
        response_object = {
            'message': 'Survey Created successfully',
            'name': survey.name,
            'description': survey.description,
            'public_id': survey.public_id
        }
        return jsonify(response_object), 200


@app.route('/surveys', methods=['GET'])
@jwt_required
def view_all_surveys():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    company = Company.query.filter_by(company_code=user.company_code).first()
    surveys = Survey.query.filter_by(company_id=company.company_id).all()
    if surveys:
        surveys_list = []
        for survey in surveys:
            survey_dict = {
                'name':        survey.name,
                'public_id':   survey.public_id,
                'description': survey.description,
                'company_id':  survey.company_id
            }
            surveys_list.append(survey_dict)
        return jsonify(surveys_list), 200
    else:
        return jsonify({'message': 'No survey available'}), 404


@app.route('/survey/<public_id>', methods=['GET'])
@jwt_required
def view_single_survey(public_id):
    if request.method == 'GET':
        survey = Survey.query.filter_by(public_id=public_id).first()
        if survey:
            survey_dict = {
                'name':        survey.name,
                'public_id':   survey.public_id,
                'description': survey.description,
                'company_id': survey.company_id,
                'q0': survey.question_0,
                'q1': survey.question_1,
                'q2': survey.question_2,
                'q3': survey.question_3,
                'q4': survey.question_4,
                'q5': survey.question_5,
            }
            return jsonify(survey_dict), 200
        else:
            return jsonify({'message': 'Survey does not exist'}), 404

