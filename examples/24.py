import elevators

class GD:
    PRECISION = 0.01
    POS_UP = 2
    POS_DOWN = 0
    # POS_DOWN - dole, POS_UP - nahore, 10 - stoji, 11 - jede nahoru, 12 - jede dolu
    posState = 0
    # 0 - zavrene, 1 - oteviraji se, 2 - zaviraji se, 3 - otevrene
    doorState = 1

def stisknutoTlacitko(e: elevators.Simulator, text: str) -> bool:
    if e.numEvents() > 0:
        if e.getNextEvent() == text:
            return True
    return False

def kabinaJeNahore(e: elevators.Simulator):
    return abs(e.getPosition('A') - GD.POS_UP) < GD.PRECISION

def kabinaJeDole(e: elevators.Simulator):
    return abs(e.getPosition('A') - GD.POS_DOWN) < GD.PRECISION

def otevirejDvere(e, id, floor) -> bool:
    if e.getDoorsPosition(id, floor) > 0.95:
        return True
    else:
        e.openDoors(id, floor)
        return False

def zavirejDvere(e, id, floor) -> bool:
    if e.getDoorsPosition(id, floor) < 0.05:
        return True
    else:
        e.closeDoors(id, floor)
        return False

def prechodovaFunkce(e: elevators.Simulator):
    # dole nebo nahore s otevirajicimi se dvermi
    if GD.doorState == 1:
        if otevirejDvere(e, 'A', GD.posState):
            GD.doorState = 3
    # dole s otevrenyi dvermi
    elif GD.posState == GD.POS_DOWN and GD.doorState == 3:
        if stisknutoTlacitko(e, 'nahoru'):
            GD.doorState = 2
    # nahore s otevrenymi dvermi
    elif GD.posState == GD.POS_UP and GD.doorState == 3:
        if stisknutoTlacitko(e, 'dolu'):
            GD.doorState = 2
    # dole se zavirajicimi se dvermi
    elif GD.posState == GD.POS_DOWN and GD.doorState == 2:
        if zavirejDvere(e, 'A', GD.POS_DOWN):
            GD.doorState = 0
            GD.posState = 11
            e.speedUp('A')
    # nahore se zavirajicimi se dvermi
    elif GD.posState == GD.POS_UP and GD.doorState == 2:
        if zavirejDvere(e, 'A', GD.POS_UP):
            GD.doorState = 0
            GD.posState = 12
            e.speedDown('A')
    # jede nahoru
    elif GD.posState == 11:
        if kabinaJeNahore(e):
            e.speedDown('A')
            GD.posState = GD.POS_UP
            GD.doorState = 1
        elif e.numEvents() > 0:
            if e.getNextEvent() == 'stop':
                e.speedDown('A')
                GD.posState = 10
    # jede dolu
    elif GD.posState == 12:
        if kabinaJeDole(e):
            e.speedUp('A')
            GD.posState = GD.POS_DOWN
            GD.doorState = 1
        elif e.numEvents() > 0:
            if e.getNextEvent() == 'stop':
                e.speedUp('A')
                GD.posState = 10
    # stoji nekde
    elif GD.posState == 10:
        if e.numEvents() > 0:
            event = e.getNextEvent()
            if event == 'nahoru':
                e.speedUp('A')
                GD.posState = 11
            elif event == 'dolu':
                e.speedDown('A')
                GD.posState = 12
    else:
        print('Neznamy stav:', GD.posState, GD.doorState)

elevators.runSimulation('elevators.json', prechodovaFunkce)
