from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .db import get_db
from .schemas import changepassword
from .auth import get_current_user
from .auth import authenticate_user
from .auth import get_password_hash


router = APIRouter()


@router.post("")
async def change_password(
    reset: changepassword,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """make end point for reset old password

    Args:
        reset (ResetPasssword): schema for paswords
        db (Session, optional): db connection
        user (_type_, optional): current user

    Raises:
        HTTPException: 401, Incorrect Password
        HTTPException: 401, new and confirm passwords not match

    Returns:
        _type_: Response for successfully reset password
    """

    user = authenticate_user(user.email, reset.old_password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password"
        )
    if reset.new_password == reset.confirm_password:
        hashed_password = get_password_hash(reset.new_password)
        user.password = hashed_password
        db.commit()
    else:
        raise HTTPException(
            status_code=401, detail="new_pasword and confirm_password not match"
        )
    return {"msg": "password change successfully"}
