import elevators

def elevatorSimulationStep(e):
    if (e.getTime()+10) % 40 < 20:
        e.speedUp('Alfa')
    else:
        e.speedDown('Alfa')

elevators.runSimulation('example4.json', elevatorSimulationStep)
