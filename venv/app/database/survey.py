from routes import db
import datetime


class Survey(db.Model):
    __tablename__ = 'surveys'

    survey_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    question_0 = db.Column(db.String(255), nullable=True)
    question_1 = db.Column(db.String(255), nullable=True)
    question_2 = db.Column(db.String(255), nullable=True)
    question_3 = db.Column(db.String(255), nullable=True)
    question_4 = db.Column(db.String(255), nullable=True)
    question_5 = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.Date, nullable=False)

    # Relationships
    survey_responses = db.relationship('SurveyResponses', backref='surveys', lazy=True)

    def __init__(self, public_id, name, description, question_0, question_1, question_2, question_3, question_4, question_5):
        self.created_at = datetime.date.today()
        self.public_id = public_id
        self.name = name
        self.description = description
        self.question_0 = question_0
        self.question_1 = question_1
        self.question_2 = question_2
        self.question_3 = question_3
        self.question_4 = question_4
        self.question_5 = question_5
