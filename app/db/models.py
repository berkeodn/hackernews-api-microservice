from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, Text, DateTime
from datetime import datetime, timezone

Base = declarative_base()

class Story(Base):
    __tablename__ = 'stories'

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(Text)
    score = Column(Integer, nullable=True)
    url = Column(Text)
    author = Column(Text)
    time = Column(BigInteger, nullable=True)
    descendants = Column(Integer)
    type = Column(Text)

class ETLError(Base):
    __tablename__ = "etl_errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    story_id = Column(Integer, nullable=True)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
