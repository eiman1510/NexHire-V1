"""
this route page maily deals with the admin panel

admin logs in using pre-defined password from .env and then access the admin dashboard
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from db_functions.allowed_hr import create_admin, delete_admin, get_admins, get_registered
from core.config import ADMIN_PASS
from utils.response import api_response
from logging_config import logger
from utils.serialization import serialize_mongo_documents

#just to ease the input
class AdminLoginRequest(BaseModel):
    password: str


class AddHRRequest(BaseModel):
    email: str


router = APIRouter(prefix="/admin")

#handles admin login by comparing the entered password with the env password
@router.post("/admin_login")
def get_admin_login(request: AdminLoginRequest):
    try:
        if request.password == ADMIN_PASS:
            logger.info("Admin logged in successfully")
            return api_response(api_source="Admin Handler", status_code=200, message="Admin Logged in successfully")
        else:
            return api_response(api_source="Admin Handler", status_code=401, message="Invalid password")
    except Exception as e:
        logger.exception(f"Error in admin login: {str(e)}")
        return api_response(api_source="Admin Handler", status_code=500, message=f"Internal Error: {str(e)}")

#------------------------------------------------------------------
#here the admin can add in hr 
#he enters email of emloyee for authorize him/her as hr 
@router.post("/add_hr")
def add_hr(request: AddHRRequest):
    try:
        res = create_admin(request.email)
        if res:
            logger.info(f"User with email {request.email} is registered as HR")
            return api_response(api_source="Admin Handler", status_code=200, message="HR created successfully")
    except:
        logger.exception(f"Unexpected error while creating hr for user: {request.email}")
        return api_response(
            api_source="Admin Handler",
            status_code=500,
            data=None,
            message="Internal Server Error",
            error_code=1,
        )

#------------------------------------------------------------------
#admin can remove any user from hr position
@router.delete("/delete_hr")
def remove_hr(email: str = Query(...)):
    try:
        res = delete_admin(email)
        if res:
            logger.info(f"User with email {email} is removed as HR")
            return api_response(api_source="Admin Handler", status_code=200, message="HR removed successfully")
    except:
        logger.exception(f"Unexpected error while removing hr for user: {email}")
        return api_response(
            api_source="Admin Handler",
            status_code=500,
            data=None,
            message="Internal Server Error",
            error_code=1,
        )

#------------------------------------------------------------------
#this functions displays all the hr's
@router.get("/app_hr")
def get_all_hr():
    try:
        res = get_admins()
        res=serialize_mongo_documents(res)
        if res:
            logger.info("Hr retrieved successfully")
            return api_response(
                status_code=200, data=res, message="Hr retrieved successfully",api_source="admin handler"
            )
    except:
        logger.exception("Unable to fetch HRs")
        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="Admin Handler",
            error_code=1,
        )

#------------------------------------------------------------------

#this is used to displays the hr who has activated their hr account
@router.get("/get_registered_hrs")
def get_registered_hrs():
    try:
        res = get_registered()
        res=serialize_mongo_documents(res)
        if res:
            logger.info("Hr retrieved successfully")
            return api_response(
                status_code=200, data=res, message="Hr retrieved successfully",api_source="admin handler"
            )
    except:
        logger.exception("Unable to fetch HRs")
        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="Admin Handler",
            error_code=1,
        )