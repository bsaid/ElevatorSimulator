## This example was created by student.

import elevators
from example_oneCompleteElevator_goToFloor import goToFloor

class GD:
    id = 'Elevator1'
    state = 'waiting'
    targetFloor = 0
    toDo = []

def openDoors(e, eleId, floor):
    if e.getDoorsPosition(eleId, floor) <1:
        e.openDoors(eleId,floor)
        return False
    return True

def closeDoors(e, eleId, floor):
    if e.getDoorsPosition(eleId, floor) > 0.1:
        e.closeDoors(eleId,floor)
        return False
    return True

def buttonPressed(e, text):
    if len(GD.toDo) > 0:
        if GD.toDo[-1] == text:
            return True
    return False

def transitionFunction(e):
    if e.numEvents() > 0:
        GD.toDo.append(e.getNextEvent())

    if GD.state == 'going':
        if goToFloor(e, GD.id, GD.targetFloor):
            GD.state = 'opening'
            print('Elevator arrived to floor number ' + str(GD.targetFloor) + '.')

    elif GD.state == 'opening':
        if buttonPressed(e, 'Close doors'):
            GD.state = 'closing'
            GD.toDo.remove('Close doors')
        elif openDoors(e, GD.id, GD.targetFloor):
            GD.state = 'waiting'

    elif GD.state == 'closing':
        if buttonPressed(e, 'Open doors'):
            GD.state = 'opening'
            GD.toDo.remove('Open doors')
        elif closeDoors(e, GD.id, GD.targetFloor):
            GD.state = 'waiting'

    elif GD.state == 'waiting' and len(GD.toDo) > 0:
        if  buttonPressed(e, 'Open doors'):
            GD.state = 'opening'
            GD.toDo.remove('Open doors')
        elif buttonPressed(e, 'Close doors'):
            GD.state = 'closing'
            GD.toDo.remove('Close doors')
        elif e.getDoorsPosition(GD.id, GD.targetFloor) <= 0.1:
            GD.state = 'closed'
        else:
            GD.state = 'closing'

    elif GD.state == 'closed':
        event = GD.toDo[-1]
        GD.toDo.remove(event)
        if event == 'Ground':
            GD.targetFloor = 0
            GD.state = 'going'
        elif event == '1st floor':
            GD.targetFloor = 1
            GD.state = 'going'
        elif event == '2nd floor':
            GD.targetFloor = 2
            GD.state = 'going'
        elif event == '3rd floor':
            GD.targetFloor = 3
            GD.state = 'going'
        elif event == 'Close doors':
            pass
        else:
            print('Unknown button pressed.')

    elif GD.state == 'waiting':
       pass

    else:
        print('Unknown state: ', GD.state)

elevators.runSimulation('example_oneCompleteElevator.json', transitionFunction)
