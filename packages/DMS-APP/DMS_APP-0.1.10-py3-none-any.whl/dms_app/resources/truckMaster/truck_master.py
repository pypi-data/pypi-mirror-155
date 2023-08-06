from flask import request
from flask_restx import Resource, fields, reqparse
from ...db.db_connection import database_access
from ...namespace import api
import logging
from ...response_helper import get_response
import json
from bson import json_util
import re
from ..login_register.login import token_required


post_truck_master = api.model("VehicleDetails", {
	"vehicle_no": fields.String,
	"plant_code": fields.String,
	"transporter_name": fields.String,
	"transporter_code": fields.String,
	"capacity": fields.String,
	"empty_weight": fields.String,
	"vehicle_type": fields.String,
	"engine_number": fields.String,
	"chasis_number": fields.String,
	"puc_number": fields.String,
	"puc_issue_date": fields.String,
	"puc_expiry_date": fields.String,
	"fitness_issue": fields.String,
	"fitness_expiry": fields.String,
	"insurance_number": fields.String,
	"insurance_issue_date": fields.String,
	"insurance_expiry_date": fields.String,
	"vehicle_owner_name": fields.String,
})

get_all_truck_master = reqparse.RequestParser()
get_all_truck_master.add_argument("page_no", type=int, required=True, help="Page number")
get_all_truck_master.add_argument("page_limit", type=int, required=True, help="limit ")


class TruckMaster(Resource):
	@token_required
	@api.expect(get_all_truck_master)
	def get(self, *args):
		try:
			database_connection = database_access()
			truck_details_col = database_connection["truck_master"]
			data = truck_details_col.find()
			count = truck_details_col.count_documents({})
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			if len(list(data)):
				data = truck_details_col.find().skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
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
			_response['message'] = 'Failed to Get Truck Detail'
			logging.error(e)
			return _response

	@token_required
	@api.expect(post_truck_master)
	def post(self, *args):
		args = request.get_json()
		try:
			database_connection = database_access()
			truck_details_col = database_connection["truck_master"]
			if not truck_details_col.find_one({"vehicle_no": args["vehicle_no"]}):
				truck_details_col.insert_one(args)
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(409))
				return get_response(409)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Truck Details'
			logging.error(e)
			return _response

	@token_required
	@api.expect(post_truck_master)
	def put(self, *args):
		args = request.get_json()
		try:
			database_connection = database_access()
			truck_details_col = database_connection["truck_master"]
			if truck_details_col.find_one({"vehicle_no": args["vehicle_no"]}):
				truck_details_col.update_one({"vehicle_no": args["vehicle_no"]}, {
					'$set': args})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.error(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Update Truck Details'
			logging.error(e)
			return _response


truck_master_by_id = reqparse.RequestParser()
truck_master_by_id.add_argument("vehicle_no", type=str, required=True, help="Vehicle No")


class TruckMasterById(Resource):
	@token_required
	@api.expect(truck_master_by_id)
	def get(self, *args):
		try:
			database_connection = database_access()
			truck_details_col = database_connection["truck_master"]
			vehicle_no = request.args.get("vehicle_no")
			data = truck_details_col.find_one({"vehicle_no": vehicle_no})
			if data:
				data = truck_details_col.find_one({"vehicle_no": vehicle_no})
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Truck Detail'
			logging.error(e)
			return _response


post_integration_trigger = api.model("integration_trigger", {
	"trip_id": fields.String,
	"vehicle_number": fields.String,
	"movement_type": fields.String,
})

get_integration_trigger = reqparse.RequestParser()
get_integration_trigger.add_argument("page_no", type=int, required=True, help="Page number")
get_integration_trigger.add_argument("page_limit", type=int, required=True, help="limit ")
get_integration_trigger.add_argument("movement_type", type=str, help="Movement Type")
get_integration_trigger.add_argument("trip_id", type=str, help="Trip Id")


class IntegrationTrigger(Resource):
	@token_required
	@api.expect(get_integration_trigger)
	def get(self, *args):
		try:
			database_connection = database_access()
			integration_trigger_col = database_connection["integration_trigger"]
			args = get_integration_trigger.parse_args()
			if args["trip_id"] and args["movement_type"]:
				movement_type = request.args.get("movement_type")
				regx = re.compile(movement_type, re.IGNORECASE)
				regx_trip_id = re.compile(args["trip_id"], re.IGNORECASE)
				data = integration_trigger_col.find(
					{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}], "movement_type": {
						'$regex': regx}})
				count = integration_trigger_col.count_documents(
					{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}], "movement_type": {
						'$regex': regx}})
				total_count = integration_trigger_col.count_documents({})
				if len(list(data)):
					data = integration_trigger_col.find(
						{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}], "movement_type": {
							'$regex': regx}}).skip(
						int(args["page_limit"]) * (int(args["page_no"]) - 1)). \
						limit(int(args["page_limit"]))
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

			elif args["movement_type"]:
				movement_type = request.args.get("movement_type")
				regx = re.compile(movement_type, re.IGNORECASE)
				data = integration_trigger_col.find({"movement_type": {'$regex': regx}})
				count = integration_trigger_col.count_documents({"movement_type": {'$regex': regx}})
				total_count = integration_trigger_col.count_documents({})
				if len(list(data)):
					data = integration_trigger_col.find({"movement_type": {'$regex': regx}}).skip(
						int(args["page_limit"]) * (int(args["page_no"]) - 1)). \
						limit(int(args["page_limit"]))
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

			elif args["trip_id"]:
				regx_trip_id = re.compile(args["trip_id"], re.IGNORECASE)
				data = integration_trigger_col.find(
					{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}]})
				count = integration_trigger_col.count_documents(
					{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}]})
				total_count = integration_trigger_col.count_documents({})
				if len(list(data)):
					data = integration_trigger_col.find(
						{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}]})
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
				data = integration_trigger_col.find()
				count = integration_trigger_col.count_documents({})
				if len(list(data)):
					data = integration_trigger_col.find().skip(int(args["page_limit"]) * (int(args["page_no"]) - 1)). \
						limit(int(args["page_limit"]))
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
			_response['message'] = 'Failed to Get Integration Trigger Detail'
			logging.error(e)
			return _response

	@token_required
	@api.expect(post_integration_trigger)
	def post(self, *args):
		args = request.get_json()
		try:
			database_connection = database_access()
			integration_trigger_col = database_connection["integration_trigger"]
			if not integration_trigger_col.find_one({"vehicle_number": args["vehicle_number"]}):
				integration_trigger_col.insert_one(args)
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(409))
				return get_response(409)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Integration Trigger Details'
			logging.error(e)
			return _response


