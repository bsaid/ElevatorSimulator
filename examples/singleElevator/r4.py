import elevators
class GD: 
    id = "Alfa"
    stav = "ceka"
    cilovePatro = 0
    chyba= 0.005
    real_order=[]
    dictPatra = {0:"P0",1:"P1", 2:"P2",-1:"P-1",3:"P3"}
    Patra_reverse = {"P0":0,"P1":1,"P2":2,"P-1":-1,"P3":3}
    patra_list = ["P1","P0","P-1","P2","P3"]
    cekam=0
    archive=[]
    max=0.00   
    rest = 0.00
    pohyb=0
    DN = "otevrit"

def prechodovaFunkce(e):
    if GD.stav == "jede":
            GD.cekam=0
            GD.DN="zavrit"
            if goToFloor(e, GD.id, GD.cilovePatro):
                GD.stav = "ceka"
                GD.DN="otevrit"
                print("Vytah dorazil do " + str(GD.cilovePatro) + ". patra.")
            if e.numEvents()>0:
                event = e.getNextEvent()
                if event in GD.patra_list:
                    GD.real_order+=[GD.Patra_reverse.get(event)]
                if event=="zpomal":
                    if GD.cilovePatro-GD.rest<e.getPosition("Alfa")<GD.cilovePatro+GD.rest:
                        GD.max=GD.max
                        print("Vytah se pripravuje na zastaveni a snizuje rychlost.")
                    elif GD.max!=0.05:
                        GD.max-=0.05
                if event=="zrychli":
                    if GD.cilovePatro-GD.rest<e.getPosition("Alfa")<GD.cilovePatro+GD.rest:
                        GD.max=GD.max
                        print("Vytah se pripravuje na zastaveni a snizuje rychlost.")
                    elif GD.max!=-0.05:
                        GD.max+=0.05
    elif GD.stav == "ceka":    
        DoorsNow(e)
        if e.getSpeed("Alfa")<0.00:
            e.speedUp("Alfa")
        elif e.getSpeed("Alfa")>0.00:
            e.speedDown("Alfa")
        if GD.DN=="zavrit": 
            CloseAllDoors(e, GD.id)
        elif e.numEvents()==0 or GD.DN=="otevrit":
            OpenADoor(e)
        if GD.cekam>20:
            if e.numEvents()>0 and CloseAllDoors(e, GD.id)==False:
                GD.DN="zavrit"
                CloseAllDoors(e, GD.id)
            if e.numEvents()>0 and CloseAllDoors(e, GD.id)==True:
                event = e.getNextEvent()
                if event in GD.patra_list:
                    GD.real_order+=[GD.Patra_reverse.get(event)]
                    GD.stav="jede"
            else:
                    print("Stisknuto nezname tlacitko.")
    Telemetry(e)
    CheckSpeed(e)
    Optimalise(e,"Alfa")  
    
def Telemetry(e):
    print("krok", e.getTime())
    print("eventu je",e.numEvents(), "pozice",e.getPosition("Alfa"),"max", GD.max,"rest", GD.rest,"DN", GD.DN)
    print("eventy jsou",e.displayQueue(),"stav je",GD.stav,"cekam",GD.cekam,"cilove patro",GD.cilovePatro, "poradi",GD.real_order,"rychlost", e.getSpeed("Alfa"))
    print("***")

def DoorsNow(e):
    pairs = {"P-1":"P-1","P0":"P0","P1":"P1","P2":"P2","P3":"P3","zpomal":"zpomal","zrychli":"zrychli"}
    events = ["P-1","P0","P1","P2","P3"]
    myfloor= None
    for f in e.getDescription("Alfa").get("floors"):
        if f-GD.chyba<=e.getPosition("Alfa")<=f+GD.chyba:
            myfloor=f
    ignore=["zpomal","zrychli", GD.dictPatra.get(myfloor)]
    GD.cekam+=1
    if e.numEvents()>0:
            event = e.getNextEvent()
            if event in events and not event in ignore:
                e.addEvent(pairs.get(event))
            elif event in ignore:
                pass
            else:
                if event=="otevrit":
                    OpenADoor(e)
                    GD.cekam=0
                    GD.DN="otevrit" 
                elif event=="zavrit":
                    CloseAllDoors(e,"Alfa")
                    GD.cekam=0
                    GD.DN="zavrit"      
       

