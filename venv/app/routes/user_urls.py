from flask import Flask, jsonify, url_for, request
from datetime import datetime, timedelta
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
import uuid

# File imports
from database.user import User
from database.revoked_token import RevokedToken
from database.company import Company
from routes import app, db


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        request_json = request.get_json()
        name = request_json.get('name')
        email = request_json.get('email')
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'The email has already been registered'}), 401
        password = request_json.get('password')
        company_code = request_json.get('company_code')
        if not Company.query.filter_by(company_code=company_code).first():
            return jsonify({'message': 'The company code is invalid'}), 401
        user_public_id = str(uuid.uuid4())
        user = User(user_public_id, name, email, company_code)
        user.hash_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            response_object = {}
            response_object['message'] = 'Register of {} was Successful'.format(user.email)
            response_object['access_token'] = access_token
            response_object['refresh_token'] = refresh_token
            return jsonify(response_object), 200
        except:
            return jsonify({'message': 'Something went wrong'}), 500


@app.route('/login', methods=['POST'])
def login():
    request_json = request.get_json()
    email = request_json.get('email')
    password = request_json.get('password')
    try:
        if email is None or password is None:
            return jsonify({'error': 'No data provided'}), 400
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            app.logger.info('{0}successful log in at {1}'.format(user.user_id, datetime.now()))
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            response_object = {
                "message":       "Login Successful",
                'access_token':  access_token,
                'refresh_token': refresh_token
            }
            return jsonify(response_object), 200
        else:
            return jsonify({'error': 'Email or password not found'}), 400
    except(Exception, NameError, TypeError, RuntimeError, ValueError) as identifier:
        response_object = {
            'status':  str(identifier),
            'message': 'Try again @login',
            'user':    email
        }
        return jsonify(response_object), 500
    except NameError as name_identifier:
        response_object = {
            'status':   str(name_identifier),
            'message':  'Try again @login',
            'error':    'Name',
            'username': email
        }
        return jsonify(response_object), 500
    except TypeError as type_identifier:
        response_object = {
            'status':   str(type_identifier),
            'message':  'Try again @login',
            'error':    'Type',
            'username': email
        }
        return jsonify(response_object), 500
    except RuntimeError as run_identifier:
        response_object = {
            'status':   str(run_identifier),
            'message':  'Try again @login',
            'error':    'Runtime',
            'username': email
        }
        return jsonify(response_object), 500
    except ValueError as val_identifier:
        response_object = {
            'status':   str(val_identifier),
            'message':  'Try again @login',
            'error':    'Value',
            'username': email
        }
        return jsonify(response_object), 500
    except Exception as exc_identifier:
        response_object = {
            'status':   str(exc_identifier),
            'message':  'Try again @login',
            'error':    'Exception',
            'username': email
        }
        return jsonify(response_object), 500


@app.route('/token_refresh', methods=['POST'])
@jwt_refresh_token_required
def token_refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return {
               'access_token': access_token
           }, 200


@app.route('/logout', methods=['POST'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    try:
        revoked_token = RevokedToken(jti=jti)
        revoked_token.add()
        return {'message': 'Access Token has been revoked'}, 200
    except:
        return {'message': 'Something went wrong'}, 500


@app.route('/logout_refresh', methods=['POST'])
@jwt_refresh_token_required
def logout_refresh():
    jti = get_raw_jwt()['jti']
    try:
        revoked_token = RevokedToken(jti=jti)
        revoked_token.add()
        return {'message': 'Refresh token has been revoked'}
    except:
        return {'message': 'Something went wrong'}, 500
