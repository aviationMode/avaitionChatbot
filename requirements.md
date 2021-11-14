# Requirements

- ### FlightRadarAPI:
   - read the [requirements for that](https://github.com/JeanExtreme002/FlightRadarAPI/blob/main/requirements.txt)

 - ### FlightRadarAPI.api:
   - the package [FlightRadarAPI](https://pypi.org/project/FlightRadarAPI/) must be installed
   - if it is installed and already in use, consider creating a copy of the .api file to use for this module
   - parts to edit:
     - on line 82
       change
       ```
       def get_flights(self, airline = None, bounds = None):
       ```
       to
       ```
       def get_flights(self, airline = None, bounds = None, airport = None, aircraft = None, number = None, registration = None):
       ```
     - change the block starting on the comment on line 91
       ```
       # Insert the parameters "airline" and "bounds" in the dictionary for the request.
       if airline: request_params["airline"] = airline
       if bounds: request_params["bounds"] = bounds.replace(",", "%2C")
       if airport: request_params["airport"] = airport
       if aircraft: request_params["type"] = aircraft
       if number: request_params["flight"] = number
       if registration: request_params["reg"] = registration
       ```
     - replace 
       ```
       flights = []
       ```
       with
       ```
       flights = {}
       ```
     - replace
       ```
       flights.append(Flight(flight_id, flight_info))
       ```
       with
       ```
       flights[flight_id] = flight_info
       ```
