from api import auth
from flask import make_response, jsonify, g
from api.models import User


@auth.error_handler
def unauthorized():
    return make_response(jsonify({
        "state": 403,
        'message': 'Unauthorized access'}), 403)


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True
