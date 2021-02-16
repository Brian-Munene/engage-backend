from routes import db
import datetime


class Company(db.Model):
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    company_name = db.Column(db.String(50), nullable=False, unique=True)
    company_code = db.Column(db.String(70), nullable=False, unique=True)
    company_head = db.Column(db.String(70), nullable=False)
    company_size = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    # Relationships
    surveys = db.relationship('Survey', backref='companies', lazy=True)

    def __init__(self, public_id, company_name, company_code, company_head, company_size):
        self.company_name = company_name
        self.public_id = public_id
        self.company_code = company_code
        self.company_head = company_head
        self.company_size = company_size
        self.created_at = datetime.datetime.today()
