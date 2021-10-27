from data_manager import DataManager
from flight_search import FlightSearch
from misc import jprint
from os import environ
from dotenv import load_dotenv
from tqdm import tqdm


# Loads environment variables
load_dotenv()

SHEETY_AUTH_TOKEN = environ["SHEETY_AUTH_TOKEN"]
SHEETY_ENDPOINT = environ["SHEETY_ENDPOINT"]

KIWI_TEQUILA_API_KEY = environ["KIWI_TEQUILA_API_KEY"]
KIWI_TEQUILA_SEARCH_ENDPOINT = environ["KIWI_TEQUILA_SEARCH_ENDPOINT"]
KIWI_TEQUILA_LOCATIONS_ENDPOINT = environ["KIWI_TEQUILA_LOCATIONS_ENDPOINT"]

data_manager = DataManager(auth_token=SHEETY_AUTH_TOKEN,
                           endpoint=SHEETY_ENDPOINT)

# r = data_manager.get_rows()
# r = data_manager.filter_rows(lowest_price=42)
# jprint(r)

flight_search = FlightSearch(api_key=KIWI_TEQUILA_API_KEY,
                             location_endpoint=KIWI_TEQUILA_LOCATIONS_ENDPOINT,
                             search_endpoint=KIWI_TEQUILA_SEARCH_ENDPOINT)


# Update IATA codes:
for city_record in tqdm(data_manager.sheet_data):
    city_name = city_record["city"]
    city_id = city_record["id"]

    code = flight_search.get_iata_code(city_name)
    city_record["iataCode"] = code

    data_manager.edit_row(row_id=city_id, iata_code=code)

