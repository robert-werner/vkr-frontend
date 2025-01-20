from fastapi import APIRouter

router = APIRouter()

@router.get("/tms/{alias}/{band}/{z}/{x}/{y}.tif@{res}")
async def tms(alias: str, band: str, z: int, x: int, y: int, res: int):
    ...
