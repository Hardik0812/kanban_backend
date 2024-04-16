from datetime import datetime, timedelta
import os
import jwt
import random

def generate_token(email=None, token_time=None):
    try:
        exp_time = datetime.now() + timedelta(minutes=token_time)
        JWT_PAYLOAD = {"email": email, "exp": exp_time}
        jwt_token = jwt.encode(JWT_PAYLOAD, os.getenv("SECRET_KEY"), algorithm="HS256")
        return jwt_token
    except Exception as e:
        print(f"Error generating token: {e}")
        return None


def decode_token(token):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms="HS256")
        return payload
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None

def generate_otp():
    otp = random.randint(100000,900000)
    return otp