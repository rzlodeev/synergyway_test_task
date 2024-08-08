from src.web_driver import FirefoxWebDriver

web_driver = FirefoxWebDriver(
    user_data_link='https://jsonplaceholder.typicode.com/users',
    credit_card_data_link='https://random-data-api.com/workspaces/89a079f2-eea3-4d05-bd6b-807993438d67/db_tables/aba545fc-aa47-4c00-aec0-84088ef9c1f2',
    addresses_data_link='https://random-data-api.com/workspaces/89a079f2-eea3-4d05-bd6b-807993438d67/db_tables/ef0466d7-8858-4693-b039-b4ef97fe6c5c'
)


def test_get_user_data():
    """
    This test ensures, that user data can be extracted from corresponding API.
    Checks for 'id' field in given response.
    """
    user_data = web_driver.get_user_data()
    assert 'id' in user_data[0]


def test_get_credit_card_data():
    """
    This test ensures, that credit card data can be extracted from given API.
    """
    credit_card_data = web_driver.get_credit_card_data()
    assert 'id' in credit_card_data[0]


def test_get_addresses_data():
    """
    This test ensures, that addresses data can be extracted from the given API.
    """
    addresses_data = web_driver.get_addresses_data()
    assert 'id' in addresses_data[0]
