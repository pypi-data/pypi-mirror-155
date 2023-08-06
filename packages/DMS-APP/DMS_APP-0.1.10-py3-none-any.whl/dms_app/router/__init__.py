from dms_app.resources.login_register import Login, AddUser, ChangeUserPassword, SuperLogin
from dms_app.resources.driver_functions import Driver, Status
from dms_app.resources.add_profile import AddEmployee, GetEmployee
from dms_app.resources.violation import ViolationOperations, ActiveViolations, UpdateViolation, ViolationsEmployee
from dms_app.resources.schema import AddSchema
from dms_app.resources.settings import PersonIdAutoIncrement
from dms_app.resources.fingerprint import AddFingerprint, MatchFingerprint
from dms_app.resources.roles_privileges import AddRolePrivileges, GetAllRolesPrivileges
from dms_app.resources.truckMaster import TruckMaster, ChecklistHistory, IntegrationTrigger, StageMaster, \
    CheckListApproval, GetCheckListById, CheckListMaster, GetCheckListByStages, IntegrationTriggerByTripID, \
    ChecklistHistoryById, TruckMasterById
from dms_app.resources.access_token import CreateToken


def register_routes(api):
    api.add_resource(Login, "/LoginRegister")
    api.add_resource(AddUser, "/RegisterUser")
    api.add_resource(ChangeUserPassword, "/ ")
    api.add_resource(Driver, "/Employee")
    api.add_resource(Status, "/EmployeeStatus")
    api.add_resource(AddEmployee, "/EmployeeProfile")
    api.add_resource(GetEmployee, "/GetAllEmployees")
    api.add_resource(ViolationOperations, "/Violation")
    api.add_resource(ActiveViolations, "/GetActiveViolations")
    api.add_resource(UpdateViolation, "/UpdateViolation")
    api.add_resource(AddSchema, "/Schema")
    api.add_resource(ViolationsEmployee, "/Employee_Violations")
    api.add_resource(PersonIdAutoIncrement, "/PersonIdAutoIncrement")
    api.add_resource(AddFingerprint, "/AddFingerprint")
    api.add_resource(MatchFingerprint, "/MatchFingerprint")
    api.add_resource(AddRolePrivileges, "/AddRolePrivileges")
    api.add_resource(GetAllRolesPrivileges, "/GetAllRolePrivileges")
    api.add_resource(ChangeUserPassword, "/ChangeUserPassword")
    api.add_resource(SuperLogin, "/AdminLogin")
    api.add_resource(TruckMaster, "/TruckDetail")
    api.add_resource(ChecklistHistory, "/ChecklistHistory")
    api.add_resource(IntegrationTrigger, "/IntegrationTrigger")
    api.add_resource(StageMaster, "/StageMaster")
    api.add_resource(CheckListApproval, "/CheckListApproval")
    api.add_resource(IntegrationTriggerByTripID, "/IntegrationTriggerByTripID")
    api.add_resource(CheckListMaster, "/CheckListMaster")
    api.add_resource(GetCheckListById, "/GetCheckListById")
    api.add_resource(GetCheckListByStages, "/GetCheckListByStages")
    api.add_resource(ChecklistHistoryById, "/ChecklistHistoryById")
    api.add_resource(TruckMasterById, "/TruckMasterById")
    api.add_resource(CreateToken, "/CreateToken")
