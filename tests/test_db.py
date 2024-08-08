import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database_config import (Base,
                                 insert_data,
                                 update_record,
                                 retrieve_data,
                                 delete_record,
                                 UserInfo,
                                 Address,
                                 CreditCardInfo)

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/db/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def get_test_db():
    """Fixture to get a test database session"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_insert_data(get_test_db):
    """
    This test ensures, that data can be inserted in the database.
    Creates a new user record, address record, updates user record with new address record. Same for credit card info.
    """

    # Create test user record
    user_data = {
        "name": "John Johnson",
        "email": "example@ex.com",
        "phone": "1234567890"
    }

    user_record = insert_data(get_test_db, UserInfo, **user_data)

    assert user_record.name == "John Johnson"
    assert user_record.email == "example@ex.com"
    assert user_record.phone == "1234567890"

    # Create test address record
    address_data = {
        "street_address": "Shevchenka str. 25",
        "city": "Zhmerynka",
        "country": "Ukraine"
    }

    address_record = insert_data(get_test_db, Address, **address_data)

    assert address_record.street_address == "Shevchenka str. 25"
    assert address_record.city == "Zhmerynka"
    assert address_record.country == "Ukraine"

    # Update the user model with address

    updated_user_record = update_record(get_test_db,
                                        UserInfo,
                                        column_id=user_record.id,
                                        **{
                                            "address_id": address_record.id
                                        })

    assert updated_user_record.address_id == address_record.id

    # Create credit card record

    credit_card_data = {
        "card_number": 1111222233334444,
        "card_expiry_date": "04/20",
        "card_type": "Pineapple Express",
        "user_id": user_record.id,
        "address_id": address_record.id
    }

    credit_card_record = insert_data(get_test_db, CreditCardInfo, **credit_card_data)

    assert credit_card_record.card_type == "Pineapple Express"


def test_retrieve_data(get_test_db):
    """This test ensures, that data can be retrieved from the database.
    Checks functionality of retrieve_data function."""

    users_records = retrieve_data(get_test_db, UserInfo)
    addresses_records = retrieve_data(get_test_db, Address)
    credit_cards_info_records = retrieve_data(get_test_db, CreditCardInfo)

    print(users_records)
    print(users_records[0].name)

    assert users_records[0].name == "John Johnson"
    assert addresses_records[0].city == "Zhmerynka"
    assert credit_cards_info_records[0].card_number == 1111222233334444


def test_update_data(get_test_db):
    """This test ensures, that data can be updated in the database.
    Checks functionality of update_record function."""

    credit_cards_info_records = retrieve_data(get_test_db, CreditCardInfo)

    credit_card_new_data = {
        "card_number": 9999888877776666
    }

    updated_credit_card_record = update_record(get_test_db,
                                               CreditCardInfo,
                                               column_id=credit_cards_info_records[0].id,
                                               **credit_card_new_data)

    assert updated_credit_card_record.card_number == 9999888877776666


def test_delete_data(get_test_db):
    """This test ensures, that data can be deleted from the database.
    Since we previously created 1 record for each table, we will delete entries with id 1 from all tables."""

    users_delete_message = delete_record(get_test_db, UserInfo, 1)
    addresses_delete_message = delete_record(get_test_db, Address, 1)
    credit_cards_delete_message = delete_record(get_test_db, CreditCardInfo, 1)

    # Message with successful deletion should look like
    # "Data with id 1 deleted from table_name"
    assert users_delete_message.startswith("Data with id")
    assert addresses_delete_message.startswith("Data with id")
    assert credit_cards_delete_message.startswith("Data with id")
