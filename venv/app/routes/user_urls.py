from flask import Flask, jsonify, url_for, request
from datetime import datetime, timedelta
import uuid

# File imports
from database.user import User
from routes import app, db


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        request_json = request.get_json()
        name = request_json.get('name')
        email = request_json.get('email')
        password = request_json.get('password')
        company_code = request_json.get('company_code')
        user_public_id = str(uuid.uuid4())
        user = User(user_public_id, name, email, company_code)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        response_object = {}
        response_object['message'] = 'Register Successful'
        response_object['name'] = user.name
        response_object['email'] = user.email
        return jsonify(response_object), 200


@app.route('/login', methods=['POST'])
def login():
    try:
        request_json = request.get_json()
        email = request_json.get('email')
        password = request_json.get('password')
        if email is None or password is None:
            return jsonify({'error': 'No data provided'}), 400
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            app.logger.info('{0}successful log in at {1}'.format(user.user_id, datetime.now()))
            response_object = {
                "message": "Login Successful",
                "public_id": user.public_id,
                "email": user.email,
                "name": user.name
            }
            return jsonify(response_object), 200
        else:
            return jsonify({'error': 'Username or password not found'}), 400
    except(Exception, NameError, TypeError, RuntimeError, ValueError) as identifier:
        response_object = {
            'status': str(identifier),
            'message': 'Try again @login',
            'user': email
        }
        return jsonify(response_object), 500
    except NameError as name_identifier:
        response_object = {
            'status': str(name_identifier),
            'message': 'Try again @login',
            'error': 'Name',
            'username': email
        }
        return jsonify(response_object), 500
    except TypeError as type_identifier:
        response_object = {
            'status': str(type_identifier),
            'message': 'Try again @login',
            'error': 'Type',
            'username': email
        }
        return jsonify(response_object), 500
    except RuntimeError as run_identifier:
        response_object = {
            'status': str(run_identifier),
            'message': 'Try again @login',
            'error': 'Runtime',
            'username': email
        }
        return jsonify(response_object), 500
    except ValueError as val_identifier:
        response_object = {
            'status': str(val_identifier),
            'message': 'Try again @login',
            'error': 'Value',
            'username': email
        }
        return jsonify(response_object), 500
    except Exception as exc_identifier:
        response_object = {
            'status': str(exc_identifier),
            'message': 'Try again @login',
            'error': 'Exception',
            'username': email
        }
        return jsonify(response_object), 500
