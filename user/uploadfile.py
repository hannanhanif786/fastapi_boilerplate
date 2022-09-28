import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post("")
async def upload_image(files: List[UploadFile] = File(...)):
    """upload image endpoint

    Args:
        files (List[UploadFile], optional): lsit of images

    Returns:
        _type_: dict response
    """
    for img in files:
        with open(f"{img.filename}", "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {"msg": "File uploaded"}
