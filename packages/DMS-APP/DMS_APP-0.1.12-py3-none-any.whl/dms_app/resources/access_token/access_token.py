import logging
from flask import request, Flask
from ...db.db_connection import database_access
from flask_restx import Resource, fields, reqparse
from ...response_helper import get_response
import jwt
from datetime import datetime, timedelta
from functools import wraps

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'cc6e455f0b76439d99cc8e1669232518'


def session_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if 'session_id' in request.headers:
			session_id = request.headers['session_id']
		if not session_id:
			_response = get_response(404)
			_response["message"] = "session id is missing"
			return _response
		try:
			data = jwt.decode(jwt=session_id, key=flask_app.config['SECRET_KEY'], algorithms="HS256")
		except jwt.ExpiredSignatureError:
			_response = get_response(404)
			_response["message"] = "token expired"
			return _response
		except:
			_response = get_response(404)
			_response["message"] = "token is Invalid"
			return _response
		return f(*args, **kwargs)
	return decorated


class CreateToken(Resource):
	@session_required
	def post(self):
		try:
			database_connection = database_access()
			token_coll = database_connection["bearer_token"]
			args = request.headers
			token = jwt.encode({
				'session_id': args['session_id'], 'email': args['email'],
				'exp': datetime.utcnow() + timedelta(minutes=30)
			}, flask_app.config['SECRET_KEY'])
			_response = get_response(200)
			_response["access_token"] = token
			access_token = args["email"] + "_" + args['session_id'] + "_" + _response["access_token"]
			token_coll.insert_one({"access_token": access_token})
			return _response
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store User'
			logging.error(e)
			return _response
