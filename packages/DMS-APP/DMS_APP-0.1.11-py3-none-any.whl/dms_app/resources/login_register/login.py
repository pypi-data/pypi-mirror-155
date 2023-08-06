import hashlib
import logging
from flask import request, Flask
from ...db.db_connection import database_access
from flask_restx import Resource, fields, reqparse
from ...namespace import api
from ...response_helper import get_response
import json
from bson import json_util
import smtplib
import re
from bson.objectid import ObjectId
from random import *
import random
import math
import jwt
from datetime import datetime, timedelta
from functools import wraps
import boto3
import emails
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#
# SENDER = 'notification@autoplant.systems'
# SENDERNAME = 'PK'
# USERNAME_SMTP = 'AKIAZGDBWNF3SRLJAHOB'
# PASSWORD_SMTP = 'BGw2xVcL0CCqV1dOMI8QmrEKXLaL10c2cf/LffJFaxrH'
# HOST = 'email-smtp.ap-south-1.amazonaws.com'
# PORT = 465
#
# msg = MIMEMultipart('alternative')
# msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
# msg['To'] = 'pratukharatmol99@gmail.com'
# BODY_TEXT = "HELO HDHCDSV"
# BODY_HTML = """<html>
# <head>
# <body><h1>hello</h1></body></head></html>"""
# part1 = MIMEText(BODY_TEXT,'plain')
# part1 = MIMEText(BODY_HTML,'html')
# msg.attach(part1)
# try:
#     server = smtplib.SMTP(HOST, PORT)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()
#     server.login(USERNAME_SMTP,PASSWORD_SMTP)
#     server.sendmail(SENDER,"kharatmolbhagirathi@gmail.com")
#     server.close()
# except Exception as e:
#     print("error", e)
# def verify_email_identity():
#     ses_client = boto3.client("ses", region_name="ap-south-1")
#     response = ses_client.verify_email_identity(
#         EmailAddress="notification@autoplant.systems"
#     )
#     print(response)
# verify_email_identity()
# message = emails.html(
#     html = "<h1>This is an email</h1><strong>We love sending emails</strong>",
#     subject = "Hey, look in here!",
#     mail_from="notification@autoplant.systems",
# )
#
# # Now you can send the email!
# r = message.send(
#     to="kharatmolbhagirathi@gmail.com",
#     smtp={
#         "host": "smtp.ap-south-1.amazonaws.com",
#         "port": 587,
#         "timeout": 10,
#         "user": "AKIAZGDBWNF3SRLJAHOB",
#         "password": "BGw2xVcL0CCqV1dOMI8QmrEKXLaL10c2cf/LffJFaxrH",
#         "tls": True,
#     },
# )
# print(r.status_code == 250)
flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'cc6e455f0b76439d99cc8e1669232518'
# flask_app.config['MAIL_USE_TLS'] = True

post_user = api.model("AddUser", {
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "role": fields.String,
    "contact": fields.String,
})

put_user = api.model("PutUser", {
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "role": fields.String,
    "contact": fields.String,
})

get_all_User = reqparse.RequestParser()
get_all_User.add_argument("page_no", type=int, required=True, help="Page number")
get_all_User.add_argument("page_limit", type=int, required=True, help="limit ")

change_user_password = api.model("ChangePassword", {
    "email": fields.String,
    "password": fields.String
})

delete_user = api.model("DeleteUser", {
    "object_id": fields.String
})

user = reqparse.RequestParser()
user.add_argument("role", type=str, help="role")
user.add_argument("email", type=str, help="Email")
user.add_argument("page_no", type=int, required=True, help="Page number")
user.add_argument("page_limit", type=int, required=True, help="limit ")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        database_connection = database_access()
        token_coll = database_connection["bearer_token"]
        args = request.headers
        email = args["email"]
        access_token = args["access_token"]
        session_id = args["session_id"]
        token = email + "_" + session_id + "_" + access_token
        data = token_coll.find_one({"access_token": token})
        if data:
            token_coll.delete_one({"access_token": token})
            return f(*args, **kwargs)
        else:
            _response = get_response(404)
            _response["message"] = "You are unauthorised"
            return _response
    return decorated


