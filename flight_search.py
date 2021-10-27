import requests


class FlightSearch:

    def __init__(self, api_key: str, search_endpoint: str, location_endpoint: str):
        self.api_key = api_key
        self.search_endpoint = search_endpoint
        self.location_endpoint = location_endpoint

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
