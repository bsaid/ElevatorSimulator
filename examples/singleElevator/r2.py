import elevators

def goToFloor(e, idVytahu, floorNumber):
    allDone = True
    if(e.getPosition(idVytahu) < floorNumber - 0.01):
        allDone = False
        if(e.getSpeed(idVytahu) < 0.5):
            e.speedUp(idVytahu)
        if(e.getPosition(idVytahu) > floorNumber - 0.5 and e.getSpeed(idVytahu) > 0.1):
            e.speedDown(idVytahu)
    
    if(e.getPosition(idVytahu) > floorNumber + 0.01):
        allDone = False
        if(e.getSpeed(idVytahu) > -0.5):
            e.speedDown(idVytahu)
        if(e.getPosition(idVytahu) < floorNumber + 0.5 and e.getSpeed(idVytahu) < -0.1):
            e.speedUp(idVytahu)
    
    if allDone:
        if(e.getSpeed(idVytahu) > 0):
            e.speedDown(idVytahu)
        elif(e.getSpeed(idVytahu) < 0):
            e.speedUp(idVytahu)
    
    return allDone

class GD:
    pozastavitFunkce = [0, 0] #[0] je bool jestli funkce maji byt pozastaveny, [1] je ktera funkce se ma provadet (otevrit == 0, zavrit == 1)
    listOfEvents = []
    currentPatro = 0
    id = "A"
    stav = "ceka"
    cilovePatro = 0
    startovaciPatro = 0

def sortEventList(e):
    return abs(GD.currentPatro - e)

def otevritDvere(e, floor, vytah):
    if e.getDoorsPosition(vytah, floor) < 0.95:
        e.openDoors(vytah, floor)
        return False
    return True


def zavritDvere(e, floor, vytah):
    if e.getDoorsPosition(vytah, floor) > 0.05:
        e.closeDoors(vytah, floor)
        return False
    return True

def prechodovaFunkce(e):
    #je to trochu spaghetti code, ale funguje to takze v pohode ;)
    #zavirani a otevirani dveri tlacitkem
    if GD.stav == "ceka" and GD.pozastavitFunkce[0] == 1:
        if GD.pozastavitFunkce[1] == 1:
            if(zavritDvere(e, GD.currentPatro, GD.id)):
                GD.pozastavitFunkce[0] = 0
        else:
            if(otevritDvere(e, GD.currentPatro, GD.id)):
                GD.pozastavitFunkce[0] = 0


    if GD.stav == "jede":
        if(GD.startovaciPatro == GD.cilovePatro):
            GD.stav = "ceka"
            print("Vytah uz je v " + str(GD.cilovePatro) + ". patre.")
        
        #zavirani a otevirani dveri tlacitkem
        if GD.pozastavitFunkce[0] == 1:
            if(GD.pozastavitFunkce[1] == 0):
                if(otevritDvere(e, GD.currentPatro, GD.id)):
                    GD.pozastavitFunkce[0] = 0

            
        #rozjezd vytahu
        else:    
            if(zavritDvere(e, GD.startovaciPatro, GD.id)):
                if goToFloor(e, GD.id, GD.cilovePatro):
                    if otevritDvere(e, GD.cilovePatro, GD.id):
                        GD.stav = "ceka"
                        print("Vytah dorazil do " + str(GD.cilovePatro) + ". patra.")
    
    if(e.numEvents() > 0):
        GD.currentPatro = round(e.getPosition(GD.id))
        
        while e.numEvents() > 0:
            event = e.getNextEvent()
            
            #ovladani dveri tlacitky
            if event == "otevrit dvere" or event == "zavrit dvere":
                
                if event == "otevrit dvere":
                    if GD.startovaciPatro == GD.currentPatro or GD.stav == "ceka":
                        GD.pozastavitFunkce[1] = 0
                        GD.pozastavitFunkce[0] = 1
                    
                elif event == "zavrit dvere":
                    if GD.stav == "ceka":
                        GD.pozastavitFunkce[1] = 1
                        GD.pozastavitFunkce[0] = 1
                
                continue

            #ovladani pater tlacitky
            elif event == "prizemi":
                GD.listOfEvents.append(0)
            else:
                GD.listOfEvents.append(int(event.split(".")[0]))
        GD.listOfEvents.sort(key=sortEventList)
        print(GD.listOfEvents)
    
    #nastavovani patra kam vytah jede
    if GD.stav == "ceka" and len(GD.listOfEvents) > 0:
        event = GD.listOfEvents.pop(0)
        GD.cilovePatro = event
        GD.stav = "jede"
        
        GD.startovaciPatro = round(e.getPosition(GD.id))
        
elevators.runSimulation('r2.json', prechodovaFunkce)

