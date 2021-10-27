from data_manager import DataManager
from flight_search import FlightSearch, NoFlightsError
from flight_data import FlightData
from notification_manager import NotificationManager
from os import environ
from dotenv import load_dotenv
from tqdm import tqdm


def update_iata_codes(data_manager: DataManager):
    for city_record in tqdm(data_manager.sheet_data):
        city_name = city_record["city"]
        city_id = city_record["id"]

        code = flight_search.get_iata_code(city_name)
        city_record["iataCode"] = code
        data_manager.edit_row(row_id=city_id, iata_code=code)


def send_notification(notification_manager: NotificationManager, flight_data: FlightData):
    msg_text = flight_data.make_email()
    notification_manager.send_email(to_email=notification_manager.email,
                                    message_text=msg_text)


# Loads environment variables
load_dotenv()

SHEETY_AUTH_TOKEN = environ["SHEETY_AUTH_TOKEN"]
SHEETY_ENDPOINT = environ["SHEETY_ENDPOINT"]

KIWI_TEQUILA_API_KEY = environ["KIWI_TEQUILA_API_KEY"]
KIWI_TEQUILA_SEARCH_ENDPOINT = environ["KIWI_TEQUILA_SEARCH_ENDPOINT"]
KIWI_TEQUILA_LOCATIONS_ENDPOINT = environ["KIWI_TEQUILA_LOCATIONS_ENDPOINT"]

MY_EMAIL = environ["MY_EMAIL"]
MY_PASSWORD = environ["MY_PASSWORD"]

UPDATE_IATA_CODES = True

data_manager = DataManager(auth_token=SHEETY_AUTH_TOKEN,
                           endpoint=SHEETY_ENDPOINT)

flight_search = FlightSearch(api_key=KIWI_TEQUILA_API_KEY,
                             location_endpoint=KIWI_TEQUILA_LOCATIONS_ENDPOINT,
                             search_endpoint=KIWI_TEQUILA_SEARCH_ENDPOINT)

notification_manager = NotificationManager(email=MY_EMAIL,
                                           password=MY_PASSWORD)

# Update IATA codes:
if UPDATE_IATA_CODES:
    update_iata_codes(data_manager)

# Find flights and send emails
for city_record in tqdm(data_manager.sheet_data):
    code = city_record["iataCode"]
    price = city_record["lowestPrice"]
    try:
        city_flight_data = flight_search.search_flights(iata_code=code, max_price=price + 2000)
    except NoFlightsError:
        continue
    send_notification(notification_manager, city_flight_data)
