import elevators

class GlobalData:
    alfaDirection = 1
    deltaDirection = 0
    doorsDirection = 1

def processEvents(e):
    while e.numEvents() > 0:
        event = e.getNextEvent()
        if event == 'DeltaUp':
            GlobalData.deltaDirection = 1
        elif event == 'DeltaDown':
            GlobalData.deltaDirection = -1
        elif event == 'DeltaStop':
            GlobalData.deltaDirection = 0
        else:
            print('Unknown event.')

def processAlfa(e):
    if e.getSpeed('Alfa') > 1.9:
        GlobalData.alfaDirection = -1
    if e.getSpeed('Alfa') < -1.9:
        GlobalData.alfaDirection = 1
    if GlobalData.alfaDirection  == 1:
        e.speedUp('Alfa')
    else:
        e.speedDown('Alfa')

def processDelta(e):
    if GlobalData.deltaDirection == 1:
        e.speedUp('Delta')
    elif GlobalData.deltaDirection == -1:
        e.speedDown('Delta')
    else:
        speed = e.getSpeed('Delta')
        if speed > 0:
            e.speedDown('Delta')
        elif speed < 0:
            e.speedUp('Delta')

def processDoors(e):
    if e.getDoorsPosition('Delta', 0) > 0.9:
        GlobalData.doorsDirection = -1
    elif e.getDoorsPosition('Delta', 0) < 0.1:
        GlobalData.doorsDirection = 1

    if GlobalData.doorsDirection == 1:
        e.openDoors('Delta', 0)
    else:
        e.closeDoors('Delta', 0)

def printTelemetry(e):
    print(e.getSpeed('Alfa'), e.getDoorsPosition('Delta', 0))

def elevatorSimulationStep(e):
    processEvents(e)
    processAlfa(e)
    processDelta(e)
    processDoors(e)
    printTelemetry(e)
    
configFileName = 'elevators.json'
elevators.runSimulation(configFileName, elevatorSimulationStep)
