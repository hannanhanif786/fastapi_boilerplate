from fastapi import FastAPI
from user import changepassword, crud, login, uploadfile, resetpassword
from config import settings
from tests import test_crud
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn


# setup loggers
# logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# get root logger
# logger = logging.getLogger("main")

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(crud.router, prefix="/user", tags=["user"])
app.include_router(login.router, prefix="/login", tags=["login"])
app.include_router(
    changepassword.router, prefix="/change-password", tags=["changepassword"]
)
app.include_router(uploadfile.router, prefix="/uploadfile", tags=["uploadfile"])
app.include_router(
    resetpassword.router, prefix="/reset-password", tags=["resetpassword"]
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
