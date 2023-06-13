import elevators


ODCHYLKA_SENZORU = 0.005

def closeAllDoors(e, idVytahu):
    dvereZavrene = True
    poziceDveri = e.getDoors(idVytahu)
    for patro in range(len(poziceDveri)): # pro kazde dvere
        # simulator vraci -1 pro dvere, ktere neexistuji
        if poziceDveri[patro] != -1 and poziceDveri[patro] > ODCHYLKA_SENZORU:
            e.closeDoors(idVytahu, patro)
            dvereZavrene = False
    return dvereZavrene




def setSpeed(e, id, speed):
    elevatorSpeed = e.getSpeed(id)
    if elevatorSpeed > speed + ODCHYLKA_SENZORU:
        e.speedDown(id)
        return False
    elif elevatorSpeed < speed - ODCHYLKA_SENZORU:
        e.speedUp(id)
        return False
    return True



# rychlost kabiny mezi patry
TARGET_SPEED = 0.5
# rychlost priblizovani do patra
SLOW_SPEED = 0.1
# jak daleko od cile zacit brzdit
SLOW_SPEED_DISTANCE = 0.3

# nefunguje pro num = 0, ale tato situace zde nenastane
def signum(num):
    return num / abs(num)

def goToFloor(e, idVytahu, floorNumber):
    # ziskame informace o kabine
    elevatorPosition = e.getPosition(idVytahu)
    elevatorSpeed = e.getSpeed(idVytahu)
    # vytah je ve spravnem patre a zastavil
    if abs(elevatorPosition - floorNumber) < ODCHYLKA_SENZORU and abs(elevatorSpeed) < ODCHYLKA_SENZORU:
        return True
    # vytah dorazil do cile, ale nestoji, takze zastavime kabinu
    elif abs(elevatorPosition - floorNumber) < ODCHYLKA_SENZORU:
        setSpeed(e, idVytahu, 0)
    # vytah se blizi do ciloveho patra a zpomaluje
    elif abs(elevatorPosition - floorNumber) < SLOW_SPEED_DISTANCE:
        direction = signum(floorNumber - elevatorPosition)
        setSpeed(e, idVytahu, SLOW_SPEED * direction)
    # vytah je daleko od ciloveho patra a muze jet maximalni rychlosti
    else:
        direction = signum(floorNumber - elevatorPosition)
        setSpeed(e, idVytahu, TARGET_SPEED * direction)
    return False

# --------


def callElevator(e, floorNumber):
    # ziskame polohy vytahu
    positions = [e.getPosition(f"v{i}") for i in range(3)]
    # vypocet vzdalenosti kazdeho vytahu of patra, kam volame vytah
    distances = [abs(floorNumber - positions[i]) for i in range(3)]
    # urceni nejblizsiho stacionarniho vytahu
    closestElevator = distances.index(min(distances))
    # volani vytahu do pozadovaneho patra
    return goToFloor(e, f"v{closestElevator}", floorNumber)



"""
KOMENTARE K JEDNOTLIVYM CASTEM FUNKCE NEJSOU JASNE

NEFUNGUJE, KDYZ CLOVEK ZMACKNE "VYTAH DO 3/4" (PRIJEDE KLIDNE v1, POKUD JE BLIZE NEZ v0)
"""


def elevatorSimulationStep(e):
    # nacitani eventu
    event = "no event"
    if e.numEvents() > 0:
        event = e.getNextEvent()
    
    # volani libovolneho vytahu
    for i in range(5):
        if event == f"vytah do {i}":
            if callElevator(e, i):
                pass
            else:
                e.addEvent(f"vytah do {i}")

    # volani vytahu do hornich pater
    for i in range(5):
        if event == f"vytah do {i}, horni patra":
            if goToFloor(e, "v0", i):
                pass
            else:
                e.addEvent(f"vytah do {i}, horni patra")
    
    # presun vytahu do hornich pater
    if event == "v0: 3":
        if goToFloor(e, "v0", 3):
            pass
        else: 
            e.addEvent("v0: 3")
    elif event == "v0: 4":
        if goToFloor(e, "v0", 4):
            pass
        else: 
            e.addEvent("v0: 4")
        
    # presun libovolneho vytahu do libovolneho patra
    for elevator_id in range(3):
        for floorNumber in range(3):
            if event == f"v{elevator_id}: {floorNumber}":
                if goToFloor(e, f"v{elevator_id}", floorNumber):
                    pass
                else:
                    e.addEvent(f"v{elevator_id}: {floorNumber}")

    print(event)


configFileName = 'r4.json'
elevators.runSimulation(configFileName, elevatorSimulationStep)