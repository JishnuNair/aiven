from sqlalchemy import Column, Integer, String, DateTime, MetaData, Float, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=MetaData(schema="your_schema"))


class YellowTrips(Base):
    """
    Define the schema for the yellow taxi trips table
    """
    __tablename__ = 'yellow_trips'
    _id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer)
    tpep_pickup_datetime = Column(DateTime)
    tpep_dropoff_datetime = Column(DateTime)
    passenger_count = Column(Float)
    trip_distance = Column(Float)
    rate_code_id = Column(Float)
    store_and_fwd_flag = Column(String)
    pu_location_id = Column(Integer)
    do_location_id = Column(Integer)
    payment_type = Column(Integer)
    fare_amount = Column(Float)
    extra = Column(Float)
    mta_tax = Column(Float)
    tip_amount = Column(Float)
    tolls_amount = Column(Float)
    improvement_surcharge = Column(Float)
    total_amount = Column(Float)
    congestion_surcharge = Column(Float)
    airport_fee = Column(Float)
    insert_date = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime, onupdate=func.now())


class GreenTrips(Base):
    """
    Define the schema for the green taxi trips table
    """
    __tablename__ = '_stg_green_trips'
    _id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer)
    lpep_pickup_datetime = Column(DateTime)
    lpep_dropoff_datetime = Column(DateTime)
    store_and_fwd_flag = Column(String)
    rate_code_id = Column(Float)
    pu_location_id = Column(Integer)
    do_location_id = Column(Integer)
    passenger_count = Column(Float)
    trip_distance = Column(Float)
    fare_amount = Column(Float)
    extra = Column(Float)
    mta_tax = Column(Float)
    tip_amount = Column(Float)
    tolls_amount = Column(Float)
    ehail_fee = Column(Float)
    improvement_surcharge = Column(Float)
    total_amount = Column(Float)
    payment_type = Column(Float)
    trip_type = Column(Float)
    congestion_surcharge = Column(Float)
    insert_date = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime, onupdate=func.now())
