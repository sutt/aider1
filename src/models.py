from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class FactorialResult(Base):
    __tablename__ = "factorial_results"

    id = Column(Integer, primary_key=True, index=True)
    input_number = Column(Integer)
    result = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
