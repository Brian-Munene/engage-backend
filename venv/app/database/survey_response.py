from routes import db
import datetime


class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'

    response_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    response = db.Column(db.String(255), nullable=False)
    response1 = db.Column(db.String(255), nullable=False)
    response2 = db.Column(db.String(255), nullable=False)
    response3 = db.Column(db.String(255), nullable=False)
    response4 = db.Column(db.String(255), nullable=False)
    response5 = db.Column(db.String(255), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'), nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    # Relationships

    def __init__(self, public_id, response, response1, response2, response3, response4, response5, survey_id):
        self.response = response
        self.response1 = response1
        self.response2 = response2
        self.response3 = response3
        self.response4 = response4
        self.response5 = response5
        self.public_id = public_id
        self.survey_id = survey_id
        self.date_created = datetime.date.today()
