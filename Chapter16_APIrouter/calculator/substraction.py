from fastapi import APIRouter
router=APIRouter(prefix="/sub",tags=["subractact"])

@router.post("/")
def home(a:int,b:int):
    return a-b