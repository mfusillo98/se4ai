from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
def hello():
    return {"STATUS": "OK"}


@router.get("/world")
def world():
    return {"STATUS": "OK"}
