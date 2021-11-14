# avaitionChatbot

Using [FlightRadarAPI](https://pypi.org/project/FlightRadarAPI/)[^1] and [flightradar24.com](https://www.flightradar24.com/), to get information about certain things.


## CLASSES:

  - ### tracker

    - returns all the live flights that match the criteria, including aircraft type, airline, airport, etc., given during initialization.
      - includes aircraft type, aircraft registration, flight number, origin/destination
      - includes total and timestamp at the end   
  
    #### _Shell_
    ```
    >>> 
    >>> hkg350 = tracker(airport='HKG', aircraft='A35') # all the (live) flights to and from HKG & on an a350 (-900 or -1000)
    >>> 
    >>> hkg350.now()
    <A35K (B-LXI) - [CX845] - Origin: JFK - Destination: HKG | FR24_ID: 29d86849>
    <A359 (B-LRO) - [CX260] - Origin: CDG - Destination: HKG | FR24_ID: 29d8abdf>
    <A35K (B-LXL) - [CX288] - Origin: FRA - Destination: HKG | FR24_ID: 29d8cb37>
    <A359 (OH-LWA) - [AY101] - Origin: HEL - Destination: HKG | FR24_ID: 29d91df5>
    <A35K (B-LXG) - [CX101] - Origin: HKG - Destination: SYD | FR24_ID: 29d93586>
    <A35K (G-VPRD) - [VS207] - Origin: HKG - Destination: LHR | FR24_ID: 29d9360c>
    <A359 (B-LRS) - [CX261] - Origin: HKG - Destination: CDG | FR24_ID: 29d948aa>
    <A35K (B-LXK) - [CX251] - Origin: HKG - Destination: LHR | FR24_ID: 29d94fb4>
    <A35K (B-LXH) - [CX105] - Origin: HKG - Destination: MEL | FR24_ID: 29d95929>
    <A35K (B-LXJ) - [CX271] - Origin: HKG - Destination: AMS | FR24_ID: 29d95ab3>
    <A35K (B-LXE) - [CX289] - Origin: HKG - Destination: FRA | FR24_ID: 29d95f03>
    <A359 (B-LRP) - [CX872] - Origin: HKG - Destination: SFO | FR24_ID: 29d960a2>
    <A359 (B-LRE) - [CX2731] - Origin: HKG - Destination: DXB | FR24_ID: 29d9627f>
    <A359 (B-LRU) - [CX315] - Origin: HKG - Destination: MAD | FR24_ID: 29d96704>
    <A35K (B-LXB) - [CX675] - Origin: HKG - Destination: TLV | FR24_ID: 29d972ac>
    <A359 (B-LQE) - [CX745] - Origin: HKG - Destination: DXB | FR24_ID: 29d9903e>
    <A35K (B-LXF) - [CX844] - Origin: HKG - Destination: JFK | FR24_ID: 29d9d3b9>
    <A359 (B-LRI) - [CX254] - Origin: LHR - Destination: HKG | FR24_ID: 29d9fd53>
    <A359 (B-LRL) - [CX110] - Origin: SYD - Destination: HKG | FR24_ID: 29da081d>
    <A35K (G-VTEA) - [VS206] - Origin: LHR - Destination: HKG | FR24_ID: 29da107a>
    total: 20
    Timestamp: Sat 13 Nov 2021 14:20:26
    ```
    
  - ### schedule[^2]

    -  returns the flights requested from a certain airport within the next seven days.[^3]
    
    #### _Shell_
    ```
    >>> 
    >>> dub = schedule('dub') # for flights to and from DUB
    >>> 
    >>> # 'to' method
    >>> dub.to('cph') # flights between DUB and CPH
    >>> dub.flights # returns the data collected from previous call. in this case flights between DUB and CPH
    ... 
    >>>
    >>> # 'on' method
    >>> dub.on('ei',ein') # flights on Aer Lingus to or from DUB
    >>> dub.flights # returns the data collected from previous call. In this case flights on Aer Lingus to or from DUB
    ...
    >>> 
    >>> # 'allFlights' data
    >>> dub.allFlights # returns all the data collected from the calls. different from self.flights
    ...
    >>> 
    >>> # 'filter' method
    >>> dub.filter(aircraft='A333') # returns all the flights in self.allFlights that match the criteria in flight numbers
    ['EI132', 'EI104', 'EI122']
    >>> 
    >>> # 'get' method
    >>> dub.get('lhr') # like self.filter(airport=Param), but returns dicts instead of a list
    ... 
    >>> 
    >>> # 'flight' method
    >>> dub.flight('SK538') # returns the (first) dict corresponding to the flight number
    ...
    
    ```

[^1]: not mine, will need to edited a bit
[^2]: for some reason, data for flights got by the 'on' and 'to' methods are slightly different
[^3]: dict format → {'flight':{'number':None,'airport':{'origin':{'country':None,'IATA':None,'ICAO':None},'destination':{'country':None,'IATA':None,'ICAO':None}},'airline':{'name':None,'IATA':None,'ICAO':None},'aircraft':[],'time':{'departure':[],'arrival':[]},'operatingDays':[]}}
