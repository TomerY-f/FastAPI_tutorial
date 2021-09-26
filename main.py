"""
Project name: FastAPI Tuotorial
26/09/2021
"""

from fastapi import FastAPI
import uvicorn

limongodb = FastAPI()

limongodb.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(limongodb)