class AddUser(Resource):
    @token_required
    @api.expect(user)
    def get(self, *args):
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            args = user.parse_args()
            if args["role"] and args["email"]:
                data = list(dms_user_col.find(
                    {"role": args["role"], "$or": [
                        {"email": {'$regex': '^{email}'.format(email=args["email"]), '$options': 'mi'}},
                        {"first_name": {'$regex': '^{first_name}'.format(first_name=args["email"]),
                         '$options': 'mi'}}]}, {"password": 0}).skip(args["page_limit"] * (args["page_no"] - 1)).limit(
                    args["page_limit"]))
                count = dms_user_col.count_documents(
                    {"role": args["role"],
                     "$or": [{"email": {'$regex': '^{email}'.format(email=args["email"]), '$options': 'mi'}},
                             {"first_name": {'$regex': '^{first_name}'.format(first_name=args["email"]),
                                             '$options': 'mi'}}]})
                total_count = dms_user_col.count_documents({})
                if len(data):
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
            elif args["role"]:
                data = list(dms_user_col.find({"role": args["role"]}, {"password": 0}).skip(
                    args["page_limit"] * (args["page_no"] - 1)).limit(
                    args["page_limit"]))
                count = dms_user_col.count_documents({"role": args["role"]})
                total_count = dms_user_col.count_documents({})
                if len(data):
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
            elif args["email"]:
                data = list(dms_user_col.find(
                    {"$or": [{"email": {'$regex': '^{email}'.format(email=args["email"]), '$options': 'mi'}},
                             {"first_name": {'$regex': '^{first_name}'.format(first_name=args["email"]),
                                             '$options': 'mi'}}]}).skip(args["page_limit"] * (args["page_no"] - 1)). \
                    limit(args["page_limit"]))
                count = dms_user_col.count_documents(
                    {"$or": [{"email": {'$regex': '^{email}'.format(email=args["email"]), '$options': 'mi'}},
                    {"first_name": {'$regex': '^{first_name}'.format(first_name=args["email"]), '$options': 'mi'}}]})
                total_count = dms_user_col.count_documents({})
                if len(data):
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
                data = list(dms_user_col.find({}, {"password": 0}).skip(args["page_limit"] * (args["page_no"] - 1)).limit(
                    args["page_limit"]))
                print(data)
                count = dms_user_col.count_documents({})
                if len(data):
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
            _response['message'] = 'User Not Found'
            logging.error(e)
            return _response

    @api.expect(post_user, validate=True)
    # @token_required
    def post(self, *args):
        try:
            args = request.get_json()
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            digits = [i for i in range(0, 10)]
            otp = ""
            for i in range(6):
                index = math.floor(random.random() * 10)
                otp += str(digits[index])
            recipient = args['email'].strip()
            body = "Hello " + args["first_name"] + " " + args["last_name"] + "," + \
                   "\r\nOne Time Password for Driver Management System Application : " + str(otp)
            server = smtplib.SMTP("email-smtp.ap-south-1.amazonaws.com", 587)
            server.starttls()
            hash_password = hashlib.md5(str(otp).encode("utf-8")).digest()
            regx = re.compile(args["email"], re.IGNORECASE)
            if not dms_user_col.find_one({"email": {'$regex': regx}}):
                server.login("AKIAZGDBWNF3SRLJAHOB", "BGw2xVcL0CCqV1dOMI8QmrEKXLaL10c2cf/LffJFaxrH")
                server.sendmail('notification@autoplant.systems', recipient, body)
                dms_user_col.insert_one(
                    {"first_name": args["first_name"], "last_name": args["last_name"], "email": args["email"],
                     "password": hash_password, "role": args["role"], "contact": args["contact"]})
                return get_response(200)
            else:
                return get_response(409)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Store User'
            logging.error(e)
            return _response

    @token_required
    @api.expect(put_user, validate=True)
    def put(self, *args):
        args = request.get_json()
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            regx_email = re.compile(args["email"], re.IGNORECASE)
            if dms_user_col.find_one({"email": {'$regex': regx_email}}):
                dms_user_col.update_one({"email": args["email"]}, {
                    '$set':
                        {"first_name": args["first_name"], "last_name": args["last_name"], "email": args["email"],
                            "role": args["role"], "contact": args["contact"]}})
                return get_response(200)
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update User'
            logging.error(e)
            return _response

    @token_required
    @api.expect(delete_user, validate=True)
    def delete(self, *args):
        args = request.get_json()
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            if dms_user_col.find_one({"_id": ObjectId(args["object_id"])}):
                dms_user_col.delete_one({"_id": ObjectId(args["object_id"])})
                return get_response(200)
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Delete User'
            logging.error(e)
            return _response


user_login = api.model("UserLogin", {
    "email": fields.String,
    "password": fields.String,
})


class Login(Resource):
    @api.expect(user_login, validate=True)
    def post(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            regx_email = re.compile(args["email"], re.IGNORECASE)
            data = dms_user_col.find_one({"email": {'$regex': regx_email}})
            hash_password = hashlib.md5(args["password"].encode('utf-8')).digest()
            if data:
                _response = get_response(200)
                _response["role"] = json.loads(json_util.dumps(data["role"]))
                _response["first_name"] = json.loads(json_util.dumps(data["first_name"]))
                _response["last_name"] = json.loads(json_util.dumps(data["last_name"]))
                _response["email"] = json.loads(json_util.dumps(data["email"]))
                if data["password"] == hash_password:
                    session_id = jwt.encode({
                        'email': data['email'],
                        'exp': datetime.utcnow() + timedelta(days=1)
                    }, flask_app.config['SECRET_KEY'])
                    _response["session_id"] = session_id
                    if len(args["password"]) == 6 and args["password"].isdigit():
                        _response["otp"] = True
                        return _response
                    else:
                        _response["otp"] = False
                        return _response
                else:
                    logging.error(get_response(401))
                    return get_response(401)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Store User'
            logging.error(e)
            return _response


class ChangeUserPassword(Resource):
    @token_required
    @api.expect(change_user_password, validate=True)
    def put(self, *args):
        args = request.get_json()
        try:
            database_connection = database_access()
            dms_user_col = database_connection["dms_user"]
            hash_password = hashlib.md5(args["password"].encode("utf-8")).digest()
            regx_email = re.compile(args["email"], re.IGNORECASE)
            if dms_user_col.find_one({"email": {'$regex': regx_email}}):
                dms_user_col.update_one({"email": args["email"]}, {'$set': {"password": hash_password}})
                return get_response(200)
            else:
                logging.error(get_response(409))
                return get_response(409)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update User'
            logging.error(e)
            return _response
