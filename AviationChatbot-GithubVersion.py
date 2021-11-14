
'''
'AviationChatbot'
using the flightradar24 api and other methods to get information
'''

from flightRadarAPIcopy import FlightRadar24API
fr24 = FlightRadar24API()

import requests
#from bs4 import BeautifulSoup

import copy

import time as t

class tracker:

    def __init__(self, airline = None, bounds = None, airport = None, aircraft = None, number = None, registration = None, template = None):
        """
        Parameter airline: must be the airline ICAO. Ex: "DAL", "UAE"
        Parameter bounds: must be coordinates (y1, y2 ,x1, x2). Ex: "75.78,-75.78,-427.56,427.56"
        Parameter airport: must be the airport IATA. Ex: "SFO", "LHR"
        Parameter aircraft: must the aircraft ICAO type designator. Ek: "A38", "B748"
        Parameter number: must the the IATA flight number. Ex: "KE214", "OZ211"
        Parameter registration: must be the official registration of the aircraft. Ex: "G-XLEG", "N24974"

        Parameter template: the template for which the results will be printed. see tracker.setTemplate()
        """
        
        try: self.airline = airline.upper()
        except: self.airline = None
        self.bounds = bounds
        try: self.airport = airport.upper()
        except: self.airport = None
        try: self.aircraft = aircraft.upper()
        except: self.aircraft = None
        try: self.number = number.upper()
        except: self.number = None
        try: self.registration = registration.upper()
        except: self.registration = None

        self.parameters = {'airline':self.airline,'bounds':self.bounds,'airport':self.airport,'aircraft':self.aircraft,'number':self.number,'registration':self.registration}
        
        if template: self.template = template
        else: self.template = '<{ac} ({reg}) - [{num}] - Origin: {oa} - Destination: {da} | FR24_ID: {id}>'

    def setTemplate(self, template):
        '''
        {id}: flight_id
        {alt}: altitude
        {cs}: callsign
        {al}: airline ICAO
        {num}: flight number IATA
        {reg}: registration
        {ac}: aircraft ICAO
        {oa}: origin airport IATA
        {da}: destination airport IATA
        '''
        self.template = template
        

    def now(self):
        flights = fr24.get_flights(**self.parameters)

        '''
        {id}: x
        {alt}: [x][4]
        {cs}: [x][16]
        {al}: [x][18]
        {num}: [x][13]
        {reg}: [x][9]
        {ac}: [x][8]
        {oa}: [x][11]
        {da}: [x][12]
        '''

        for x in flights:
            print(self.template.format(**{'id': x,'alt': flights[x][4],'cs': flights[x][16],'al': flights[x][18],'num': flights[x][13],'reg': flights[x][9],'ac': flights[x][8],'oa': flights[x][11],'da': flights[x][12]}))
        print(f'total: {len(flights)}')
        print(f'Timestamp: {t.strftime("%a %d %b %Y %H:%M:%S")}')
        
#################################################################################################################

from FlightRadar24.core import Core

