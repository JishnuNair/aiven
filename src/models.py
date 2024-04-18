from sqlalchemy import Column, Integer, String, DateTime, MetaData, Float, func, Index, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TEXT

Base = declarative_base(metadata=MetaData())


class YellowTrips(Base):
    """
    Define the schema for the yellow taxi trips table
    """
    __tablename__ = 'yellow_trips'
    _ID = Column(String, primary_key=True)
    VENDORID = Column(Integer)
    TPEP_PICKUP_DATETIME = Column(DateTime)
    TPEP_DROPOFF_DATETIME = Column(DateTime)
    PASSENGER_COUNT = Column(Float)
    TRIP_DISTANCE = Column(Float)
    RATECODEID = Column(Float)
    STORE_AND_FWD_FLAG = Column(TEXT)
    PULOCATIONID = Column(Integer)
    DOLOCATIONID = Column(Integer)
    PAYMENT_TYPE = Column(BigInteger)
    FARE_AMOUNT = Column(Float)
    EXTRA = Column(Float)
    MTA_TAX = Column(Float)
    TIP_AMOUNT = Column(Float)
    TOLLS_AMOUNT = Column(Float)
    IMPROVEMENT_SURCHARGE = Column(Float)
    TOTAL_AMOUNT = Column(Float)
    CONGESTION_SURCHARGE = Column(Float)
    AIRPORT_FEE = Column(Float)
    INSERT_DATE = Column(DateTime, server_default=func.now())
    UPDATE_DATE = Column(DateTime, onupdate=func.now())

    # Create indexes
    idx_vendorid = Index('idx_vendorid', VENDORID)
    idx_pickup_datetime = Index('idx_pickup_datetime', TPEP_PICKUP_DATETIME)
    idx_dropoff_datetime = Index('idx_dropoff_datetime', TPEP_DROPOFF_DATETIME)


class GreenTrips(Base):
    """
    Define the schema for the green taxi trips table
    """
    __tablename__ = 'green_trips'
    _ID = Column(String, primary_key=True)
    VENDORID = Column(Integer)
    LPEP_PICKUP_DATETIME = Column(DateTime)
    LPEP_DROPOFF_DATETIME = Column(DateTime)
    STORE_AND_FWD_FLAG = Column(TEXT)
    RATECODEID = Column(Float)
    PULOCATIONID = Column(Integer)
    DOLOCATIONID = Column(Integer)
    PASSENGER_COUNT = Column(Float)
    TRIP_DISTANCE = Column(Float)
    FARE_AMOUNT = Column(Float)
    EXTRA = Column(Float)
    MTA_TAX = Column(Float)
    TIP_AMOUNT = Column(Float)
    TOLLS_AMOUNT = Column(Float)
    EHAIL_FEE = Column(Float)
    IMPROVEMENT_SURCHARGE = Column(Float)
    TOTAL_AMOUNT = Column(Float)
    PAYMENT_TYPE = Column(Float)
    TRIP_TYPE = Column(Float)
    CONGESTION_SURCHARGE = Column(Float)
    INSERT_DATE = Column(DateTime, server_default=func.now())
    UPDATE_DATE = Column(DateTime, onupdate=func.now())

    # Create indexes
    idx_vendorid = Index('idx_green_vendorid', VENDORID)
    idx_pickup_datetime = Index('idx_lpep_pickup_datetime', LPEP_PICKUP_DATETIME)
    idx_dropoff_datetime = Index('idx_lpep_dropoff_datetime', LPEP_DROPOFF_DATETIME)
