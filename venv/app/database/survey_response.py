from routes import db
import datetime


class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'

    response_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    response = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'), nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    # Relationships

    def __init__(self, public_id, response, user_id, survey_id):
        self.response = response
        self.public_id = public_id
        self.user_id = user_id
        self.survey_id = survey_id
        self.date_created = datetime.date.today()
