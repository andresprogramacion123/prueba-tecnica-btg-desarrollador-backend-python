from fastapi import APIRouter

router = APIRouter()

@router.get("/hola")
def hola_mundo():
    return {"Hola":"Mundo"}