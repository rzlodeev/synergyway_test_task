from sqlalchemy.exc import SQLAlchemyError

from src.celery_config import celery_app

from src.web_driver import FirefoxWebDriver
from src.database_config import (SessionLocal,
                                 retrieve_data,
                                 UserInfo,
                                 Address,
                                 CreditCardInfo)

# Define API links here.
USER_DATA_LINK = 'https://jsonplaceholder.typicode.com/users'
CREDIT_CARD_DATA_LINK = 'https://random-data-api.com/workspaces/89a079f2-eea3-4d05-bd6b-807993438d67/db_tables/aba545fc-aa47-4c00-aec0-84088ef9c1f2'
ADDRESSES_DATA_LINK = 'https://random-data-api.com/workspaces/89a079f2-eea3-4d05-bd6b-807993438d67/db_tables/ef0466d7-8858-4693-b039-b4ef97fe6c5c'


def get_driver():
    """Initiate selenium web driver"""
    web_driver = FirefoxWebDriver(
        user_data_link=USER_DATA_LINK,
        credit_card_data_link=CREDIT_CARD_DATA_LINK,
        addresses_data_link=ADDRESSES_DATA_LINK
    )

    return web_driver


@celery_app.task
def update_user_info() -> None:
    """
    Celery task that fetches user data and updates the database.
    """
    try:
        db = SessionLocal()

        web_driver = get_driver()

        # Get data from API and store in dict
        user_data = web_driver.get_user_data()

        # Load data from database
        existing_user_data = retrieve_data(db, UserInfo)

        # Check, if id in newly fetched data exists in database.
        # If so, update it, else create new record.
        for new_user in user_data:
            existing_user = next((user for user in existing_user_data if user.id == new_user['id']), None)
            if existing_user:
                # Update existing user data
                try:
                    existing_user.name = new_user['name']
                    existing_user.email = new_user['email']
                    existing_user.phone = new_user['phone']
                    db.commit()
                except SQLAlchemyError as e:
                    db.rollback()
                    raise e
            else:
                # Create new user record
                try:
                    new_record = UserInfo(**{
                        "name": new_user["name"],
                        "email": new_user["email"],
                        "phone": new_user["phone"]
                    })
                    db.add(new_record)
                    db.commit()
                except SQLAlchemyError as e:
                    db.rollback()
                    raise e

        # Connect users to addresses.
        # Since we don't have any practical implementations, for now we just attach them randomly (by id in order)

        # Refresh data from the database
        existing_user_data = retrieve_data(db, UserInfo)
        existing_addresses_data = retrieve_data(db, Address)

        # Iterate through users and append to each of them such address_id, that doesn't exist in any other user.
        for user in existing_user_data:
            if not user.address_id and existing_addresses_data:
                user.address_id = next((address.id for address in existing_addresses_data if
                                        address.id != next((user.address_id for user in existing_user_data if
                                                            user.address_id == address.id), None)),
                                       None)
                db.add(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


@celery_app.task
def update_credit_card_info() -> None:
    """
    Celery task that fetches credit card data and updates the database.
    """
    try:
        db = SessionLocal()

        web_driver = get_driver()

        # Get data from API and store in dict
        credit_card_data = web_driver.get_credit_card_data()

        # Load data from database
        existing_credit_card_data = retrieve_data(db, CreditCardInfo)

        # Check, if id in newly fetched data exists in database.
        # If so, update it, else create new record.
        for new_credit_card in credit_card_data.values():
            existing_credit_card = next((card for card in existing_credit_card_data if
                                         card.id == new_credit_card['id']),
                                        None)
            if existing_credit_card:
                # Update existing credit card data
                try:
                    existing_credit_card.card_number = new_credit_card['card_number']
                    existing_credit_card.card_expiry_date = new_credit_card['card_expiry_date']
                    existing_credit_card.card_type = new_credit_card['card_type']
                    db.commit()
                except SQLAlchemyError as e:
                    db.rollback()
                    raise e
            else:
                # Create new credit card data
                try:
                    new_record = CreditCardInfo(**new_credit_card)
                    db.add(new_record)
                    db.commit()
                except SQLAlchemyError as e:
                    db.rollback()
                    raise e

        # Connect credit cards to users.
        # Since we don't have any practical implementations, for now we just attach them randomly (by id in order)

        # Refresh data from the database
        existing_credit_card_data = retrieve_data(db, CreditCardInfo)
        existing_user_data = retrieve_data(db, UserInfo)

        # Iterate through credit cards and append to each of them such user_id,
        # that doesn't exist in any other credit card.
        for card in existing_credit_card_data:
            if not card.user_id and existing_user_data:
                card.user_id = next((user.id for user in existing_user_data if
                                     user.id != next((card.user_id for card in existing_credit_card_data if
                                                      card.user_id == user.id), None)),
                                    None)
                db.add(card)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


@celery_app.task()
def update_addresses_info() -> None:
    """
    Celery task that fetches addresses data and updates the database.
    """
    try:
        db = SessionLocal()

        web_driver = get_driver()

        # Get data from API and store in dict
        addresses_data = web_driver.get_addresses_data()

        # Load data from database
        existing_addresses_data = retrieve_data(db, Address)

        # Check, if id in newly fetched data exists in database.
        # If so, update it, else create new record.
        for new_address in addresses_data.values():
            existing_address = next((address for address in existing_addresses_data if address.id == new_address['id']),
                                    None)
            if existing_address:
                # Update existing address data
                try:
                    existing_address.street_address = new_address['street_address']
                    existing_address.city = new_address['city']
                    existing_address.country = new_address['country']
                    db.commit()
                except SQLAlchemyError as e:
                    db.rollback()
                    raise e
            else:
                # Create new address data
                try:
                    new_record = Address(**new_address)
                    db.add(new_record)
                    db.commit()
                except SQLAlchemyError as e:
                    db.rollback()
                    raise e

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()
