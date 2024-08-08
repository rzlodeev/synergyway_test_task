import argparse
from fastapi import FastAPI

from src.database_config import SessionLocal, init_db, retrieve_data, UserInfo, Address, CreditCardInfo
from src.tasks import update_user_info, update_addresses_info, update_credit_card_info

# Config FastAPI endpoint for retrieving data from the database.
app = FastAPI()

init_db()
db = SessionLocal()


@app.get("/show-data")
def get_data():
    users = retrieve_data(db, UserInfo)
    addresses = retrieve_data(db, Address)
    credit_cards = retrieve_data(db, CreditCardInfo)

    return {
        "users": [row for row in users],
        "addresses": [row for row in addresses],
        "credit_cards": [row for row in credit_cards]
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Updating and retrieving data from the database.")
    parser.add_argument('-r', '--retrieve', action="store_true", help="Retrieve all data entries.")
    parser.add_argument('--update-users', action="store_true", help="Update users database with info from API.")
    parser.add_argument('--update-addresses', action="store_true", help="Update addresses database with info from API.")
    parser.add_argument('--update-cards', action="store_true", help="Update credit cards database with info from API.")

    args = parser.parse_args()
    init_db()
    db = SessionLocal()

    if args.retrieve:
        # Iterate through each table and print it values
        users_data = retrieve_data(db, UserInfo)

        print("ID | NAME | EMAIL | PHONE | ADDRESS ID")
        for user in users_data:
            print(f"{user.id} | {user.name} | {user.email} | {user.phone} | {user.address_id}")

        addresses_data = retrieve_data(db, Address)

        print("ID | STREET ADDRESS | CITY | COUNTRY")
        for address in addresses_data:
            print(f"{address.id} | {address.street_address} | {address.city} | {address.country}")

        credit_cards_data = retrieve_data(db, CreditCardInfo)

        print("ID | CARD NUMBER | CARD EXP DATE | CARD TYPE | USER ID | ADDRESS ID")
        for card in credit_cards_data:
            print(f"{card.id} | {card.card_number} | {card.card_expiry_date} | {card.card_type} | {card.address_id}")

    if args.update_users:
        update_user_info()
        print("User info updated. Call -r to see updated data")

    if args.update_cards:
        update_credit_card_info()
        print("Credit info updated. Call -r to see updated data")

    if args.update_addresses:
        update_addresses_info()
        print("Addresses info updated. Call -r to see updated data")

