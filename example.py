from aviationChatbot import *

#############################################

'''''''''''''''
#   tracker   #
'''''''''''''''

# all the flights on the 787-10
b78x = tracker(aircraft='B78X')
b78x.now() # prints all the current flights using the 787-10

# all of the a380 Emirates
EK380 = tracker(aircraft='A388', airline='UAE')
Ek380.now() # prints all the current flights using the a380 from Emirates

#############################################

''''''''''''''''''
#    schedule    #
''''''''''''''''''

# initialize the object
lhr = schedule('lhr')

lhr.on('ba','baw') # all the flights on British Airways to/from LHR
lhr.on('vs','vir') # all the flights on Virgin Atlantic to/from LHR
lhr.to('cdg') # all the flight, include those on BA & VS, between LHR and CDG
lhr.to('jfk') # all the flight, include those on BA & VS, between LHR and JFK

lhr.allflights # all the flights data got from the requests above

lhr.filter(aircraft='A320') # returns list of flight numbers that use the a320 got from the requests above
lhr.filter(aircraft='A35K', airline='VS') # returns list of flight numbers that use the a350-1000 on Virgin Atlantic got from the requests above

lhr.get('sfo') # returns list of dicts with flights between LHR and SFO got from the requests above

lhr.flight('BA1') # returns the dict associated with the flight
