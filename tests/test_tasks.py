from unittest.mock import patch

from src.tasks import update_user_info, update_addresses_info, update_credit_card_info
from src.database_config import retrieve_data, UserInfo, Address, CreditCardInfo


def test_fetch_and_refresh(get_test_db):
    """
    This test ensures, that tasks given to celery fetch data from API and update the database.
    """
    # Launch tasks
    with patch('src.tasks.SessionLocal', return_value=get_test_db):
        update_addresses_info()
        update_user_info()
        update_credit_card_info()

    # Retrieve data from the database
    addresses_data = retrieve_data(get_test_db, Address)
    users_data = retrieve_data(get_test_db, UserInfo)
    credit_cards_data = retrieve_data(get_test_db, CreditCardInfo)

    # Ensure that data retrieved and is not empty
    assert isinstance(addresses_data[0].id, int)
    assert isinstance(users_data[0].id, int)
    assert isinstance(credit_cards_data[0].id, int)
