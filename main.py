"""
Project name: limongodb
26/09/2021
"""

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List
import pymongo
import certifi

app = FastAPI()
MONGODB_URL = "mongodb+srv://limongodb1:60221041@limongodb.ftkfv.mongodb.net/limongodb?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
db = client.mador


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MadorMemberModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    age: int = Field(..., le=120)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Israel Israel",
                "age": "25",
            }
        }


class UpdateMadorMemberModel(BaseModel):
    name: Optional[str]
    age: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Israel Israel",
                "age": "25",
            }
        }


@app.post("/", response_description="Add new mador member", response_model=MadorMemberModel)
async def create_member(member: MadorMemberModel = Body(...)):
    member = jsonable_encoder(member)
    new_member = db["members"].insert_one(member)
    created_member = db["members"].find_one({"_id": new_member.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_member)


@app.get("/", response_description="List all members", response_model=List[MadorMemberModel])
async def list_members():
    students = list(db["members"].find())
    return students


@app.get("/{id}", response_description="Get a single mador member", response_model=MadorMemberModel)
async def show_member(id: str):
    if (member := db["members"].find_one({"_id": id})) is not None:
        return member

    raise HTTPException(status_code=404, detail=f"Mador member {id} not found")


@app.put("/{id}", response_description="Update a mador member", response_model=MadorMemberModel)
async def update_member(id: str, member: UpdateMadorMemberModel = Body(...)):
    member = {k: v for k, v in member.dict().items() if v is not None}

    if len(member) >= 1:
        update_result = db["members"].update_one({"_id": id}, {"$set": member})

        if update_result.modified_count == 1:
            if (
                updated_member := db["members"].find_one({"_id": id})
            ) is not None:
                return updated_member

    if (existing_member := db["members"].find_one({"_id": id})) is not None:
        return existing_member

    raise HTTPException(status_code=404, detail=f"Mador member {id} not found")


@app.delete("/{id}", response_description="Delete mador member")
async def delete_member(id: str):
    delete_result = db["members"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Mador member {id} not found")
