from flask import request
from flask_restx import Resource, reqparse, fields
from ...db.db_connection import database_access
from ...namespace import api
import logging
from ...response_helper import get_response
import json
from bson import json_util
import os
import re
from ..login_register.login import token_required

get_employee = reqparse.RequestParser()
get_employee.add_argument("person_id", type=str, required=True, help="Person_ID")

get_all_employee = reqparse.RequestParser()
get_all_employee.add_argument("page_no", type=int, required=True, help="Page number")
get_all_employee.add_argument("page_limit", type=int, required=True, help="limit ")

delete_employee = reqparse.RequestParser()
delete_employee.add_argument("person_id", type=str, required=True, help="Person Id")

add_employee = api.model("EmployeeAdd", {
    "person": fields.Raw(
        [],
        required=True,
        example=[
            {
                "person_id": "string",
                "name": "string",
                "role": "string",
                "blacklist": "string",
                "added_by": "string",
                "added_date": "added_date",
                "image": "string",
                "fingerprint": "string",
                "status": "string",
            },
        ]
    )
})


class AddEmployee(Resource):
    @token_required
    @api.expect(get_employee)
    def get(self, *args):
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            args = get_employee.parse_args()
            data = person_profile_col.find_one(
                {'person.person_id': {'$regex': '^{person}$'.format(person=args["person_id"]), '$options': 'i'}})
            _response = get_response(200)
            if data:
                _response["data"] = json.loads(json_util.dumps(data))
                return _response
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Get Employee Detail'
            logging.error(e)
            return _response

    @token_required
    @api.expect(add_employee)
    def post(self, *args):
        args = request.get_json()
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            user = person_profile_col.find_one({"person.person_id": args["person"][0]["person_id"]})
            if not user:
                person_profile_col.insert_one({
                    "person": args["person"]})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.info(get_response(409))
                return get_response(409)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Store Employee'
            logging.error(e)
            return _response

    @token_required
    @api.expect(add_employee)
    def put(self, *args):
        args = request.get_json()
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            if person_profile_col.find_one({"person.person_id": args["person"][0]["person_id"]}):
                person_profile_col.delete_one({"person.person_id": args["person"][0]["person_id"]})
                person_profile_col.insert_one({"person": args["person"]})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.info(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update Employee Detail'
            logging.error(e)
            return _response

    @token_required
    @api.expect(delete_employee)
    def delete(self, *args):
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            add_person_col = database_connection["person_violations"]
            args = delete_employee.parse_args()
            coll = person_profile_col.find_one({"person.person_id": args["person_id"]})
            if coll:
                person_profile_col.delete_one({"person.person_id": args["person_id"]})
                if add_person_col.find_one({"person_id": args["person_id"]}):
                    add_person_col.delete_one({"person_id": args["person_id"]})
                count = 0
                path1 = os.getenv('fingerprint_Path')
                for file in [file for file in os.listdir(path1)]:
                    if file[0:-7] == args['person_id']:
                        os.remove(os.path.join(path1, file))
                        count = count + 1
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Delete Employee Detail'
            logging.error(e)
            return _response


employee = reqparse.RequestParser()
employee.add_argument("person_name", type=str, help="Person Name")
employee.add_argument("status", type=str, help="Status")
employee.add_argument("page_no", type=int, required=True, help="Page number")
employee.add_argument("page_limit", type=int, required=True, help="limit")


class GetEmployee(Resource):
    @token_required
    @api.expect(employee)
    def get(self, *args):
        try:
            database_connection = database_access()
            person_profile_col = database_connection["person_profile"]
            args = employee.parse_args()
            print(args)
            if args["person_name"] and args["status"]:
                regx = re.compile(args["person_name"], re.IGNORECASE)
                data = person_profile_col.find({"person.name": {'$regex': regx}, "person.status": args["status"]})
                count = person_profile_col.count_documents(
                    {"person.name": {'$regex': regx}, "person.status": args["status"]})
                if len(list(data)):
                    logging.info(get_response(200))
                    _response = get_response(200)
                    data = person_profile_col.find({"person.name": {'$regex': regx}, "person.status": args["status"]}). \
                        skip(args["page_limit"] * (args["page_no"] - 1)).limit(
                        args["page_limit"])
                    _response["data"] = json.loads(json_util.dumps(data))
                    _response["count"] = json.loads(json_util.dumps(count))
                    return _response
                else:
                    _response = get_response(404)
                    _response["data"] = []
                    _response["count"] = 0
                    return _response

            elif args["status"]:
                data = person_profile_col.find({"person.status": args["status"]})
                count = person_profile_col.count_documents({"person.status": args["status"]})
                if len(list(data)):
                    data = person_profile_col.find({"person.status": args["status"]}).skip(
                        args["page_limit"] * (args["page_no"] - 1)).limit(
                        args["page_limit"])
                    _response = get_response(200)
                    _response["data"] = json.loads(json_util.dumps(data))
                    _response["count"] = json.loads(json_util.dumps(count))
                    return _response
                else:
                    _response = get_response(404)
                    _response["data"] = []
                    _response["count"] = 0
                    return _response

            elif args["person_name"]:
                regx = re.compile(args["person_name"], re.IGNORECASE)
                data = person_profile_col.find({"person.name": {'$regex': regx}})
                count = person_profile_col.count_documents({"person.name": {'$regex': regx}})
                if len(list(data)):
                    _response = get_response(200)
                    data = person_profile_col.find(
                        {"person.name": {'$regex': regx}}).skip(args["page_limit"] * (args["page_no"] - 1)).limit(
                        args["page_limit"])
                    _response["data"] = json.loads(json_util.dumps(data))
                    _response["count"] = json.loads(json_util.dumps(count))
                    return _response
                else:
                    _response = get_response(404)
                    _response["data"] = []
                    _response["count"] = 0
                    return _response
            else:
                count = person_profile_col.count_documents({})
                data = person_profile_col.find({})
                if len(list(data)):
                    data = person_profile_col.find({}).skip(args["page_limit"] * (args["page_no"] - 1)).limit(
                        args["page_limit"])
                    _response = get_response(200)
                    _response['count'] = json.loads(json_util.dumps(count))
                    _response["data"] = json.loads(json_util.dumps(data))
                    return _response
                else:
                    _response = get_response(404)
                    _response["data"] = []
                    _response["count"] = 0
                    return _response

        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Get Employee Detail'
            logging.error(e)
            return _response