def CheckSpeed(e):
    rest = sum([i/1000 for i in range(0,int(GD.max*100 + 5),5)])
    GD.rest=rest
    if GD.stav=="jede" and e.getSpeed("Alfa")==0.0:
        GD.max=0.05
    if GD.stav=="jede" and GD.cilovePatro-rest<e.getPosition("Alfa")<GD.cilovePatro+rest:
        GD.max=0.05
    elif GD.stav=="ceka":
        pass
        if 0.00-GD.chyba<e.getSpeed("Alfa")>0.00+GD.chyba:
            if e.getSpeed("Alfa")<0.00:
                e.speedUp("Alfa")
            elif e.getSpeed("Alfa")>0.00:
                e.speedDown("Alfa")
    else:
        pass
    if GD.stav=="jede" and abs(e.getSpeed("Alfa")) < GD.max-GD.chyba:
        if GD.cilovePatro<e.getPosition("Alfa"):
            e.speedDown("Alfa")
        elif GD.cilovePatro>e.getPosition("Alfa"):
            e.speedUp("Alfa")
    elif GD.stav=="jede" and abs(e.getSpeed("Alfa")) > GD.max + GD.chyba:
        
        if GD.cilovePatro<e.getPosition("Alfa"):
            e.speedUp("Alfa")
        elif GD.cilovePatro>e.getPosition("Alfa"):
            e.speedDown("Alfa")


def OpenADoor(e):
    floors = e.getDescription("Alfa").get("floors")
    chyba = 0.05
    pos = e.getPosition("Alfa")
    myfloor= None
    for f in floors:
        if f-chyba<=pos<=f+chyba:
            myfloor=f
    if e.getDoorsPosition(GD.id,myfloor)+GD.chyba<1.00:
            e.openDoors(GD.id,myfloor)
    elif e.getDoorsPosition(GD.id,myfloor)-GD.chyba>1.00:
            return True       
    else:
            return False

def goToFloor(e,idVytahu,floorNumber):
    pos = e.getPosition(idVytahu)
    GD.cilovePatro = floorNumber
    if GD.cilovePatro-GD.chyba<pos<GD.cilovePatro+GD.chyba:
        return True
    elif pos<GD.cilovePatro+GD.chyba and GD.stav=="jede" and e.getSpeed("Alfa") < GD.max-GD.chyba:   
        e.speedUp(idVytahu)
        return False
    elif pos>GD.cilovePatro-GD.chyba and GD.stav=="jede" and e.getSpeed("Alfa") > -GD.max + GD.chyba:
        e.speedDown(idVytahu)
        return False  
    elif GD.stav=="ceka" and not GD.cilovePatro-GD.chyba<pos<GD.cilovePatro+GD.chyba:
        return False

def CloseAllDoors(e, idVytahu):
    dict = e.getDescription(idVytahu)
    floors = dict.get("floors")
    doors = dict.get("doors")
    chyba = 0.05
    for f in floors:
        if e.getDoorsPosition(idVytahu,f)-chyba<0.05:
            continue
        elif e.getDoorsPosition(idVytahu,f)-chyba>0.00:
            e.closeDoors(idVytahu,f)
    SumOfDoorsStates = 0
    for i in doors:
        SumOfDoorsStates+=i
    if SumOfDoorsStates<0.01:
        return True
    else:
        return False

def Optimalise(e, idVytahu):
    floors = GD.real_order
    now = e.getPosition(idVytahu)
    new_floors = []
    for f in floors:
        if f not in new_floors:
            new_floors.append(int(f))
    for n in new_floors:
        if new_floors.count(n)>1:
            new_floors.remove(n)
    floors = new_floors   
    new_floors = []
    while not len(floors)==0:
        new_floors.append(min(floors))
        floors.remove(min(floors))
    floors = new_floors 
    if len(GD.real_order)==0:
        first=e.getPosition(idVytahu)
    else:
        first=GD.real_order[0] 
    a=0
    ro_copy=[]
    if first<now:
        for f in floors:
            if int(floors[a])<now:
                ro_copy.insert(0,floors[a])
                a+=1
            elif int(floors[a])>=now:
                ro_copy.append(floors[a])
                a+=1
    elif first>now:
        for f in floors:
            if int(floors[a])>now:
                ro_copy.append(floors[a])
                a+=1
            else:
                a+=1
        for r in ro_copy:
                floors.remove(r)
        floors.reverse()
        for f in floors:
            ro_copy.append(f)
    GD.real_order=ro_copy
    GD.archive+=ro_copy
    for i in GD.archive:
        if GD.archive.count(i)>1:
            GD.archive.remove(i)
    SendOrder(e)

def SendOrder(e):
        if len(GD.real_order)>0:
            GD.cilovePatro=int(GD.real_order[0])
            if goToFloor(e,"Alfa", GD.cilovePatro)!=True and GD.dictPatra.get(GD.cilovePatro) not in e.displayQueue():
                e.addEvent(GD.dictPatra.get(GD.cilovePatro))
            elif goToFloor(e,"Alfa", GD.cilovePatro)==True and GD.cekam>20:
                GD.real_order.remove(GD.real_order[0])
                if len(GD.real_order)>0 and GD.cekam>20:
                    GD.cilovePatro=int(GD.real_order[0])
         
configFileName = 'r4.json'
elevators.runSimulation(configFileName,prechodovaFunkce)