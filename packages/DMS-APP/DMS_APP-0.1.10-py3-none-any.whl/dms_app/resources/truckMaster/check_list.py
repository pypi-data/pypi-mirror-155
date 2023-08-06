from flask import request
from flask_restx import Resource, fields, reqparse
from ...db.db_connection import database_access
from ...namespace import api
from ...response_helper import get_response
import logging
import json
from bson import json_util
from bson.objectid import ObjectId
import re
from ..login_register.login import token_required


check_list_add = api.model("CheckListAdd", {
	"trip_id": fields.String,
	"vehicle_number": fields.String,
	"movement_type": fields.String,
	"stage": fields.String,
	"check_status": fields.String,
	"check_time": fields.String,
	"checklist": fields.Raw(
		[],
		required=True,
		example=[
			{
				"field1": "value1",
				"field2": "value2",
			},
		]
	)
})

update_checklist_status = api.model("Update_checklist_Status", {
	"_id": fields.String,
	"status": fields.String,
})

get_checklist = reqparse.RequestParser()
get_checklist.add_argument("trip_id", type=int, help="Trip ID")
get_checklist.add_argument("page_no", type=int, required=True, help="Page number")
get_checklist.add_argument("page_limit", type=int, required=True, help="limit ")


class CheckListApproval(Resource):
	@token_required
	@api.expect(get_checklist)
	def get(self, *args):
		try:
			database_connection = database_access()
			checklist_collection = database_connection["dms_check_list"]
			trip_id = request.args.get("trip_id")
			if trip_id:
				data = checklist_collection.find({"trip_id": {'$regex': '^{trip_id}'.format(trip_id=trip_id), '$options': 'mi'}})
				count = checklist_collection.count_documents(
					{"trip_id": {'$regex': '^{trip_id}'.format(trip_id=trip_id), '$options': 'mi'}})
				page_no = request.args.get("page_no")
				page_limit = request.args.get("page_limit")
				if len(list(data)):
					data = checklist_collection.find({"trip_id": {'$regex': '^{trip_id}'.format(trip_id=trip_id), '$options': 'mi'}}).skip(
						int(page_limit) * (int(page_no) - 1)).limit(int(page_limit))
					_response = get_response(200)
					_response["data"] = json.loads(json_util.dumps(data))
					_response["count"] = json.loads(json_util.dumps(count))
					return _response
				else:
					_response = get_response(404)
					_response["data"] = []
					_response["count"] = 0
					return _response
			else:
				data = checklist_collection.find()
				count = checklist_collection.count_documents({})
				page_no = request.args.get("page_no")
				page_limit = request.args.get("page_limit")
				if len(list(data)):
					data = checklist_collection.find().skip(int(page_limit) * (int(page_no) - 1)).limit(int(page_limit))
					_response = get_response(200)
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
			_response['message'] = 'Failed to Find Checklist History'
			logging.error(e)
			return _response

	@token_required
	@api.expect(check_list_add)
	def post(self, *args):
		args = request.get_json()
		try:
			database_connection = database_access()
			checklist_coll = database_connection["dms_check_list"]
			checklist_history_coll = database_connection["checklist_history"]
			data1 = checklist_coll.find_one({"trip_id": args["trip_id"]})
			if not data1:
				if args["check_status"] == "passed":
					checklist_history_coll.insert_one(args)
					logging.info(get_response(200))
					return get_response(200)
				elif args["check_status"] == "failed":
					checklist_coll.insert_one(args)
					logging.info(get_response(200))
					return get_response(200)
			else:
				return get_response(409)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store checklist'
			logging.error(e)
			return _response

	@token_required
	@api.expect(update_checklist_status, validate=True)
	def put(self, *args):
		try:
			database_connection = database_access()
			checklist_collection = database_connection["dms_check_list"]
			checklist_history_coll = database_connection["checklist_history"]
			args = request.get_json()
			data = checklist_collection.find_one({"_id": ObjectId(args["_id"])}, {"_id": 0})
			if data:
				if args["status"] == "approved":
					checklist_collection.update_one({"_id": ObjectId(args["_id"])}, {"$set": {"check_status": "approved"}})
					approved_collection = checklist_collection.find_one({"_id": ObjectId(args["_id"])})
					checklist_collection.delete_one({"_id": ObjectId(args["_id"])})
					checklist_history_coll.insert_one(approved_collection)
					logging.info(get_response(200))
					return get_response(200)
				elif args["status"] == "rejected":
					checklist_collection.update_one({"_id": ObjectId(args["_id"])}, {"$set": {"check_status": "rejected"}})
					approved_collection = checklist_collection.find_one({"_id": ObjectId(args["_id"])})
					checklist_collection.delete_one({"_id": ObjectId(args["_id"])})
					checklist_history_coll.insert_one(approved_collection)
					logging.info(get_response(200))
					return get_response(200)
			else:
				logging.error(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Delete Checklist'
			logging.error(e)
			return _response


get_checklist_history = reqparse.RequestParser()
get_checklist_history.add_argument("trip_id", type=int, help="Trip ID")
get_checklist_history.add_argument("page_no", type=int, required=True, help="Page number")
get_checklist_history.add_argument("page_limit", type=int, required=True, help="limit ")


class ChecklistHistory(Resource):
	@token_required
	@api.expect(get_checklist_history)
	def get(self, *args):
		try:
			database_connection = database_access()
			checklist_collection = database_connection["checklist_history"]
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			trip_id = request.args.get("trip_id")
			if trip_id:
				regx_trip_id = re.compile(trip_id, re.IGNORECASE)
				data = checklist_collection.find(
					{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}]})
				count = checklist_collection.count_documents(
					{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}]})
				total_count = checklist_collection.count_documents({})
				if len(list(data)):
					data = checklist_collection.find(
						{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}]}).skip(
						int(page_limit) * (int(page_no) - 1)). \
						limit(int(page_limit))
					data = list(data)
					logging.info(get_response(200))
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
				data = checklist_collection.find({"check_status": {"$ne": "failed"}})
				count = checklist_collection.count_documents({"check_status": {"$ne": "failed"}})
				total_count = checklist_collection.count_documents({})
				if len(list(data)):
					data = checklist_collection.find({"check_status": {"$ne": "failed"}}).skip(
						int(page_limit) * (int(page_no) - 1)). \
						limit(int(page_limit))
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
			_response['message'] = 'Failed to Get Checklist History'
			logging.error(e)
			return _response


search_checklist_history = reqparse.RequestParser()
search_checklist_history.add_argument("_id", type=str, required=True, help="Object Id")


class ChecklistHistoryById(Resource):
	@token_required
	@api.expect(search_checklist_history)
	def get(self, *args):
		try:
			database_connection = database_access()
			outbound_integration_col = database_connection["checklist_history"]
			_id = request.args.get("_id")
			data = outbound_integration_col.find_one({"_id": ObjectId(_id)})
			if data:
				data = outbound_integration_col.find_one({"_id": ObjectId(_id)})
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Checklist History'
			logging.error(e)
			return _response
