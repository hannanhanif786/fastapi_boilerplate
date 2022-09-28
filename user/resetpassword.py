from fastapi import APIRouter, Depends, Request, HTTPException, status
from .schemas import ForgetPassword, ResetPassword
from .db import get_db
from sqlalchemy.orm import Session
from .query import user_get_by_email
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from decouple import config
from .auth import create_access_token, get_password_hash
from datetime import timedelta
from jose import jwt
from config import settings

ALGORITHM = "HS256"


router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME=config("EMAIL_HOST_USER"),
    MAIL_PASSWORD=config("EMAIL_HOST_PASSWORD"),
    MAIL_FROM=config("EMAIL_HOST_USER"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
)


@router.post("")
async def reset_password(
    user: ForgetPassword, request: Request, db: Session = Depends(get_db)
):
    """send email to the user for reset password

    Args:
        user (ForgetPassword): schema for emial
        request (Request): request for url
        db (Session, optional): db connection

    Returns:
        _type_: email confirmation msg
    """
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    client_host = request.url._url
    message = MessageSchema(
        subject="Reset Pasword",
        recipients=[user.email],
        body=f"{client_host}/done?token={access_token}",
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"msg": "Reset password email sent"}


@router.post("/done")
async def reset_password_confirm(
    token: str, reset: ResetPassword, db: Session = Depends(get_db)
):
    """reset password confirm endpoint

    Args:
        token (str): param query token
        reset (ResetPassword): schema for reset password
        db (Session, optional): db connection

    Raises:
        HTTPException: 400, if user not found in token
        HTTPException: 401, user not exist
        HTTPException: 401. if password not matched

    Returns:
        _type_: successful msg
    """
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=400, detail="token user is not found")
    user = user_get_by_email(username, db)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="user not exist")
    if reset.password == reset.confirm_password:
        hashed_password = get_password_hash(reset.password)
        user.password = hashed_password
        db.commit()
    else:
        raise HTTPException(
            status_code=401, detail="new_pasword and confirm_password not match"
        )
    return {"msg": "password reset successfully"}
