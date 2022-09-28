from fastapi import APIRouter, Depends, HTTPException
from .schemas import UserBase, UpdateUser, UserSchema
from .db import get_db
from .models import User
from sqlalchemy.orm import Session
from .auth import get_password_hash
from .query import user_create, user_update, user_get_by_id, user_delete
from .auth import get_current_active_user
import logging

logger = logging.getLogger("user.crud")

router = APIRouter()


@router.get("/{id}", response_model=UserSchema)
def user_id(
    id: int,
    db: Session = Depends(get_db),
):
    """ "
        get user by id
    Args:
        id (int): user_id
        db (Session, optional): database connection

    Raises:
        HTTPException: 404, user not found

    Returns:
        _type_: instant user by id
    """
    response = user_get_by_id(id, db)
    logger.info(f"user id {id}")
    return response


@router.post("/")
def add_user(
    user: UserBase,
    db: Session = Depends(get_db),
    active_user=Depends(get_current_active_user),
):
    """create user for crud

    Args:
        user (UserBase): schema for user create
        db (Session, optional): database connection

    Raises:
        HTTPException: 400, exception for email already exist

    Returns:
        _type_: dic for user creation
    """
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    db_user = user_create(user, db)
    logger.info(f"{db_user.name} created successfully")
    return {"msg": f"{db_user.name} created successfully"}


@router.put("/{id}")
def update_user(id: int, user: UpdateUser, db: Session = Depends(get_db)):
    """update user

    Args:
        id (int): id from request
        user (UpdateUser): schema for updation
        db (Session, optional): database connection

    Raises:
        HTTPException: 400, user not found

    Returns:
        _type_: dic for msg to update user
    """
    update_user = user_update(id, user, db)
    logger.info(f"{update_user.name} updated successfully")
    return {"msg": "updated user"}


@router.delete("/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db),
):
    """delete user

    Args:
        id (int): id from request
        db (Session, optional): database connection

    Raises:
        HTTPException:  400, user not found

    Returns:
        _type_: dic for msg to delete user
    """
    userObj = user_delete(id, db)
    logger.info(f"{userObj.name} deleted successfully")
    return {"msg": f"{userObj.name} deleted successfully"}
