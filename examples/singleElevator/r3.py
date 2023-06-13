import elevators

class GlobalData:
    liftDirection = 0
    doorsDirection = 0
    breaks = False
    breaksUp = False
    breaksDown = False
    requests = []
    travel = False
    p3Pressed = False
    p2Pressed = False
    p1Pressed = False
    p0Pressed = False
    doorsPhase = 0
    doorsTime = 0

c = 0.4
k = 0.004


def unpress():
    if GlobalData.liftDirection == 0:
        GlobalData.p0Pressed = False
    if GlobalData.liftDirection == 1:
        GlobalData.p1Pressed = False
    if GlobalData.liftDirection == 2:
        GlobalData.p2Pressed = False
    if GlobalData.liftDirection == 3:
        GlobalData.p3Pressed = False

def line(e,newlvl):
    if GlobalData.travel == False or GlobalData.breaks == True:
        GlobalData.requests.append(newlvl)
    elif e.getSpeed("lift") > 0 and GlobalData.breaks == False:
        if GlobalData.liftDirection > newlvl and newlvl - e.getPosition("lift") > c:
            GlobalData.requests.append(GlobalData.liftDirection)
            GlobalData.liftDirection = newlvl
        else:
            GlobalData.requests.append(newlvl)
    elif e.getSpeed("lift") < 0 and GlobalData.breaks == False:
        if GlobalData.liftDirection < newlvl and newlvl - e.getPosition("lift") < -c:
            GlobalData.requests.append(GlobalData.liftDirection)
            GlobalData.liftDirection = newlvl
        else:
            GlobalData.requests.append(newlvl)

def myKey(num):
    return(abs(GlobalData.liftDirection - num))


def processEvents(e):
    while e.numEvents() > 0:
        event = e.getNextEvent()
        if event == "p3":
            if GlobalData.p3Pressed == True:
                pass
            else:
                line(e,3)
                GlobalData.p3Pressed = True
        elif event == 'p2':
            if GlobalData.p2Pressed == True:
                pass
            else:
                line(e,2)
                GlobalData.p2Pressed = True
        elif event == 'p1':
            if GlobalData.p1Pressed == True:
                pass
            else:
                line(e,1)
                GlobalData.p1Pressed = True
        elif event == 'p0':
            if GlobalData.p0Pressed == True:
                pass
            else:
                line(e,0)
                GlobalData.p0Pressed = True
        elif event == "<I>":
            if GlobalData.travel == False:
                GlobalData.doorsPhase = 1
                GlobalData.doorsTime = 0
        elif event == ">I<":
            if GlobalData.doorsPhase == 2 or GlobalData.doorsPhase == 1:
                GlobalData.doorsPhase = 2
                GlobalData.doorsTime = 35
            pass
        else:
            print('Unknown event.')

def processLift(e):
    if GlobalData.liftDirection == round(e.getPosition("lift"),3) and e.getSpeed("lift") == 0:
        GlobalData.travel = False
        if GlobalData.doorsPhase == 0:
            GlobalData.doorsPhase = 1
            unpress()
            GlobalData.breaksUp = False
            GlobalData.breaksDown = False
            GlobalData.requests.sort(key=myKey,reverse=True)
        elif len(GlobalData.requests) > 0 and GlobalData.doorsPhase == 3:
            GlobalData.doorsPhase = 0
            GlobalData.liftDirection = GlobalData.requests.pop()

    elif (GlobalData.liftDirection > e.getPosition("lift") and GlobalData.breaksDown == False) or GlobalData.breaksUp == True and GlobalData.doorsPhase == 0:
        GlobalData.travel = True
        if (GlobalData.liftDirection - e.getPosition("lift")) > c:
            e.speedUp("lift")
            GlobalData.breaks = False
        elif (GlobalData.liftDirection - e.getPosition("lift")) > k:
            if e.getSpeed("lift") > 0.1:
                e.speedDown("lift")
                GlobalData.breaks = True
                GlobalData.breaksUp = True
        elif e.getSpeed("lift") > 0:
            e.speedDown("lift")
            

    elif (GlobalData.liftDirection < e.getPosition("lift") and GlobalData.breaksUp == False) or GlobalData.breaksDown == True and GlobalData.doorsPhase == 0:
        GlobalData.travel = True
        if (GlobalData.liftDirection - e.getPosition("lift")) < -c:
            e.speedDown("lift")
            GlobalData.breaks = False
        elif (GlobalData.liftDirection - e.getPosition("lift")) < -k:
            if e.getSpeed("lift") < -0.1:
                e.speedUp("lift")
                GlobalData.breaks = True
                GlobalData.breaksDown = True
        elif e.getSpeed("lift") < 0:
            e.speedUp("lift")
        
def processDoor(e):
    if GlobalData.travel == True:
        pass
    elif e.getDoorsPosition("lift",GlobalData.liftDirection) < 0.9 and GlobalData.doorsPhase == 1:
        e.openDoors("lift",GlobalData.liftDirection)
    elif e.getDoorsPosition("lift",GlobalData.liftDirection) >= 0.9 and GlobalData.doorsPhase == 1:
        GlobalData.doorsPhase = 2
    elif  e.getDoorsPosition("lift",GlobalData.liftDirection) > 0.1 and GlobalData.doorsPhase == 2:
        if GlobalData.doorsTime == 40:
            e.closeDoors("lift", GlobalData.liftDirection)
        else:
            GlobalData.doorsTime += 1
    elif e.getDoorsPosition("lift", GlobalData.liftDirection) <= 0.1 and GlobalData.doorsPhase == 2:
        GlobalData.doorsPhase = 3
        GlobalData.doorsTime = 0
    else:
        pass

def elevatorSimulationStep(e):
    processEvents(e)
    processLift(e)
    processDoor(e)
 
configFileName = 'r3.json'
elevators.runSimulation(configFileName, elevatorSimulationStep)
