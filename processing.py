from hmm import model # HMM model
import xml.etree.ElementTree as ET

print(model.transmat_)
print(model.emissionprob_)


# Getting lane changing and seepage values from HMM model
speedGain = model.emissionprob_[0][4] + model.emissionprob_[0][5] # assigning the value to the lcspeedgain later on
pushy = model.emissionprob_[0][2] + model.emissionprob_[0][3] # assigning the value to the lcPushy later on

# fixing depart time of each motorcycles
tree = ET.parse('osm.motorcycle.trips.xml')
root = tree.getroot()
value = 0
print(len(root.findall('trip')))
for x in root.findall('trip'):
    x.set("depart", str(value))
    value += 5000/len(root.findall('trip')) # Dividend was originally based on steps
tree.write('motorcycle.xml')

# fixing depart time of each car
tree = ET.parse('osm.passenger.trips.xml')
root = tree.getroot()
value = 0
print(len(root.findall('trip')))
for x in root.findall('trip'):
    x.set("depart", str(value))
    value += 5000/len(root.findall('trip')) # Dividend was originally based on steps 
tree.write('car.xml') # output to car.xml

# assigning the lcpushy and lcspeedgain value to the motortaxis
tree = ET.parse('osm.motortaxi.trips.xml')
root = tree.getroot()
root[0].set("lcSpeedGain", str(speedGain))
root[0].set("lcPushy", str(pushy))
tree.write('motortaxi.xml') # output to motortaxi.xml
