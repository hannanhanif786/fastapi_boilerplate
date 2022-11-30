from typing import List
from fastapi import APIRouter, UploadFile, File, Depends
from .schemas import FileUpload
from decouple import config
from service.s3 import upload_to_aws
import os
from .db import get_db
import shutil
from temp_files.file import TEMP_FILE_FOLDER
from .models import FileUpload
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("")
async def upload_image( files: UploadFile = File(...), db: Session = Depends(get_db)):
    """upload image endpoint

    Args:
        files (List[UploadFile], optional): lsit of images

    Returns:
        _type_: dict response
    """
    ext=files.filename.split(".")
    bucket= config("AWS_BUCKET")
    path = os.path.join(TEMP_FILE_FOLDER, files.filename)
    with open(f"temp_files/{files.filename}","wb") as f:
        shutil.copyfileobj(files.file, f)
        ext=ext[1]  #file Extension
        data = upload_to_aws(path, bucket, files.filename, ext)
        # added url to database
        add_path = FileUpload(file_path=data)
        db.add(add_path)
        db.commit()
        db.refresh
        os.remove(path)
    return {"msg": data}
