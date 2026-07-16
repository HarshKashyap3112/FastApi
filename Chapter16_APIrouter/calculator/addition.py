from fastapi import APIRouter
# router=APIRouter(prefix="/add",tags=["add"])
router=APIRouter(prefix="/add")

@router.post("/")
def home(a:int,b:int):
    return a+b
