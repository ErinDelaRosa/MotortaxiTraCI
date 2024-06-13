# Documentation link: https://sumo.dlr.de/docs/TraCI/Interfacing_TraCI_from_Python.html
import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools')))
else:
    sys.exit("Environment variable 'SUMO_HOME' not found")
import traci

from hmm import model

sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "osm.sumocfg", "-d", "200"] #replace osm.sumocfg to your cfg file

#taxi part
#def createMotortaxi(time):
#    for i in range(0, 20, 5):
        # declaring the name(unique), route(from demand.route.xml), type of vehicle(declared in demand.route.xml),
        # depart time, and line
#        traci.vehicle.add(f'motortaxi{i}', 'route0', 'motorcycle', depart=f'{time}', line='taxi')
        
#    fleet = traci.vehicle.getTaxiFleet(0) #taxi dispatch and fetch algo
#    reservations = traci.person.getTaxiReservations(0)
#    reservation_ids = [r.id for r in reservations]
#    traci.vehicle.dispatchTaxi(fleet[0], reservation_ids[0])

# Dispatching taxis to cater to people waiting at a bus stop
#def emergencyTaxi(busstopID):
    # getting a Id-list of people waiting at the busstop
#    peopleWaiting = traci.busstop.getPersonIDs(busstopID)
#    pickup = []
    # creating a list with the taxi reservations
#    for i, val in enumerate(peopleWaiting):
#        pickup.append(traci.person.getTaxiReservations(0)[i].id)
    # if one Taxi should pick up all customers, the list needs to clarify the drop off
    # hence the pickup is extended by the order of drop offs
    # pickup.extend(pickup)
#    try:
#        fleet = traci.vehicle.getTaxiFleet(0)
#    except (traci.exceptions.FatalTraCIError):
#        print("No unoccupied taxi-fleet!")
    # dispatching the unoccupied taxis to pick up their designated customers
#    for i, val in enumerate(peopleWaiting):
#        traci.vehicle.dispatchTaxi(fleet[i], pickup[i])

print(model.transmat_)
print(model.emissionprob_)

left = model.emissionprob_[0][4]
right = model.emissionprob_[0][5]

speedGain = left + right
print(left)
print(right)
print(left + right)

#motortaxi details
#<vType id="motortaxi" vClass="motorcycle" guiShape="motorcycle" color="red" laneChangeModel="SL2015" 
#    minGap="1.5" lcSublane="1.5" lcAssertive=".1" latAlignment="nice" lcStrategic="0" lcSpeedGain="0.606" 
#    lcKeepRight=".5">
#<trip id="motortaxi_test" type="motortaxi" begin="0.00" end="500" from="27662625#1" to="-704338387"/>

traci.start(sumoCmd)
step = 0
# while traci.simulation.getMinExpectedNumber() > 0:
while step <= 1000:
    traci.simulationStep()
    
    #changing the motortaxi vehicle properties 
    #traci.vehicle.setLaneChangeMode("motortaxi_test", 0b010101100101)
    #traci.vehicle.setParameter("motortaxi_test", changeSublane, 1.5)
    #traci.vehicle.setParameter("motortaxi_test", "lcSpeedGain", speedGain)
    
    step += 1 #required
    
    

traci.close()
