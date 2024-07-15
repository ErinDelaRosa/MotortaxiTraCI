# Documentation link: https://sumo.dlr.de/docs/TraCI/Interfacing_TraCI_from_Python.html
import os
import sys

import traci._vehicle
import traci._vehicletype
if 'SUMO_HOME' in os.environ:
    sys.path.append(sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools')))
else:
    sys.exit("Environment variable 'SUMO_HOME' not found")
import traci

from hmm import model

print(model.transmat_)
print(model.emissionprob_)

left = model.emissionprob_[0][4]
right = model.emissionprob_[0][5]

speedGain = left + right
pushy = model.emissionprob_[0][2] + model.emissionprob_[0][3]

import xml.etree.ElementTree as ET
tree = ET.parse('osm.motortaxi.trips.xml')
root = tree.getroot()

# for x in root:
#     print(x.tag, x.attrib)

print (root[0].attrib["lcSpeedGain"])

root[0].set("lcSpeedGain", str(speedGain))

print (root[0].attrib["lcSpeedGain"])

print (root[0].attrib["lcPushy"])

root[0].set("lcPushy", str(pushy))

print (root[0].attrib["lcPushy"])
# root[0].attrib["lcSpeedGain"] = speedGain

tree.write('output.xml')


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

#motortaxi details
#<vType id="motortaxi" vClass="motorcycle" guiShape="motorcycle" color="red" laneChangeModel="SL2015" 
#    minGap="1.5" lcSublane="1.5" lcAssertive=".1" latAlignment="nice" lcStrategic="0" lcSpeedGain="0.606" 
#    lcKeepRight=".5">
#<trip id="motortaxi_test" type="motortaxi" begin="0.00" end="500" from="27662625#1" to="-704338387"/>

traci.start(sumoCmd)
step = 0
queue = []
# while traci.simulation.getMinExpectedNumber() > 0:
while step <= 5000:
    traci.simulationStep()
    if step <= 100:
        test=traci.vehicle.getIDList()
        for x in test:
            if x[:9] == "motortaxi":
                # print(x)
                traci.vehicle.setLength(x, 2.0)
                traci.vehicle.setWidth(x, 0.7)
                traci.vehicle.setHeight(x, 1.1)
                traci.vehicle.setAccel(x, 6)
                traci.vehicle.setDecel(x, 10)
                traci.vehicle.setEmergencyDecel(x, 10)
                traci.vehicle.setMaxSpeed(x, 60)
                traci.vehicle.setLine(x, 'taxi')
                
    fleet = traci.vehicle.getTaxiFleet(0)
    we = traci.person.getTaxiReservations(1)

    # Logging
    # ongoing = traci.vehicle.getTaxiFleet(2)
    # motortaxi = traci.vehicle.getIDList()
    # for x in motortaxi:
    #     if x[:9] == "motortaxi":
    #         for y in ongoing:
    #             if x == y:
    #                 print(x, " ")
    #                 print("Lateral Lane Pos: ", traci.vehicle.getLateralLanePosition(x))
    #                 print("Lane ID: ",traci.vehicle.getLaneID(x))
    #                 print("Lane Index: ",traci.vehicle.getLaneIndex(x))


    # print(we)
    print("Available ", fleet)
    print(queue)
    if queue and fleet:
        driver = None
        lowestDistance = 0
        # area = None
        winner = None
        # list = []
        # for i in queue:
        #     if traci.person.getRoadID(i.persons[0]) not in list:
        #         list.append(traci.person.getRoadID(i.persons[0]))
        for j in fleet:
            if driver == None:
                driver = j
            for i in queue:
                # if area == None:
                #     area = traci.person.getRoadID(i.persons[0])
                distance = traci.simulation.getDistanceRoad(traci.vehicle.getRoadID(j),traci.vehicle.getLanePosition(j),traci.person.getRoadID(i.persons[0]),traci.person.getLanePosition(i.persons[0]))
                print("From vehicle ", j, " to ", i.persons[0], " Distance: ", distance)

                if lowestDistance == 0:
                    lowestDistance = distance
                    winner = i
                # print(distance, "<= ", lowestDistance)
                if distance < lowestDistance:
                    winner = i
                    driver = j


        traci.vehicle.dispatchTaxi(driver, winner.id)
        queue.remove(winner)
    if we:
        for i in we:
            queue.append(i)


    


    # reservations = traci.person.getTaxiReservations(1)
    # reservation_ids = [r.id for r in reservations]
    # if reservation_ids and fleet:
    #     traci.vehicle.dispatchTaxi(fleet[0], reservation_ids[0]


    # traci.vehicle.setVehicleClass
    #changing the motortaxi vehicle properties 
    #traci.vehicle.setLaneChangeMode("motortaxi_test", 0b010101100101)
    #traci.vehicle.setParameter("motortaxi_test", changeSublane, 1.5)
    #traci.vehicle.setParameter("motortaxi_test", "lcSpeedGain", speedGain)
    
    step += 1 #required
    
    

traci.close()
