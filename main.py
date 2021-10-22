from data_manager import DataManager
from flight_search import FlightSearch
from os import environ
from dotenv import load_dotenv
import json
import requests


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

print(flight_search.get_iata_code("Berlin"))
