import jwt

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask import current_app as app


JWT_ALGO = 'HS256'


def generate_auth_token(id, name, user_type, expiration=3600):
    """
    Generates a secure token for the user
    :param id: user id
    :param name: user name
    :param user_type: user type
    :param expiration: ttl in seconds
    :return: token as encoded string
    """
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': id, 'name': name, 'user_type': user_type})


def verify_auth_token(token):
    """
    Verifies and decodes th token
    :param token: Encoded token
    :return: decoded token as dict
    """
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    return data


def generate_jwt(**payload):
    """Generate JWT for payload."""
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm=JWT_ALGO).decode('utf-8')


def decode_jwt(token):
    """Decode JWT payload."""
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=[JWT_ALGO])
    except jwt.exceptions.DecodeError:
        return None
