from sqlalchemy import create_engine, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = 'sqlite:///./db/database.db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

Base = declarative_base(metadata=metadata)


def init_db():
    """Init db tables"""
    Base.metadata.create_all(bind=engine)


# Define database models
class UserInfo(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    address_id = Column(Integer, ForeignKey("addresses.id"))

    address = relationship("Address", back_populates="users", uselist=False)
    credit_cards = relationship("CreditCardInfo", back_populates="user")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)

    users = relationship("UserInfo", back_populates="address")
    credit_cards = relationship("CreditCardInfo", back_populates="address")


class CreditCardInfo(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(Integer, unique=True, nullable=False, index=True)
    card_expiry_date = Column(String, nullable=False)
    card_type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("addresses.id"))

    address = relationship("Address", back_populates="credit_cards", uselist=False)
    user = relationship("UserInfo", back_populates="credit_cards", uselist=False)


# Dependency to get session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def insert_data(db: Session, model: Base, **kwargs):
    """
    Insert a new record into a specified table.
    :param db: The database Session object.
    :param model: The model class corresponding to the table.
    :param kwargs: The column data as key-value pairs.
    :return: The inserted record.
    """
    try:
        new_record = model(**kwargs)
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return new_record
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()


def update_record(db: Session, model: Base, column_id: int, **kwargs):
    """
    Update an existing record in a specified table.
    :param db: The database Session object.
    :param model: The model class corresponding to the table.
    :param column_id: ID of column that needs to be updated.
    :param kwargs: The column data as key-value pairs.
    :return: The updated record.
    """
    try:
        old_record = db.query(model).filter(model.id == column_id).first()

        if old_record is None:
            raise Exception(f"Record for {model.__tablename__} with id {column_id} not found.")

        # Update old record from database with new data
        for var, value in kwargs.items():
            setattr(old_record, var, value) if value else None

        db.add(old_record)
        db.commit()
        db.refresh(old_record)
        return old_record
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()


def retrieve_data(db: Session, model: Base):
    """
    Retrieve data from specified table
    :param db: The database Session object.
    :param model: Model class corresponding to the table
    :return:
    """
    try:
        data = db.query(model).all()
        if data is None:
            raise Exception(f"Table {model.__tablename__} not found")
        return data
    except SQLAlchemyError as e:
        raise e
    finally:
        db.close()


def delete_record(db: Session, model: Base, column_id: int):
    """
    Delete specific column from the database.
    :param db: The database Session object
    :param model: Model class corresponding to the table
    :param column_id: ID of column that needs to be deleted.
    :return: Message indicating successful deletion.
    """
    try:
        data = db.query(model).filter(model.id == column_id).first()
        if data is None:
            raise Exception(f"Column with id {column_id} not found in {model.__tablename__}")
        db.delete(data)
        db.commit()

        return f"Data with id {column_id} successfully deleted from {model.__tablename__}"
    except SQLAlchemyError as e:
        raise e
    finally:
        db.close()
