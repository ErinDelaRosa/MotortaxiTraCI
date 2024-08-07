# Documentation link: https://sumo.dlr.de/docs/TraCI/Interfacing_TraCI_from_Python.html
import os
import sys

import traci._vehicle
import traci._vehicletype

from random import randrange
if 'SUMO_HOME' in os.environ:
    sys.path.append(sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools')))
else:
    sys.exit("Environment variable 'SUMO_HOME' not found")
import traci

sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "osm.sumocfg", "-d", "200"] #replace osm.sumocfg to your cfg file

traci.start(sumoCmd)

def closest_Passenger(queue, fleet):
    skip = False
    driver = None
    lowestDistance = 0
    winner = None

    for j in fleet:
        # motortaxis usually stop when done dropping passengers so resumed
        if traci.vehicle.getStopState(j) > 0:
            traci.vehicle.resume(j)
            skip = True # To skip the dispatch taxi since its being resumed (needs to reset)
            break

        for i in queue:
            # Getting distance of each vehicle to every person in queue
            distance = traci.simulation.getDistanceRoad(traci.vehicle.getRoadID(j),traci.vehicle.getLanePosition(j),traci.person.getRoadID(i.persons[0]),traci.person.getLanePosition(i.persons[0]))
            if lowestDistance == 0: # if its the first iteration
                lowestDistance = distance
                winner = i
                driver = j
            elif distance < lowestDistance: # if current iteration is better 
                lowestDistance = distance
                winner = i
                driver = j


    if not skip:
        # Dispatches a motortaxi to the passenger once shortest distance was calculated
        traci.vehicle.dispatchTaxi(driver, [winner.id, winner.id]) 
        # remove the passenger's reservation detail from the queue and add to logging
    return winner

def convert_To_Motortaxi(vehicle):
    for x in vehicle:
        if x[:9] == "motortaxi":
            traci.vehicle.setLength(x, 2.0)
            traci.vehicle.setWidth(x, 0.7)
            traci.vehicle.setHeight(x, 1.1)
            traci.vehicle.setAccel(x, 6)
            traci.vehicle.setDecel(x, 10)
            traci.vehicle.setEmergencyDecel(x, 10)
            traci.vehicle.setMaxSpeed(x, 60)
            traci.vehicle.setLine(x, 'taxi')

step = 0
queue = [] # queue of passengers to be picked up
logging = [] # tracking passengers who are assigned a motortaxi
wah = 100 # for observation purposes in the terminal
while step <= 10000:
    traci.simulationStep()

    # Changing taxi vehicles to motorcycles
    if step <= 100: # Only check steps 100 and below since all motortaxis were spawned early
        convert_To_Motortaxi(traci.vehicle.getIDList())
                

    # Getting taxi fleet and reservations from people
    fleet = traci.vehicle.getTaxiFleet(0)
    reservations = traci.person.getTaxiReservations(1)

    # Start of assigning motortaxis to passengers
    if queue and fleet:
        winner = closest_Passenger(queue, fleet)
        queue.remove(winner)
        logging.append(winner) # Adding current passengers who has a taxi assigned to them (Logging purposes)





    # Code below is for logging down event of when passengers started waiting, picked up, and dropped off
    # Adds every new reservation found to queue and logs it to a file
    if reservations:
        for i in reservations:
            file = open("logging_" + str(i.persons[0]) + ".txt", "w")
            file.writelines("Started waiting at " + str(step) + "\n")
            queue.append(i)
            file.close()

    logging2 = [] # for removing items from logging


    # logging to check when a passenger has been picked up and dropped off
    for i in logging:
        # if the passenger has not been picked up yet
        go = False 
        with open("logging_" + str(i.persons[0]) + ".txt", "r") as f:
            text = f.readlines()[-1][0:6]
            if text == "Starte":
                go = True

        
        remove=False # boolean for if a passenger has been dropped off
        
        for j in traci.person.getTaxiReservations(8):
            if i.group != j.group and not go: # if its finally not in the "picked up state" from getTaxiReservations(8), means it was dropped off
                remove=True
            elif i.group == j.group and not go: # if its still in, continously update the "Dropped at x"
                remove=False
                with open("logging_" + str(i.persons[0]) + ".txt", "r") as f:
                    data = f.readlines()
                if data[-1][0:6] == "Picked":
                    data.append("Dropped at " + str(step) + "\n")
                else:
                    data[2] = "Dropped at " + str(step) + "\n"
                with open("logging_" + str(i.persons[0]) + ".txt", "w") as f:
                    f.writelines(data)
                break

        if remove: # if true, adds to logging2 (which is the list holding items to be removed from logging)
            logging2.append(i)
            print(step, "  ", i.group)
            print("SOMETHING WAS DROPPED")

        # To check if a passenger was picked up
        for j in traci.person.getTaxiReservations(8):
            if i.group == j.group and go:
                # print(i.group,"  ",step)
                with open("logging_" + str(i.persons[0]) + ".txt", "a") as f:
                    f.writelines("Picked at " + str(step) + "\n")
                # print(step, "  ", i.group)
                # print("SOMETHING WAS PICKED UP")

    # removing item in logging
    for i in logging2:
        logging.remove(i)
    


    step += 1 # goes to next step
traci.close()
