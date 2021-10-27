from dataclasses import dataclass


@dataclass
class FlightData:
    @dataclass
    class OneWayData:
        departure_city: str
        departure_code: str
        arrival_city: str
        arrival_code: str
        airline: str
        flight_no: int
        departure_time: str
        arrival_time: str
        departure_date: str
        arrival_date: str

        def __init__(self, route_data: dict):
            self.departure_city = route_data["cityFrom"]
            self.departure_code = route_data["cityCodeFrom"]

            self.arrival_city = route_data["cityTo"]
            self.arrival_code = route_data["cityCodeTo"]

            self.airline = route_data["airline"]
            self.flight_no = route_data["flight_no"]

            def parse_datetime(datetime: str):
                datetime = datetime[:-1]
                datetime_split = datetime.split('T')
                return datetime_split[0], datetime_split[1][:-7]

            departure_datetime = route_data["local_departure"]
            arrival_datetime = route_data["local_arrival"]

            self.departure_date, self.departure_time = parse_datetime(departure_datetime)
            self.arrival_date, self.arrival_time = parse_datetime(arrival_datetime)

    from_data: OneWayData
    back_data: OneWayData

    no_of_nights: str
    price: float

    def __init__(self, data_dict: dict):
        data = data_dict["data"][0]

        self.no_of_nights = data["nightsInDest"]
        self.price = data["price"]

        from_route = data["route"][0]
        back_route = data["route"][1]

        self.from_data = self.OneWayData(from_route)
        self.back_data = self.OneWayData(back_route)

    def make_email(self):
        message = f"Greetings! I found a flight from {self.from_data.departure_city} to {self.from_data.arrival_city}" \
                  f" on {self.from_data.departure_date} at {self.from_data.departure_time}, " \
                  f"on airline {self.from_data.airline},flight no {self.from_data.flight_no}. " \
                  f"The price of the flight is {self.price} Euros, and the number of nights that you would spend is " \
                  f"{self.no_of_nights}. The flight back is from {self.back_data.departure_city} on " \
                  f"{self.back_data.departure_date} at {self.back_data.departure_time}, on airline " \
                  f"{self.back_data.airline}, flight no {self.back_data.flight_no}. " \
                  f"This program can be improved to reserve a ticket, but it's not yet implemented. "

        return message
