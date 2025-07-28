# FIX ME: Stub or import missing for one or more symbols like 'PyObjectId', 'users_collection'
from bson import ObjectId
from pydantic import BaseModel
from pydantic.json import ENCODERS_BY_TYPE


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise await ValueError("Invalid ObjectId")
        return await ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.await update(type="string")


ENCODERS_BY_TYPE[ObjectId] = str