class schedule:
    # ERROR: the origin and destination are mixed; one will always be the origin and the other the destination no matter what
    '''
    Methods:
        to(self, destination)
            

        get(slef, destination)
            Returns the assosiated list of dicts cached from the to() method

    Data:
        flights
            list of dicts.
            format of dicts:
                {
                'flight':
                    {
                    'number':
                        flightNumber,
                    'airport':
                        {
                        'origin':
                        {
                            'IATA':
                                originAirportIATA,
                            'ICAO':
                                originAirportICAO
                        },
                        'destination':
                        {
                            'IATA':
                                destinationAirportIATA,
                            'ICAO':
                                destinationAirportICAO
                        }
                        },
                    'airline':
                        {
                        'name':name,
                        'IATA':iata,
                        'ICAO':icao
                        },
                    'aircraft':
                        [aircraft],
                    'time':
                        {
                        'departure':[timeOfDeparture],
                        'arrival':[timeOfArrival]
                        },
                    'operatingDays':
                        [Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday]
                    }
                }
        
    '''

    def __init__(self, origin):
        if fr24.get_airport(origin): self.o = fr24.get_airport(origin)
        
        self.rootURL = f'https://www.flightradar24.com/data/airports/{self.o["code"]["iata"]}/routes?get-airport-arr-dep=DESTINATION&format=json'
        self.flights = [] # list of dicts for the most recent request
        self.allFlights = {} # dict of the lists for all the requests; {'airport1':[self.flights]}

        self.dictTemplate = {'flight':{'number':None,'airport':{'origin':{'country':None,'IATA':None,'ICAO':None},'destination':{'country':None,'IATA':None,'ICAO':None}},'airline':{'name':None,'IATA':None,'ICAO':None},'aircraft':[],'time':{'departure':[],'arrival':[]},'operatingDays':[]}}

    def to(self, destination):
        '''
        Param destination: the IATA or ICAO code (upper or lower case is accepted)
        Finds all the flights from the set origin to the inputted destination. returns list of dicts.
        '''

        if fr24.get_airport(destination): self.d = fr24.get_airport(destination)['code']['iata']
        
        page = requests.get(self.rootURL.replace('DESTINATION', self.d), headers=Core.headers)
        page = page.json() # is a python dict
        
        
        if not(page): return(False) # if there are no flights; page == []
        
        else:

            self.flights.clear()
            
            country = list(page['arrivals'].keys())[0]
            
            for x in page['arrivals'][country]['airports'][self.d.upper()]['flights']: # flights arriving from self.o
                f = copy.deepcopy(self.dictTemplate)
                
                ###
                f['flight']['number'] = x
                #
                f['flight']['airport']['origin']['country'] = self.o['position']['country']['name']
                f['flight']['airport']['origin']['IATA'] = self.o['code']['iata'].upper()
                f['flight']['airport']['origin']['ICAO'] = self.o['code']['icao']

                f['flight']['airport']['destination']['country'] = country
                f['flight']['airport']['destination']['IATA'] = self.d.upper()
                f['flight']['airport']['destination']['ICAO'] = page['departures'][country]['airports'][self.d.upper()]['icao']
                #
                f['flight']['airline']['name'] = page['arrivals'][country]['airports'][self.d.upper()]['flights'][x]['airline']['name']
                f['flight']['airline']['IATA'] = page['arrivals'][country]['airports'][self.d.upper()]['flights'][x]['airline']['iata']
                f['flight']['airline']['ICAO'] = page['arrivals'][country]['airports'][self.d.upper()]['flights'][x]['airline']['icao']
                #
                for n in page['arrivals'][country]['airports'][self.d.upper()]['flights'][x]['utc']:
                    ##
                    f['flight']['aircraft'].append(page['arrivals'][country]['airports'][self.d.upper()]['flights'][x]['utc'][n]['aircraft'])
                    #
                    f['flight']['time']['arrival'].append(t.strftime('%H:%M',t.gmtime(page['arrivals'][country]['airports'][self.d.upper()]['flights'][x]['utc'][n]['timestamp']+page['arrivals'][country]['airports'][self.d.upper()]['flights'][x]['utc'][n]['offset'])))
                    #
                    f['flight']['operatingDays'].append(t.strftime('%A',t.gmtime(page['arrivals'][country]['airports'][self.d.upper()]['flights'][x]['utc'][n]['timestamp']+page['arrivals'][country]['airports'][self.d.upper()]['flights'][x]['utc'][n]['offset']))) #-86400
                    ###
                ###

                self.flights.append(f)
            #####
            for x in page['departures'][country]['airports'][self.d.upper()]['flights']: # flights departing from self.o
                f = copy.deepcopy(self.dictTemplate)
                
                ###
                f['flight']['number'] = x
                #
                f['flight']['airport']['origin']['country'] = country
                f['flight']['airport']['origin']['IATA'] = self.d.upper()
                f['flight']['airport']['origin']['ICAO'] = page['arrivals'][country]['airports'][self.d.upper()]['icao']

                f['flight']['airport']['destination']['country'] = self.o['position']['country']['name']
                f['flight']['airport']['destination']['IATA'] = self.o['code']['iata'].upper()
                f['flight']['airport']['destination']['ICAO'] = self.o['code']['icao']
                #
                f['flight']['airline']['name'] = page['departures'][country]['airports'][self.d.upper()]['flights'][x]['airline']['name']
                f['flight']['airline']['IATA'] = page['departures'][country]['airports'][self.d.upper()]['flights'][x]['airline']['iata']
                f['flight']['airline']['ICAO'] = page['departures'][country]['airports'][self.d.upper()]['flights'][x]['airline']['icao']
                #
                for n in page['departures'][country]['airports'][self.d.upper()]['flights'][x]['utc']:
                    ##
                    f['flight']['aircraft'].append(page['departures'][country]['airports'][self.d.upper()]['flights'][x]['utc'][n]['aircraft'])
                    #
                    f['flight']['time']['departure'].append(t.strftime('%H:%M',t.gmtime(page['departures'][country]['airports'][self.d.upper()]['flights'][x]['utc'][n]['timestamp']+page['departures'][country]['airports'][self.d.upper()]['flights'][x]['utc'][n]['offset'])))
                    #
                    f['flight']['operatingDays'].append(t.strftime('%A',t.gmtime(page['departures'][country]['airports'][self.d.upper()]['flights'][x]['utc'][n]['timestamp']+page['departures'][country]['airports'][self.d.upper()]['flights'][x]['utc'][n]['offset']))) #-86400
                    ###
                ###

                self.flights.append(f)
        try: self.allFlights[self.d.lower()]
        except KeyError: self.allFlights[self.d.lower()] = copy.deepcopy(self.flights) # check to make sure self.flights is list# the airport is not in the dict
        else:
            if self.flights not in self.allFlights[self.d.lower()]:
                self.allFlights[self.d.lower()].extend(copy.deepcopy(self.flights)) # the airport is already in the dict
            else:
                pass

        ######

        for x in self.allFlights:
            for n in self.allFlights[x]:
                if self.allFlights[x].count(n) > 1: self.allFlights[x].remove(n)
            
