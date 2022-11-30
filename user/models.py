from .db import Base
from sqlalchemy import Boolean, Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)
    phone_no = Column(String)

class FileUpload(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, unique=True, nullable=False, index=True)

