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

        def __init__(self, route_data: dict):
            self.departure_city = route_data["cityFrom"]
            self.departure_code = route_data["cityCodeFrom"]

            self.arrival_city = route_data["cityTo"]
            self.arrival_code = route_data["cityCodeTo"]

            self.airline = route_data["airline"]
            self.flight_no = route_data["flight_no"]

            # PARSE THESE TIME STRINGS!!!
            self.departure_time = route_data["local_departure"]
            self.arrival_time = route_data["local_arrival"]

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




