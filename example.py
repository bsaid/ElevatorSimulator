import elevators

class GlobalData:
        alfaDirection = 1
        deltaDirection = 0
        doorsDirection = 1

def elevatorSimulationStep(e):
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

    if e.getSpeed('Alfa') > 0.9:
        GlobalData.alfaDirection = -1
    if e.getSpeed('Alfa') < -0.9:
        GlobalData.alfaDirection = 1
    if GlobalData.alfaDirection  == 1:
        e.speedUp('Alfa')
    else:
        e.speedDown('Alfa')

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

    if e.getDoorsPosition('Bravo', 2) > 0.9:
        GlobalData.doorsDirection = -1
    elif e.getDoorsPosition('Bravo', 2) < 0.1:
        GlobalData.doorsDirection = 1

    if GlobalData.doorsDirection == 1:
        e.openDoors('Bravo', 2)
    else:
        e.closeDoors('Bravo', 2)
    
    #print(e.getSpeed('Alfa'), e.getDoorsPosition('Bravo', 2))
    #print(e.getDoors('Bravo'))
    
configFileName = 'elevators.json'
elevators.runSimulation(configFileName, elevatorSimulationStep)
