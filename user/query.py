from .models import User
from fastapi import HTTPException
import sqlalchemy
from .schemas import UserSchema


def user_get_by_id(id, db):
    user = db.query(User).get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    response: UserSchema = user
    return response


def user_create(user, db):
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="email already exist")
    return db_user


def user_update(id, user, db):
    userObj = db.query(User).get(id)
    if userObj is None:
        raise HTTPException(status_code=400, detail="user not found")
    userObj.name = user.name
    userObj.phone_no = user.phone_no
    db.commit()
    return userObj


def user_delete(id, db):
    userObj = db.query(User).get(id)
    if userObj is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(userObj)
    db.commit()
    db.close
    return userObj


def user_get_by_email(name, db):
    user = db.query(User).filter(User.email == name).first()
    return user
