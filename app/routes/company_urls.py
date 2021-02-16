from flask import Flask, jsonify, url_for, request
import uuid
from flask_jwt_extended import (jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

# File imports
from database.company import Company
from database.survey import Survey
from database.survey_response import SurveyResponse
from database.user import User
from routes import app, db


@app.route('/register_company', methods=['POST'])
@jwt_required
def register_company():
    if request.method == 'POST':
        request_json = request.get_json()
        public_id = str(uuid.uuid4())
        company_name = request_json.get('company_name')
        company_code = str(uuid.uuid4())
        company_head = request_json.get('company_head')
        company_size = request_json.get('company_size')
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        if user.role == 'admin':
            company = Company(public_id, company_name, company_code, company_head, company_size)
            db.session.add(company)
            db.session.commit()
            response_object = {
                'public_id': public_id,
                'name':      company_name,
                'head':      company_head,
                'size':      company_size,
                'code':      company_code
            }
            return jsonify(response_object), 200
        else:
            return jsonify({'message': 'You cannot register a company'}), 400


@app.route('/companies', methods=['GET'])
def companies():
    companies = Company.query.all()
    if not companies:
        return jsonify({'message': 'There are no companies available at the moment'}), 400
    companies_list = []
    for company in companies:
        company_dict = {
            'name': company.company_name,
            'code': company.company_code,
            'public_id': company.public_id
        }
        companies_list.append(company_dict)
    return jsonify(companies_list), 200


@app.route('/company/<public_id>', methods=['GET'])
@jwt_required
def company_details(public_id):
    company = Company.query.filter_by(public_id=public_id).first()
    if company:
        response_object = {'name': company.company_name,
                           'code': company.company_code,
                           'head': company.company_head,
                           'size': company.company_size}
        return jsonify(response_object), 200
    else:
        return jsonify({'message': 'Company not found'}), 400


@app.route('/company_surveys/<public_id>', methods=['GET'])
@jwt_required
def company_surveys(public_id):
    company = Company.query.filter_by(public_id=public_id).first()
    if not company:
        return jsonify({'message': 'Company Details are unavailable.'}), 500
    surveys = Survey.query.filter_by(company_id=company.company_id).all()
    if not surveys:
        return jsonify({'message': 'No surveys found'}), 404
    survey_list = []
    for survey in surveys:
        survey_response = SurveyResponse.query.filter_by(survey_id=survey.survey_id).all()
        survey_response_dict = {
            'response_id': survey_response.response_id,
            'public_id': survey_response.public_id,
            'survey_id': survey_response.survey_id,
            'created_at': survey_response.created_at
        }
        survey_list.append(survey_response_dict)
    return jsonify({'survey_responses': survey_list}), 200


@app.route('/companies', methods=['GET'])
def get_all_companies():
    companies = Company.query.all()
    if companies:
        companies_list = []
        for company in companies:
            company_dict = {
                'name': company.company_name,
                'code': company.company_code,
                'public_id': company.public_id,
                'size': company.company_size,
                'head': company.company_head
            }
            companies_list.append(company_dict)
        return jsonify(companies_list), 200
    else:
        return jsonify({'message': 'No companies found'}), 400