#############
    def on(self, iata, icao):
        '''
        Param iata, icao: the IATA, ICAO for the SAME airline
        '''
        global page
        page = requests.get(f'https://www.flightradar24.com/data/airlines/{iata}-{icao}/routes?get-airport-arr-dep={self.o["code"]["iata"]}&format=json', headers=Core.headers)
##        print(page.url)
        page = page.json()

        airline = fr24.get_airlines()
        for x in airline:
            if x['ICAO'] == icao.upper():
                airline = x
                break
        if type(airline) is list: # icao didn't math any airline
            raise(RuntimeError('Param \'icao\' is not valid'))
    
        for a in page['arrivals']:
            country = a
            airports = [p for p in page['arrivals'][country]['airports']]
            
            for p in airports:
                for x in page['arrivals'][country]['airports'][p]['flights']: # flights arriving from self.o
                    f = copy.deepcopy(self.dictTemplate)
                    
                    ###
                    f['flight']['number'] = x
                    #
                    f['flight']['airport']['origin']['country'] = country
                    f['flight']['airport']['origin']['IATA'] = p
                    try: f['flight']['airport']['origin']['ICAO'] = page['departures'][country]['airports'][p]['icao'] #for 'milk run' / cargo flights / ferry flights
                    except: pass

                    f['flight']['airport']['destination']['country'] = self.o['position']['country']['name']
                    f['flight']['airport']['destination']['IATA'] = self.o['code']['iata'].upper()
                    f['flight']['airport']['destination']['ICAO'] = self.o['code']['icao']
                    #
                    f['flight']['airline']['name'] = airline['Name']
                    f['flight']['airline']['IATA'] = airline['Code']
                    f['flight']['airline']['ICAO'] = airline['ICAO']
                    #
                    for n in page['arrivals'][country]['airports'][p]['flights'][x]['utc']:
                        ##
                        f['flight']['aircraft'].append(page['arrivals'][country]['airports'][p]['flights'][x]['utc'][n]['aircraft'])
                        #
                        f['flight']['time']['arrival'].append(t.strftime('%H:%M',t.gmtime(page['arrivals'][country]['airports'][p]['flights'][x]['utc'][n]['timestamp']+page['arrivals'][country]['airports'][p]['flights'][x]['utc'][n]['offset'])))
                        #
                        f['flight']['operatingDays'].append(t.strftime('%A',t.gmtime(page['arrivals'][country]['airports'][p]['flights'][x]['utc'][n]['timestamp']+page['arrivals'][country]['airports'][p]['flights'][x]['utc'][n]['offset']))) #-86400
                        ###
                    ###
                    self.flights.append(f)
        #####
        for a in page['departures']:
            country = a
            airports = [p for p in page['departures'][country]['airports']]
            
            for p in airports:
                
                for x in page['departures'][country]['airports'][p]['flights']: # flights departing from self.o
                    f = copy.deepcopy(self.dictTemplate)
                    
                    ###
                    f['flight']['number'] = x
                    #
                    f['flight']['airport']['origin']['country'] = self.o['position']['country']['name']
                    f['flight']['airport']['origin']['IATA'] = self.o['code']['iata'].upper()
                    f['flight']['airport']['origin']['ICAO'] = self.o['code']['icao']

                    f['flight']['airport']['destination']['country'] = country
                    f['flight']['airport']['destination']['IATA'] = p
                    try: f['flight']['airport']['destination']['ICAO'] = page['arrivals'][country]['airports'][p]['icao'] #for 'milk run' / cargo flights / ferry flights
                    except: pass
                    #
                    f['flight']['airline']['name'] = airline['Name']
                    f['flight']['airline']['IATA'] = airline['Code']
                    f['flight']['airline']['ICAO'] = airline['ICAO']
                    #
                    for n in page['departures'][country]['airports'][p]['flights'][x]['utc']:
                        ##
                        f['flight']['aircraft'].append(page['departures'][country]['airports'][p]['flights'][x]['utc'][n]['aircraft'])
                        #
                        #print(f['flight']['time'])
                        f['flight']['time']['departure'].append(t.strftime('%H:%M',t.gmtime(page['departures'][country]['airports'][p]['flights'][x]['utc'][n]['timestamp']+page['departures'][country]['airports'][p]['flights'][x]['utc'][n]['offset'])))
                        #
                        f['flight']['operatingDays'].append(t.strftime('%A',t.gmtime(page['departures'][country]['airports'][p]['flights'][x]['utc'][n]['timestamp']+page['departures'][country]['airports'][p]['flights'][x]['utc'][n]['offset']))) #-86400
                        ###
                    ###
                    self.flights.append(f)
                
        for x in self.flights:
            try:
                self.allFlights[x['flight']['airport'][('origin' if (x['flight']['airport']['origin']['IATA'] != self.o['code']['iata'].upper()) else 'destination')]['IATA'].lower()]
            except KeyError:                
                self.allFlights[x['flight']['airport'][('origin' if (x['flight']['airport']['origin']['IATA'] != self.o['code']['iata'].upper()) else 'destination')]['IATA'].lower()] = [x]
            else:
                #print(type(self.allFlights[x['flight']['airport'][('origin' if (x['flight']['airport']['origin']['IATA'] != self.o['code']['iata'].upper()) else 'destination')]['IATA'].lower()]))
                self.allFlights[x['flight']['airport'][('origin' if (x['flight']['airport']['origin']['IATA'] != self.o['code']['iata'].upper()) else 'destination')]['IATA'].lower()].append(x)
        ######

        for x in self.allFlights:
            #print(self.allFlights[x])
            for n in self.allFlights[x]:
                if self.allFlights[x].count(n) > 1: self.allFlights[x].remove(n)
        

    def get(self, destination):
        if fr24.get_airport(destination): return(self.allFlights[fr24.get_airport(destination)['code']['iata'].lower()])
    def flight(self, flightNumber): #, error=None
        '''
        Param flightNumber: the IATA flight number. eg. BA1
        #Param error: the error message if flight is not found
        '''
        #found = 0
        for p in self.allFlights:
            for f in self.allFlights[p]:
                if f['flight']['number'] == flightNumber.upper():
                    #found += 1
                    return(f)
