from flask import request
from flask_restx import Resource, fields, reqparse
from ...db.db_connection import database_access
from ...namespace import api
from ...response_helper import get_response
import logging
import json
from bson import json_util
from bson.objectid import ObjectId
from ..login_register.login import token_required

delete_checklist_master = reqparse.RequestParser()
delete_checklist_master.add_argument("_id", type=str, required=True)

post_checklist_master = api.model("CheckListMasterAdd", {
	"stages": fields.Raw(
		[],
		required="true",
		example=[
			{
				"applicable_movement": [
					{
						"value": "inbound",
						"label": "Inbound",
					}
				],
				"enable": "enable",
				"applicable_stage": "yard1",
				"mandatory": "yes",
			},
			{
				"applicable_movement": [
					{
						"value": "outbound",
						"label": "Outbound",
					}
				],
				"enable": "enable",
				"applicable_stage": "gate1",
				"mandatory": "no",
			},
		]
	),
	"checklist_details": fields.Raw(
		[],
		required="true",
		example=[
			{
				"checklist_name": "nikhil35",
				"created_by": "super_admin",
				"created_on": "5/24/2022",
				"status": "enabled",
				"checklist_data":
					[{
						"parameter_name": "sdf",
						"data_type": "string",
						"mandatory": "true",
						"critical": "",
						"pass_condition": "",
						"negative_value": "",
						"positive_value": "",
						"include_na": ""},
						{
							"parameter_name": "sdf",
							"data_type": "string[]",
							"mandatory": "true",
							"critical": "yes",
							"pass_condition": "negative",
							"negative_value": "no",
							"positive_value": "good",
							"include_na": "NA"
						}
					]}
		])
})

put_checklist_master = api.model("CheckListMasterUpdate", {
	"_id": fields.String,
	"stages": fields.Raw(
		[],
		required="true",
		example=[
			{
				"applicable_movement": [
					{
						"value": "inbound",
						"label": "Inbound",
					}
				],
				"enable": "enable",
				"applicable_stage": "yard1",
				"mandatory": "yes",
			},
			{
				"applicable_movement": [
					{
						"value": "outbound",
						"label": "Outbound",
					}
				],
				"enable": "enable",
				"applicable_stage": "gate1",
				"mandatory": "no",
			},
		]
	),
	"checklist_details": fields.Raw(
		[],
		required="true",
		example=[
			{
				"checklist_name": "nikhil35",
				"created_by": "super_admin",
				"created_on": "5/24/2022",
				"status": "enabled",
				"checklist_data":
					[{
						"parameter_name": "sdf",
						"data_type": "string",
						"mandatory": "true",
						"critical": "",
						"pass_condition": "",
						"negative_value": "",
						"positive_value": "",
						"include_na": ""},
						{
							"parameter_name": "sdf",
							"data_type": "string[]",
							"mandatory": "true",
							"critical": "yes",
							"pass_condition": "negative",
							"negative_value": "no",
							"positive_value": "good",
							"include_na": "NA"
						}
					]},
		])
})

get_checklist_master = reqparse.RequestParser()
get_checklist_master.add_argument("page_no", type=int, required=True, help="Page number")
get_checklist_master.add_argument("page_limit", type=int, required=True, help="limit ")
get_checklist_master.add_argument("status", type=str, help="Status")
get_checklist_master.add_argument("created_by", type=str, help="Created By")


