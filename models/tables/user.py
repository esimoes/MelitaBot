from datetime import datetime

from sqlalchemy import Column, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BOOLEAN
from sqlalchemy.orm import relationship

from ..base import Base
from config import Config

class User(Base):
    __tablename__ = Config.USER_DB

    id = Column(INTEGER, primary_key=True)
    username = Column(VARCHAR(64), nullable=True)
    first_name = Column(VARCHAR(64), nullable=False)
    last_name = Column(VARCHAR(64), nullable=True)
    joined = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    language_code = Column(VARCHAR(2), nullable=False)
    active = Column(BOOLEAN, nullable=False, default=True)