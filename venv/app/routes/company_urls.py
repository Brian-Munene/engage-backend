from flask import Flask, jsonify, url_for, request
import uuid
from flask_jwt_extended import (jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

# File imports
from database.company import Company
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
        company = Company(public_id, company_name, company_code, company_head, company_size)
        db.session.add(company)
        db.session.commit()
        response_object = {
            'public_id': public_id,
            'name': company_name,
            'head': company_head,
            'size': company_size,
            'code': company_code
        }
        return jsonify(response_object), 200


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


@app.route('/companies', methods=['GET'])
@jwt_required
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
