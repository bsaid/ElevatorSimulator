import elevators

class GD:
    PRECISION = 0.01
    WAITING_TIMEOUT = 20
    POS_UP = 2
    POS_DOWN = 0
    waitingFrom = 0
    actState = 0

def zacniCekat(e):
    GD.waitingFrom = e.getTime()

def casUplynul(e):
    return e.getTime() - GD.waitingFrom > GD.WAITING_TIMEOUT

def jeNahore(e):
    return abs(e.getPosition('A') - GD.POS_UP) < GD.PRECISION

def jeDole(e):
    return abs(e.getPosition('A') - GD.POS_DOWN) < GD.PRECISION

def prechodovaFunkce(e):
    if GD.actState == 0:
        if casUplynul(e):
            e.speedUp('A')
            GD.actState = 1
    elif GD.actState == 1:
        if jeNahore(e):
            e.speedDown('A')
            zacniCekat(e)
            GD.actState = 2
    elif GD.actState == 2:
        if casUplynul(e):
            e.speedDown('A')
            GD.actState = 3
    elif GD.actState == 3:
        if jeDole(e):
            e.speedUp('A')
            zacniCekat(e)
            GD.actState = 0

elevators.runSimulation('elevators.json', prechodovaFunkce)