class CheckListMaster(Resource):
	@token_required
	@api.expect(get_checklist_master)
	def get(self, *args):
		try:
			database_connection = database_access()
			checklist_master_collection = database_connection["dms_checklist_master"]
			args = get_checklist_master.parse_args()
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			if args["status"] and args["created_by"]:
				data = checklist_master_collection.find({"checklist_details.status": args["status"],"checklist_details.created_by": args["created_by"]})
				count = checklist_master_collection.count_documents({"checklist_details.status": args["status"],"checklist_details.created_by": args["created_by"]})
				total_count = checklist_master_collection.count_documents({})
				if len(list(data)):
					data = checklist_master_collection.find({"checklist_details.status": args["status"],"checklist_details.created_by": args["created_by"]}).skip(
						args["page_limit"] * (args["page_no"] - 1)).limit(
						args["page_limit"])
					_response = get_response(200)
					_response["data"] = json.loads(json_util.dumps(data))
					_response["count"] = json.loads(json_util.dumps(count))
					_response["total_count"] = json.loads(json_util.dumps(total_count))
					return _response
				else:
					_response = get_response(404)
					_response["data"] = []
					_response["count"] = 0
					return _response
			elif args["status"]:
				data = checklist_master_collection.find({"checklist_details.status": args["status"]})
				count = checklist_master_collection.count_documents({"checklist_details.status": args["status"]})
				total_count = checklist_master_collection.count_documents({})
				if len(list(data)):
					data = checklist_master_collection.find({"checklist_details.status": args["status"]}).skip(
						args["page_limit"] * (args["page_no"] - 1)).limit(
						args["page_limit"])
					_response = get_response(200)
					_response["data"] = json.loads(json_util.dumps(data))
					_response["count"] = json.loads(json_util.dumps(count))
					_response["total_count"] = json.loads(json_util.dumps(total_count))
					return _response
				else:
					_response = get_response(404)
					_response["data"] = []
					_response["count"] = 0
					return _response
			elif args["created_by"]:
				data = checklist_master_collection.find({"checklist_details.created_by": args["created_by"]})
				count = checklist_master_collection.count_documents(
					{"checklist_details.created_by": args["created_by"]})
				total_count = checklist_master_collection.count_documents({})
				if len(list(data)):
					data = checklist_master_collection.find({"checklist_details.created_by": args["created_by"]}).skip(
						args["page_limit"] * (args["page_no"] - 1)).limit(
						args["page_limit"])
					_response = get_response(200)
					_response["data"] = json.loads(json_util.dumps(data))
					_response["count"] = json.loads(json_util.dumps(count))
					_response["total_count"] = json.loads(json_util.dumps(total_count))
					return _response
				else:
					_response = get_response(404)
					_response["data"] = []
					_response["count"] = 0
					return _response
			else:
				data = checklist_master_collection.find()
				count = checklist_master_collection.count_documents({})
				if len(list(data)):
					data = checklist_master_collection.find().skip(
						args["page_limit"] * (args["page_no"] - 1)).limit(
						args["page_limit"])
					_response = get_response(200)
					_response["data"] = json.loads(json_util.dumps(data))
					_response["count"] = count
					return _response
				else:
					_response = get_response(404)
					_response["data"] = []
					_response["count"] = 0
					return _response

		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Checklist Data'
			logging.error(e)
			return _response

	@token_required
	@api.expect(post_checklist_master)
	def post(self, *args):
		try:
			args = request.get_json()
			database_connection = database_access()
			checklist_master_collection = database_connection["dms_checklist_master"]
			checklist_master_collection.insert_one(args)
			logging.info(get_response(200))
			return get_response(200)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Checklist Data'
			logging.error(e)
			return _response

	@token_required
	@api.expect(put_checklist_master)
	def put(self, *args):
		try:
			args = request.get_json()
			database_connection = database_access()
			checklist_master_collection = database_connection["dms_checklist_master"]
			data = checklist_master_collection.find_one({"_id": ObjectId(args["_id"])})
			if data:
				checklist_master_collection.update_one(
					{"_id": ObjectId(args["_id"])},
					{'$set': {"stages": args["stages"], "checklist_details": args["checklist_details"]}})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Update Checklist Data'
			logging.error(e)
			return _response

	@token_required
	@api.expect(delete_checklist_master)
	def delete(self, *args):
		try:
			_id = request.args.get("_id")
			database_connection = database_access()
			checklist_master_collection = database_connection["dms_checklist_master"]
			data = checklist_master_collection.find_one({"_id": ObjectId(_id)})
			if data:
				checklist_master_collection.delete_one({"_id": ObjectId(_id)})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Delete checklist data'
			logging.error(e)
			return _response


checklist_byid = reqparse.RequestParser()
checklist_byid.add_argument("_id", type=str, required=True, help="_id")


class GetCheckListById(Resource):
	@token_required
	@api.expect(checklist_byid)
	def get(self, *args):
		try:
			_id = request.args.get("_id")
			database_connection = database_access()
			checklist_master_collection = database_connection["dms_checklist_master"]
			data = checklist_master_collection.find_one({"_id": ObjectId(_id)})
			if data:
				data = checklist_master_collection.find_one({"_id": ObjectId(_id)})
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
			_response['message'] = 'Failed to Get Checklist Data'
			logging.error(e)
			return _response


checklist_master_by_stages = reqparse.RequestParser()
checklist_master_by_stages.add_argument("applicable_stage", type=str, required=True, help="Applicable Stage")
checklist_master_by_stages.add_argument("applicable_movement", type=str, required=True, help="_id")


class GetCheckListByStages(Resource):
	@token_required
	@api.expect(checklist_master_by_stages)
	def get(self, *args):
		try:
			applicable_stage = request.args.get("applicable_stage")
			applicable_movement = request.args.get("applicable_movement")
			database_connection = database_access()
			checklist_master_collection = database_connection["dms_checklist_master"]
			data = checklist_master_collection.find(
				{"stages": {"$elemMatch": {"applicable_stage": applicable_stage, "applicable_movement": {"$elemMatch": {"value":
					applicable_movement}}}}, "checklist_details.status": "enabled"})
			count = checklist_master_collection.count_documents(
				{"stages": {
					"$elemMatch": {"applicable_stage": applicable_stage, "applicable_movement": {"$elemMatch": {"value":
				applicable_movement}}}}, "checklist_details.status": "enabled"})
			total_count = checklist_master_collection.count_documents({})
			if len(list(data)):
				data = checklist_master_collection.find(
					{"stages": {"$elemMatch": {"applicable_stage": applicable_stage, "applicable_movement": {"$elemMatch": {"value":
						applicable_movement}}}}, "checklist_details.status": "enabled"})
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				_response["count"] = json.loads(json_util.dumps(count))
				_response["total_count"] = json.loads(json_util.dumps(total_count))
				return _response
			else:
				_response = get_response(404)
				_response["data"] = []
				_response["count"] = 0
				return _response
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Checklist Data'
			logging.error(e)
			return _response
