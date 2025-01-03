from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True)
    message_id = Column(String, unique=True)
    sender = Column(String)
    subject = Column(String)
    received_date = Column(DateTime)
    summary = Column(Text)
    category = Column(String)
    is_processed = Column(Boolean, default=False)
    action_taken = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime) 