from frontend.db.download_status import get_download_status
from fastapi import APIRouter

from starlette.background import BackgroundTasks
from frontend.utils.products.download import download

router = APIRouter()


@router.get("/download/{s2_product_name}")
async def download_product(background_tasks: BackgroundTasks, s2_product_name: str):
    background_tasks.add_task(download, s2_product_name)
    return {
        "message": f"The Sentinel-2 product under name {s2_product_name} is being downloaded.",
    }

@router.get("/download/status/{s2_product_name}")
async def download_status(s2_product_name: str):
    is_downloaded = await get_download_status(s2_product_name)

    return {
        "downloaded": is_downloaded
    }