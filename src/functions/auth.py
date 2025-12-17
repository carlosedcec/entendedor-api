from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timezone, timedelta

class AuthHelper():

    SECRET_KEY = "your-secret-key-change-this"

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password, hash):
        return check_password_hash(hash, password)

    @staticmethod
    def generate_token(user_id, expires_in=7200):
        payload = {
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        }
        return jwt.encode(payload, AuthHelper.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, AuthHelper.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None