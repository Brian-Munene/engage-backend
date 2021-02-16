from routes import db
import datetime


class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'

    response_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    response = db.Column(db.String(255), nullable=False)
    emotion = db.Column(db.String(50), nullable=False)
    response1 = db.Column(db.String(255), nullable=False)
    emotion1 = db.Column(db.String(50), nullable=False)
    response2 = db.Column(db.String(255), nullable=False)
    emotion2 = db.Column(db.String(50), nullable=False)
    response3 = db.Column(db.String(255), nullable=False)
    emotion3 = db.Column(db.String(50), nullable=False)
    response4 = db.Column(db.String(255), nullable=False)
    emotion4 = db.Column(db.String(50), nullable=False)
    response5 = db.Column(db.String(255), nullable=False)
    emotion5 = db.Column(db.String(50), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'), nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    # Relationships

    def __init__(self, public_id, response, emotion, response1, emotion1, response2, emotion2, response3, emotion3,
                 response4, emotion4, response5, emotion5, survey_id):
        self.response = response
        self.emotion = emotion
        self.response1 = response1
        self.emotion1 = emotion1
        self.response2 = response2
        self.emotion2 = emotion2
        self.response3 = response3
        self.emotion3 = emotion3
        self.response4 = response4
        self.emotion4 = emotion4
        self.response5 = response5
        self.emotion5 = emotion5
        self.public_id = public_id
        self.survey_id = survey_id
        self.created_at = datetime.date.today()
