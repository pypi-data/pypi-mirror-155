import logging
from flask import request, Flask
from ...db.db_connection import database_access
from flask_restx import Resource, fields
from ...namespace import api
from ...response_helper import get_response
import hashlib
import jwt
from datetime import datetime, timedelta

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'cc6e455f0b76439d99cc8e1669232518'

super_login = api.model("SuperLogin", {
	"email": fields.String,
	"password": fields.String})
role = "super_admin"
dashboard = "both_dashboard"
first_name = "Admin"
privileges = [{
	"Roles_Privileges":
		[
			{
				"read": "true",
				"write": "true"
			}
		]
},
	{
		"Users": [
			{
				"read": "true",
				"write": "true"
			}
		]
	},
	{
		"Create_Violation": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Customize_Form": [
			{
				"read": "true",
				"write": "true"
			}
		]
	},
	{
		"Checklist_Master": [
			{
				"read": "true",
				"write": "true"
			}
		]
	},{
		"Checklist_Configure": [
			{
				"read": "true",
				"write": "true"
			}
		]
	},{
		"Checklist_Approval": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Checklist_History": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Fingerprint_Authentication": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Fingerprint_Enrollment": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Add_New_Profile": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"View_Profiles": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Edit_Profile": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}, {
		"Person_Profile": [
			{
				"read": "true",
				"write": "true"
			}
		]
	},{
		"Security_Checklist": [
			{
				"read": "true",
				"write": "true"
			}
		]
	}]


class SuperLogin(Resource):
	@api.expect(super_login, validate=True)
	def post(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			dms_super_admin = database_connection["dms_super_admin"]
			password = hashlib.md5("dmsautoplant@987".encode('utf-8')).digest()
			data = dms_super_admin.find_one({"email": args["email"]})
			if data:
				if data["password"] == password:
					_response = get_response(200)
					session_id = jwt.encode({
						'email': data['email'],
						'exp': datetime.utcnow() + timedelta(days=1)
					}, flask_app.config['SECRET_KEY'])
					_response["session_id"] = session_id
					_response["email"] = data["email"]
					_response["role"] = role
					_response["first_name"] = first_name
					_response["dashboard"] = dashboard
					_response["privileges"] = privileges
					return _response
				else:
					logging.error(get_response(401))
					return get_response(401)
			else:
				logging.error(get_response(404))
				return get_response(404)
		except Exception as e:
			logging.error(e)
