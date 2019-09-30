from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


# Development database_uri
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:motongoria@127.0.0.1:5432/employee-engagement"

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import Routes
from routes import base_urls, user_urls, google_login_url, company_urls, survey_urls, survey_responses_url

