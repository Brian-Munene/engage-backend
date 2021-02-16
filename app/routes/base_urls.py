from flask import Flask, flash, redirect, url_for, session, logging, request, jsonify

#File imports
from routes import app


@app.route('/index')
@app.route('/')
def index():
	#return "Brian"
    return jsonify('Welcome to Employee Engagement'), 200


@app.errorhandler(404)
def page_not_found(e):
    response = []
    response.append("Nothing to see here...")
    print(e)
    return jsonify({'message': response}), 404
