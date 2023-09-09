from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
def hello():
    return {"status": "OK"}


@router.get("/world")
def world():
    return {"status": "OK"}