##        if not(found) and not(error): return(f'{flightNumber} is not in allFlights')
##        else: return(error)


    def filter(self, aircraft=None, airport=None, airline=None, operatingDay=None):
        '''
        searches through all of self.allFlights to find EXACT matches with the parameters. returns list of flight numbers

        Param aircraft: the 4-character (A333) designator of an aircraft
        Param airport: the IATA or ICAO code of an airport
        Param airline: the IATA or ICAO code of an airline
        Param operatingDays: one of the following: [Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday]
        '''

        matching = [] # list of flight numbers that mathch the criteria

        if aircraft: aircraft = aircraft.upper()
        if airport: airport = fr24.get_airport(airport)['code']['iata'].upper()
        if airline: airline = airline.upper()
        if operatingDay: operatingDay = operatingDay.title()
        
        
        for n in self.allFlights:
            for x in self.allFlights[n]:
                if ((aircraft[-3:] in x['flight']['aircraft'] or aircraft in x['flight']['aircraft']) if aircraft else True) \
                   and \
                   ((x['flight']['airport']['origin']['IATA'] == airport or x['flight']['airport']['destination']['IATA'] == airport) if airport else True) \
                   and \
                   ((airline == ((x['flight']['airline']['IATA']) if (len(airline) == 2) else (x['flight']['airline']['ICAO']))) if airline else True) \
                   and \
                   ((operatingDay in x['flight']['operatingDays']) if operatingDay else True) \
                   and \
                   ((aircraft[-3:] in x['flight']['aircraft'][x['flight']['operatingDays'].index(operatingDay)] or aircraft in x['flight']['aircraft'][x['flight']['operatingDays'].index(operatingDay)]) if (aircraft and operatingDay and operatingDay in x['flight']['operatingDays']) else True):
                    #
                    matching.append(x['flight']['number'])

        return(list(set(matching)))
