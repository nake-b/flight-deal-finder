import requests
from re import sub


def camel_case(string: str) -> str:
    """
    Return camelCase of a given string

    :param string: the string to be converted
    :return: the string in camelCase
    :rtype: str
    """
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return ''.join([string[0].lower(), string[1:]])


class DataManager:

    def __init__(self, auth_token: str, endpoint: str):
        """
        Constructs a DataManager object with given "Sheety" API parameters

        :param auth_token: the sheet's "Bearer" authentication token
        :param endpoint: the sheet's endpoint
        .. seealso:: https://dashboard.sheety.co/projects/{your_project_id}
        """
        self.endpoint = endpoint

        self.sheet_name = self.endpoint.split('/')[-1]
        self.sheet_post_request_name = self.sheet_name[:-1] if self.sheet_name[-1] == 's' else self.sheet_name

        self.get_headers = {"Authorization": "Bearer " + auth_token}
        self.post_headers = self.get_headers
        self.post_headers["Content-Type"] = "application/json"

    def __get_request(self, **kwargs) -> requests.request:
        """
        Send a get request to sheet's endpoint

        :param payload: the params keyword argument for requests.get method
        :return: response from the get request sent to the sheet's endpoint
        :rtype: requests.request
        """
        response = requests.get(url=self.endpoint,
                                params=kwargs,
                                headers=self.get_headers)
        response.raise_for_status()
        return response

    def get_rows(self, row_id=None) -> list:
        """
        Return rows from the Google Sheet connected to "Sheety"

        :param row_id: row number of the desired row in the Google Sheet
        :return: response from the sheet's endpoint in json format
        :rtype: list
        """
        response = self.__get_request(id=row_id)
        data = response.json()["prices"]
        return data

    def filter_rows(self, **kwargs) -> list:
        """
        Return filtered rows from the Google Sheet

        :param kwargs: sheet's column names in snake or camel case as keys and corresponding values as values
        :return: response from the sheet's endpoint in json format
        :rtype: list

        :example:

        >>> data_manager = DataManager(auth_token, endpoint)
        >>> row_data = data_manager.filter_rows(lowest_price=54)
                [
          {
            "city": "Berlin",
            "iataCode": "",
            "lowestPrice": 42,
            "id": 3
          }
        ]
        """
        payload = {f"filter[{camel_case(str(key))}]": value for key, value in kwargs.items()}

        response = self.__get_request(**payload)
        data = response.json()["prices"]
        return data
