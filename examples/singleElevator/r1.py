import elevators
import numpy

ODCHYLKA_SENZORU = 0.005
MAX_SPEED = 0.0
OPEN_TIME = 50
SLOW_SPEED = 0.0 #stejne jako speedStep

class GD:
    ID = "A"
    state = 1
    X = 0
    openTime = 0
    callQueue = []
    FloorWasCalled = [False, False, False, False, False]


def IsDoorOpen(e, floor):
    return e.getDoorsPosition(GD.ID, floor) > 1 - ODCHYLKA_SENZORU

def IsDoorClosed(e, floor):
    return e.getDoorsPosition(GD.ID, floor) < 0 + ODCHYLKA_SENZORU

def Deccelerate(e): #zpomal vytah
    direction = numpy.sign(e.getSpeed(GD.ID))
    if direction == 1:
        e.speedDown(GD.ID)
    else:
        e.speedUp(GD.ID)

def Accelerate(e): #zrychli vytah smerem k X
    direction = numpy.sign(GD.X - e.getPosition(GD.ID))
    if direction == 1:
        e.speedUp(GD.ID)
    else:
        e.speedDown(GD.ID)


def StopDistance(e): #vzdalenost, kterou vytah urazi nez zastavi
    acceleration = e.getConfig()["elevators"][0]["speedStep"]
    speed = abs(e.getSpeed(GD.ID)) + acceleration
    stopTime = speed / acceleration
    return stopTime*(speed/10.0)/2.0

def ShouldSlowDown(e): #jestli vytah musi zacit zpomalovat, aby zastavil v patre X
    stopDistNextFrame = StopDistance(e)
    dist = abs(GD.X - e.getPosition(GD.ID))
    return stopDistNextFrame >= dist 


def ChooseX(e): #"vyber nove X" z mealyho stroje
    GD.X = GD.callQueue[0]
    CheckX(e)

def CheckX(e): #"zkontroluj X" z mealyho stroje
    direction = int(numpy.sign(GD.X - e.getPosition(GD.ID)))
    i = int(min(max(int(e.getPosition(GD.ID)) - direction, 0), 4))
    while i != GD.X and i != -1:
        if numpy.sign(i - e.getPosition(GD.ID)) == direction: #pokud je patro na ceste (stejnym smerem)
            if GD.FloorWasCalled[i]: #vytah chce v patre zastavit
                if abs(GD.X - i) > StopDistance(e) or e.getSpeed(GD.ID) == 0: #vytah stihne zastavit
                    GD.X = i
                    return
        i += direction
    return
   
def RemoveFloorFromCallQueue(): #odeber X z rady zavolani
    GD.FloorWasCalled[GD.X] = False
    i = 0
    while i < len(GD.callQueue):
        if GD.callQueue[i] == GD.X:
            del GD.callQueue[i]
            i -= 1
        i += 1





def prechodovaFunkce(e):
    MAX_SPEED = e.getConfig()["elevators"][0]["maxSpeed"]
    SLOW_SPEED = e.getConfig()["elevators"][0]["speedStep"]
    
    closeDoor = False #jestli byly zmáčknuté tlačítka "otevreni dveri" a "zavreni dveri"
    openDoor = False
    while e.numEvents() > 0:
        event = e.getNextEvent()
        if event == "otevreni dveri":
            openDoor = True
        elif event == "zavreni dveri":
            closeDoor = True
        else:
            floor = int(event[0])
            if floor != GD.X:
                GD.FloorWasCalled[floor] = True
                GD.callQueue.append(floor)
                
    
    if GD.state == 1:
        if closeDoor:
            GD.state = 3
        elif IsDoorOpen (e, GD.X):
            GD.state = 2
            GD.openTime = 0
        else:
            e.openDoors(GD.ID, GD.X)
        return
    
    elif GD.state == 2:
        GD.openTime += 1
        if GD.openTime >= OPEN_TIME:
            GD.state = 3
        elif closeDoor:
            GD.state = 3
        return
    
    elif GD.state == 3:
        if openDoor:
            GD.state = 1
            GD.openTime = 0
        elif IsDoorClosed(e, GD.X):
            GD.state = 4
        else:
            e.closeDoors(GD.ID, GD.X)
        return
    
    elif GD.state == 4:
        if len(GD.callQueue) > 0:
            GD.state = 5
            ChooseX(e)
        elif openDoor:
            GD.state = 1
        return
    
    elif GD.state == 5:
        if ShouldSlowDown(e):
            GD.state = 7
            Deccelerate(e)
        elif e.getSpeed(GD.ID) >= MAX_SPEED - ODCHYLKA_SENZORU:
            GD.state = 6
        else:
            CheckX(e)
            Accelerate(e)
        return
    
    elif GD.state == 6:
        if ShouldSlowDown(e):
            GD.state = 7
            Deccelerate(e)
        else:
            CheckX(e)
        return
    
    elif GD.state == 7:
        if abs(e.getSpeed(GD.ID)) <= SLOW_SPEED + ODCHYLKA_SENZORU:
            GD.state = 8
        else:
            Deccelerate(e)
        return

    elif GD.state == 8:
        if abs(e.getPosition(GD.ID) - GD.X) < ODCHYLKA_SENZORU:
            GD.state = 1
            RemoveFloorFromCallQueue()
            Deccelerate(e)
        return
    
    else:
        print("NEZNAMY STAV")



elevators.runSimulation("r1.json", prechodovaFunkce)
