from routes import db, app
from passlib.apps import custom_app_context as pwd_context
import datetime
import jwt


def encode_auth_token(user_id):
    """
    Generate Auth Token
    :param public_id:
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3, seconds=33),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


class User(db.Model):
    __tablename__ = 'users'

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes Auth Token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. PLease log in again.'

    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(70), nullable=False, unique=True)
    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(70), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(45), nullable=False)
    company_code = db.Column(db.String(70), nullable=True)

    def __init__(self, public_id, name, email, role, company_code):
        self.name = name
        self.public_id = public_id
        self.email = email
        self.role = role
        self.company_code = company_code
