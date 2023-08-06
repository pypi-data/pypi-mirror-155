from flask import request
from flask_restx import Resource, fields, reqparse
from ...db.db_connection import database_access
from ...namespace import api
import logging
from ...response_helper import get_response
import json
from bson import json_util
from flask_jwt_extended import jwt_required
from ..login_register.login import token_required

get_rolesPrivileges = reqparse.RequestParser()
get_rolesPrivileges.add_argument("role_name", type=str, required=True)
get_rolesPrivileges.add_argument("page_no", type=int, required=True, help="Page number")
get_rolesPrivileges.add_argument("page_limit", type=int, required=True, help="limit ")

delete_rolesPrivileges = reqparse.RequestParser()
delete_rolesPrivileges.add_argument("role_name", type=str, required=True)

get_allRolesPrivileges = reqparse.RequestParser()
get_allRolesPrivileges.add_argument("page_no", type=int, required=True, help="Page number")
get_allRolesPrivileges.add_argument("page_limit", type=int, required=True, help="limit ")


post_rolesPrivileges = api.model("AddRolePrivileges", {
	"stage": fields.String,
	"dashboard": fields.String,
	"role_name": fields.String,
	"privileges": fields.Raw(
		[], required="true",
		example=[
			{
				"roles": [
					{
						"read": "true",
						"write": "false"
					}
				]
			},
			{
				"create_violation": [
					{
						"read": "true",
						"write": "true"
					}
				]
			},
			{
				"customize_form": [
					{
						"read": "true",
						"write": "true"
					}
				]
			},
			{
				"view_users": [
					{
						"read": "true",
						"write": "true"
					}
				]
			},
			{
				"fingerprint_auth": [
					{
						"read": "true",
						"write": "false"
					}
				]
			},
			{
				"add-new-profile": [
					{
						"read": "true",
						"write": "false"
					}
				]
			},
			{
				"edit-profile": [
					{
						"read": "true",
						"write": "false"
					}
				]
			},
			{
				"view-profiles": [
					{
						"read": "true",
						"write": "false"
					}
				]
			},
			{
				"view-profile": [
					{
						"read": "true",
						"write": "false"
					}
				]
			}
		]
	)
})


class AddRolePrivileges(Resource):
	@token_required
	@api.expect(get_rolesPrivileges)
	def get(self, *args):
		try:
			role_name = request.args.get("role_name")
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			data = rolesPrivileges_col.find({"role_name": role_name})
			if len(list(data)):
				data = rolesPrivileges_col.find({"role_name": role_name}).skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				_response = get_response(404)
				_response["data"] = []
				_response["count"] = 0
				return _response
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Find Roles and Privileges'
			logging.error(e)
			return _response

	@token_required
	@api.expect(post_rolesPrivileges)
	def post(self, *args):
		args = request.get_json()
		try:
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			data = rolesPrivileges_col.find_one({"role_name": args["role_name"]})
			print(data)
			if not data:
				rolesPrivileges_col.insert_one(
					{"stage": args["stage"],"dashboard": args["dashboard"], "role_name": args["role_name"], "privileges": args["privileges"]})
				logging.info(get_response(200))
				return get_response(200)
			else:
				_response = get_response(409)
				_response["data"] = []
				return _response
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Roles and Privileges'
			logging.error(e)
			return _response

	@token_required
	@api.expect(post_rolesPrivileges)
	def put(self, *args):
		args = request.get_json()
		try:
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			data = rolesPrivileges_col.find_one({ "role_name": args["role_name"]})
			if data:
				rolesPrivileges_col.update_one(
					{ "role_name": args["role_name"]}, {'$set': {"privileges": args["privileges"], "role_name": args["role_name"], "dashboard": args["dashboard"],"stage": args["stage"]}})
				logging.info(get_response(200))
				return get_response(200)
			else:
				_response = get_response(404)
				_response["data"] = []
				_response["count"] = 0
				return _response
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Update Roles and Privileges'
			logging.error(e)
			return _response

	@token_required
	@api.expect(delete_rolesPrivileges)
	def delete(self, *args):
		args = delete_rolesPrivileges.parse_args()
		try:
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			data = rolesPrivileges_col.find_one({"role_name": args["role_name"]})
			if data:
				rolesPrivileges_col.delete_one({"role_name": args["role_name"]})
				logging.info(get_response(200))
				return get_response(200)
			else:
				_response = get_response(404)
				_response["data"] = []
				_response["count"] = 0
				return _response
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Delete Roles and Privileges'
			logging.error(e)
			return _response


class GetAllRolesPrivileges(Resource):
	@token_required
	@api.expect(get_allRolesPrivileges)
	def get(self, *args):
		try:
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			data = rolesPrivileges_col.find()
			count = rolesPrivileges_col.count_documents({})
			if len(list(data)):
				_response = get_response(200)
				data = rolesPrivileges_col.find().skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
				print(data)
				_response["data"] = json.loads(json_util.dumps(data))
				_response["count"] = json.loads(json_util.dumps(count))

				return _response
			else:
				_response = get_response(404)
				_response["data"] = []
				_response["count"] = 0
				return _response
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Find Roles and Privileges'
			logging.error(e)
			return _response


class AllRolesPrivileges(Resource):
	@token_required
	@api.expect(get_allRolesPrivileges)
	def get(self, *args):
		try:
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			database_connection = database_access()
			rolesPrivileges_col = database_connection["roles&privileges"]
			data = rolesPrivileges_col.find()
			count=rolesPrivileges_col.count_documents({})
			if len(list(data)):
				_response = get_response(200)
				data = rolesPrivileges_col.find().skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
				print(data)
				_response["data"] = json.loads(json_util.dumps(data))
				_response["count"] = json.loads(json_util.dumps(count))
				return _response
			else:
				_response = get_response(404)
				_response["data"] = []
				_response["count"] = 0
				return _response
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Find Roles and Privileges'
			logging.error(e)
			return _response