integration_trigger_by_id = reqparse.RequestParser()
integration_trigger_by_id.add_argument("trip_id", type=str, required=True, help="Trip Id")


class IntegrationTriggerByTripID(Resource):
	@token_required
	@api.expect(integration_trigger_by_id)
	def get(self, *args):
		try:
			database_connection = database_access()
			integration_trigger_col = database_connection["integration_trigger"]
			trip_id = request.args.get("trip_id")
			data = integration_trigger_col.find_one({"trip_id": trip_id})
			if data:
				data = integration_trigger_col.find_one({"trip_id": trip_id})
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Integration Trigger Detail'
			logging.error(e)
			return _response


post_stage_master = api.model("StageMaster", {
	"stages": fields.Raw(
		[],
		required=True,
		example=[

		]
	)
})

get_stage_master = reqparse.RequestParser()
get_stage_master.add_argument("page_no", type=int, required=True, help="Page number")
get_stage_master.add_argument("page_limit", type=int, required=True, help="limit ")


class StageMaster(Resource):
	@token_required
	@api.expect(get_stage_master)
	def get(self, *args):
		try:
			database_connection = database_access()
			stage_master_col = database_connection["stage_master"]
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			data = stage_master_col.find()
			count = stage_master_col.count_documents({})
			if len(list(data)):
				data = stage_master_col.find().skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
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
			_response['message'] = 'Failed to Get Stage Master Detail'
			logging.error(e)
			return _response

	@token_required
	@api.expect(post_stage_master)
	def post(self, *args):
		args = request.get_json()
		try:
			database_connection = database_access()
			stage_master_col = database_connection["stage_master"]
			stage_master_col.insert_one(args)
			logging.info(get_response(200))
			return get_response(200)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Stages Details'
			logging.error(e)
			return _response
