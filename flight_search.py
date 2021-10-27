import requests
from datetime import datetime, timedelta
from flight_data import FlightData
from misc import jprint

DEPARTURE_COUNTRY = "BA"


class FlightSearch:

    def __init__(self, api_key: str, search_endpoint: str, location_endpoint: str):
        self.api_key = api_key
        self.search_endpoint = search_endpoint
        self.location_endpoint = location_endpoint

        self.departure_country = DEPARTURE_COUNTRY
        self.no_of_adults = 2
        self.date_format = "%d/%m/%Y"

    def __get_request(self, endpoint, **kwargs):
        payload = kwargs
        headers = {"apikey": self.api_key}

        response = requests.get(params=payload, url=endpoint, headers=headers)
        response.raise_for_status()
        return response

    def get_iata_code(self, city):
        response = self.__get_request(endpoint=self.location_endpoint,
                                      term=city,
                                      location_types="city",
                                      limit=1)
        data = response.json()
        code = data["locations"][0]["code"]
        return code

    def search_flights(self, iata_code, max_price):
        current_date = datetime.now()
        current_date_string = current_date.strftime(self.date_format)

        time_interval = timedelta(days=6 * 30)
        max_date = current_date + time_interval
        max_date_string = max_date.strftime(self.date_format)

        response = self.__get_request(endpoint=self.search_endpoint,
                                      fly_from=self.departure_country,
                                      fly_to=iata_code,
                                      date_from=current_date_string,
                                      date_to=max_date_string,
                                      nights_in_dst_from=7,
                                      nights_in_dst_to=28,
                                      flight_type="round",
                                      adults=self.no_of_adults,
                                      price_to=max_price,
                                      curr="EUR",
                                      limit=1
                                      )
        data = response.json()
        # jprint(data)
        data = FlightData(data)
        return data
