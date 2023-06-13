import elevators
from r5_goToFloor import goToFloor

class GD:
    id = 'Vytah1'
    stav = 'ceka'
    cilovePatro = 0
    toDo = []

def openDoors(e, idVytahu, floor):
    if e.getDoorsPosition(idVytahu, floor) <1:
        e.openDoors(idVytahu,floor)
        return False
    return True
def closeDoors(e, idVytahu, floor):
    if e.getDoorsPosition(idVytahu, floor) > 0.1:
        e.closeDoors(idVytahu,floor)
        return False
    return True

def stisknutoTlacitko(e, text):
    if len(GD.toDo) > 0:
        if GD.toDo[-1] == text:
            return True
    return False

def prechodovaFunkce(e):
    if e.numEvents() > 0:
        GD.toDo.append(e.getNextEvent())

    if GD.stav == 'jede':
        if goToFloor(e, GD.id, GD.cilovePatro):
            GD.stav = 'oteviram'
            print('Vytah dorazil do ' + str(GD.cilovePatro) + '. patra.')

    elif GD.stav == 'oteviram':
        if stisknutoTlacitko(e, 'zavri'):
            GD.stav = 'zaviram'
            GD.toDo.remove('zavri')
        elif openDoors(e, GD.id, GD.cilovePatro):
            GD.stav = 'ceka'

    elif GD.stav == 'zaviram':
        if stisknutoTlacitko(e, 'otevri'):
            GD.stav = 'oteviram'
            GD.toDo.remove('otevri')
        elif closeDoors(e, GD.id, GD.cilovePatro):
            GD.stav = 'ceka'

    elif GD.stav == 'ceka' and len(GD.toDo) > 0:
        if  stisknutoTlacitko(e, 'otevri'):
            GD.stav = 'oteviram'
            GD.toDo.remove('otevri')
        elif stisknutoTlacitko(e, 'zavri'):
            GD.stav = 'zaviram'
            GD.toDo.remove('zavri')
        elif e.getDoorsPosition(GD.id, GD.cilovePatro) <= 0.1:
            GD.stav = 'zavreno'
        else:
            GD.stav = 'zaviram'

    elif GD.stav == 'zavreno':
        event = GD.toDo[-1]
        GD.toDo.remove(event)
        if event == 'prizemi':
            GD.cilovePatro = 0
            GD.stav = 'jede'
        elif event == '1.patro':
            GD.cilovePatro = 1
            GD.stav = 'jede'
        elif event == '2.patro':
            GD.cilovePatro = 2
            GD.stav = 'jede'
        elif event == '3.patro':
            GD.cilovePatro = 3
            GD.stav = 'jede'
        elif event == 'zavri':
            pass
        else:
            print('Stisknuto nezname tlacitko.')

    elif GD.stav == 'ceka':
       pass

    else:
        print('neznamy stav ', GD.stav)

elevators.runSimulation('r5.json', prechodovaFunkce)
