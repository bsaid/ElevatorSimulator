import elevators
class GD: 
    chyba= 0.005 
    Patra_reverse = {"A0":0,"A1":1,"A2":2,"A3":3,"B0":0,"B-1":-1,"B1":1,"B2":2,"G0":0,"G1":1,"G2":2,"P0":0,"P1":1,"P2":2,"P-1":-1,"P3":3}#
    A ={"stav":"ceka","cilovePatro":0,"cekam":0,"max":0,"rest":0.00,"DN":"otevrit","Qup":[],"Qdown":[],"smer":"ceka","floors":[],"dictPatra":{0:"A0",1:"A1", 2:"A2",3:"A3"},"patra_list":["A0","A1","A2","A3"],"order":[]}
    B={"stav":"ceka","cilovePatro":0,"cekam":0,"max":0,"rest":0.00,"DN":"otevrit","Qup":[],"Qdown":[],"smer":"ceka","floors":[],"dictPatra":{0:"B0",1:"B1", 2:"B2",-1:"B-1"},"patra_list":["B0","B1","B2","B-1"],"order":[]}
    G={"stav":"ceka","cilovePatro":0,"cekam":0,"max":0,"rest":0.00,"DN":"otevrit","Qup":[],"Qdown":[],"smer":"ceka","floors":[],"dictPatra":{0:"G0",1:"G1", 2:"G2"},"patra_list":["G0","G1","G2"],"order":[]}
    #dictionaries A,B,G popisují jednotlivé výtahy
    elevs_dict={"Alfa":A,"Beta":B,"Gama":G,"A":"Alfa","B":"Beta","G":"Gama"}
    doors = ["zavrit A","otevrit A","zavrit B","otevrit B","zavrit G","otevrit G"]
    

def prechodovaFunkce(e):    #Hlavní přechodová funkce
    events=e.displayQueue()
    print("krok", e.getTime(),events)
    dict = GD.Patra_reverse
    accep_ev=GD.A.get("patra_list")+GD.B.get("patra_list")+GD.G.get("patra_list")
    posib = []
    A =[e.getPosition("Alfa"),GD.A.get("stav"),GD.A.get("smer"),GD.A.get("order"),"A",[0,1,2,3] ]
    B =[e.getPosition("Beta"),GD.B.get("stav"),GD.B.get("smer"),GD.B.get("order"),"B",[-1,0,1,2]]
    G =[e.getPosition("Gama"),GD.G.get("stav"),GD.G.get("smer"),GD.G.get("order"),"G",[0,1,2]]
    #seznamy A,B,G zestručněně popisují jednotlivé výtahy - jejich pozici, stav, směr, seznam pater, do kterých pojedou, a seznam pater, do kterých jet mohou
    distances=[]
    eles= [A,B,G]
    for event in events:        #Prohledá frontu, zajistí reakce na tlačítka týkající se dveří.
        if event in GD.doors:
            idVytahu = GD.elevs_dict.get(event[len(event)-1])
            myDict = GD.elevs_dict.get(idVytahu)
            if event[0]=="z" and myDict.get("stav")=="ceka":
                myDict["cekam"]=0
                myDict["DN"]="zavrit"
            elif event[0]=="o" and myDict.get("stav")=="ceka":
                myDict["cekam"]=0
                myDict["DN"]="otevrit"
    for i in range(e.numEvents()):  #Způsobí vymazaní událostí, které se týkají dveří, z fronty. Ostatní události do fronty vrátí.
        event = e.getNextEvent()
        id = GD.elevs_dict.get(event[0])
        myDict = GD.elevs_dict.get(id)
        if event[0]=="z" or event[0]=="o" or((event[0]=="A" or event[0]=="B" or event[0]=="G")  and GD.Patra_reverse.get(event)==myDict.get("cilovePatro")):
            pass
        else:
            e.addEvent(event)
    for event in events:        #Zajistí reakci na události vyloženě se týkajících pohybu výtahu v určené šachtě (A1,B2,G0...).
        if event[0]!="P" and event not in GD.doors:
            eles_pairs={"A":GD.A,"B":GD.B,"G":GD.G}
            myDict = eles_pairs.get(event[0])
            myFloors = myDict.get("floors")
            if not GD.Patra_reverse.get(event)+GD.chyba>e.getPosition(GD.elevs_dict.get(event[0]))>GD.Patra_reverse.get(event)-GD.chyba:
                myDict["DN"]="zavrit"
                myFloors.append(GD.Patra_reverse.get(event))
                if CloseAllDoors(e,GD.elevs_dict.get(event[0]))==True:
                    myDict["stav"]="jede" 
            else:
                if event in events:
                    if float(GD.Patra_reverse.get(event))-GD.chyba<e.getPosition(GD.elevs_dict.get(event[0]))<float(GD.Patra_reverse.get(event))+GD.chyba and len(e.displayQueue()) and events.index(event)==0:
                        events.remove(event)
            if event not in e.displayQueue():   
                e.addEvent(event)
                pass  
    events = events 
    for event in events:
        if event=="P3":
            if "A3" not in e.displayQueue():        #Reakce na událost, na kterou může vždy reagovat jen jeden výtah - 
                e.addEvent("A3")
            else:
                pass
        elif event=="P-1":
            if "B-1" not in e.displayQueue():       #jen výtah Alfa jezdí do patra 3 a jen výtah Beta jezdí do patra -1.
                e.addEvent("B-1")
            else:
                pass
        if event[0]=="P" and event!="P3" and event!="P-1":
            p = dict.get(event)
            for l in eles:      #Řádky 76-83 reagují na event začínající písmenem P v případě, že některý výtah už v cílovém patře stojí.
                if l[0]<p+GD.chyba and l[0]>p-GD.chyba and str(l[4]+str(p)) not in e.displayQueue() and str(l[4]+str(p)) in accep_ev:
                    posib=[]
                    posib.append(l[4])
            if len(posib)>0:
                e.getNextEvent()
                e.addEvent("otevrit "+posib[0])
                posib=[]
            for j in eles:      #Následující řádky zjišťují, jestli, v případě, že se žádný výtah nenachází v cílovém patře, tam alespoň některý nemíří (výtah musí být schopný do patra dojet).
                    if ((j[0]<p and j[2]=="nahoru") or (j[0]>p and j[2]=="dolu")) and j not in posib and p in j[5]:
                        posib.append(j) 
            if len(posib)>0:    #Jestli tam míří alespoň jeden vhodný výtah, program přidá do fronty událost spojující dané patro a výtah k němu nejbližší.
                for i in posib:
                    distances.append(abs(i[0]-p))
                c=""
                c=(posib[distances.index(min(distances))][4]+str(dict.get(event)))
                distances=[]
                p=[]
                posib=[]
                if c not in e.displayQueue():
                    e.addEvent(c)
            elif len(posib)==0:     #V opačném případě je do fronty přidána událost spojující cílové patro buď s nejbližším stojícím výtahem,
                for m in eles:      #nebo s tím výtahem, pro který je spojnice jeho současného cílového patra s řešeným cílovým patrem nejkratší.
                    if m[1]=="ceka":
                        distances.append(abs(m[0]-p))
                    elif m[1]=="jede":
                        distances.append(abs(m[3][len(m[3])-1]-p))
                c=(eles[distances.index(min(distances))][4]+str(p))
                e.getNextEvent()
                id = GD.elevs_dict.get(c[0])
                CP = GD.Patra_reverse.get(c)
                if  c in accep_ev and c not in e.displayQueue() and not CP-GD.chyba<e.getPosition(id)<CP+GD.chyba: #Poslední podmínka na řádku má zabránit tomu, že by výtah jel do patra, kde se už nachází (pokud spustím program a zmáčknu P0). 
                    e.addEvent(c)
    #Volání přechodových funkcí pro jednotlivé výtahy.         
    prechodova(e,"Alfa")
    prechodova(e,"Beta")
    prechodova(e,"Gama")
    print("***")
    
def prechodova(e,idVytahu):     #Přechodová funkce pro jednotlivý výtah. Vzhledem k tomu, že funguje stejně, jako fungovala během dřívějších čísel M&Mka, nepovažovala jsem za nutné ji moc popisovat.
    myDict = GD.elevs_dict.get(idVytahu)    
    #Dictionary myDict obsahuje všechny informace (ty, které jsem uznala za potřebné) k danému výtahu. 
    #Definovat na začátku každé funkce myDict mi přišlo výhodnější a úspornější než zavést do classu GD 13 proměnných pro každý výtah.
    if myDict.get("stav") == "jede":
            myDict["cekam"]=0
            myDict["DN"]="zavrit"
            if goToFloor(e, idVytahu, myDict.get("cilovePatro"))==True:
                myDict["stav"] = "ceka"
                myDict["DN"]="otevrit"
            if e.numEvents()>0:
                event = e.getNextEvent()
                if event in GD.doors:
                    e.addEvent(event)
                elif event in myDict.get("patra_list"):
                    myDict["floors"]+=[GD.Patra_reverse.get(event)]
                elif event[0]!="P" and event not in e.displayQueue() and event not in GD.doors:
                    e.addEvent(event)
    elif myDict.get("stav") == "ceka":    
        myDict["cekam"]+=1
        count =0
        evs=e.displayQueue()
        for i in evs:
                if idVytahu[0]==i[0]:
                    count+=1   
        if e.getSpeed(idVytahu)<0.00:
            e.speedUp(idVytahu)
        elif e.getSpeed(idVytahu)>0.00:
            e.speedDown(idVytahu)
        if myDict.get("DN")=="zavrit": 
            CloseAllDoors(e, idVytahu)
        elif myDict.get("DN")=="otevrit":
            OpenADoor(e,idVytahu)
        if myDict.get("cekam")>20: 
            if count>0 and myDict.get("DN")=="zavrit": 
                myDict["DN"]="zavrit"
                CloseAllDoors(e, idVytahu)
            if count>0 and CloseAllDoors(e, idVytahu)==True: 
                event = e.getNextEvent()
                if event in GD.doors:
                    e.addEvent(event)
                elif event in myDict.get("patra_list"):
                    myDict["floors"]+=[GD.Patra_reverse.get(event)]
                    myDict["stav"]="jede"
                elif event[0]!="P" and event not in e.displayQueue() and event not in GD.doors and not float(GD.Patra_reverse.get(event))-GD.chyba<e.getPosition(idVytahu)<float(GD.Patra_reverse.get(event))+GD.chyba:
                    e.addEvent(event)
    CheckSpeed(e,idVytahu)
    Optimalise(e,idVytahu)
    Telemetry(e,idVytahu)

    
def Telemetry(e,idVytahu):
    myDict = GD.elevs_dict.get(idVytahu)
    print(idVytahu,myDict.get("order"),myDict.get("DN"))
    
 

def CheckSpeed(e,idVytahu):     #Funkce se stará, aby výtah nepřekročil svou maximální rychlost, kterou jsem nastavila na 0.3. Tlačítka "zrychlit" a "zpomalit" jsem zrušila.
    myDict = GD.elevs_dict.get(idVytahu)
    rest = sum([i/1000 for i in range(0,int(myDict["max"]*100 + 5),5)])
    myDict["rest"]=rest
    if myDict.get("stav")=="jede"  and (abs(e.getSpeed(idVytahu)==0.00) or abs(e.getSpeed(idVytahu))==0.05) and (myDict.get("cilovePatro")+rest<e.getPosition(idVytahu) or e.getPosition(idVytahu)<myDict.get("cilovePatro")-rest):
        myDict["max"]=0.3
    if myDict.get("stav")=="jede" and myDict.get("cilovePatro")-rest<e.getPosition(idVytahu)<myDict.get("cilovePatro")+rest:
        myDict["max"]=0.05
    elif myDict.get("stav")=="ceka":
        pass
        if 0.00-GD.chyba<e.getSpeed(idVytahu)>0.00+GD.chyba:
            if e.getSpeed(idVytahu)<0.00:
                e.speedUp(idVytahu)
            elif e.getSpeed(idVytahu)>0.00:
                e.speedDown(idVytahu)
    else:
        pass
    if myDict.get("stav")=="jede" and abs(e.getSpeed(idVytahu)) < myDict.get("max")-GD.chyba:
        if myDict.get("cilovePatro")<e.getPosition(idVytahu):
            e.speedDown(idVytahu)
        elif myDict.get("cilovePatro")>e.getPosition(idVytahu):
            e.speedUp(idVytahu)
    elif myDict.get("stav")=="jede" and abs(e.getSpeed(idVytahu)) > myDict.get("max") + GD.chyba:
        if myDict.get("cilovePatro")<e.getPosition(idVytahu):
            e.speedUp(idVytahu)
        elif myDict.get("cilovePatro")>e.getPosition(idVytahu):
            e.speedDown(idVytahu)


def OpenADoor(e,idVytahu):      #Zajišťuje otevírání dveří v tom patře, kde výtah zrovna stojí.
    floors = e.getDescription(idVytahu).get("floors")
    chyba = 0.05
    pos = e.getPosition(idVytahu)
    myfloor= None
    for f in floors:
        if f-chyba<=pos<=f+chyba:
            myfloor=f
    if e.getDoorsPosition(idVytahu,myfloor)+GD.chyba<1.00:
            e.openDoors(idVytahu,myfloor)
    elif e.getDoorsPosition(idVytahu,myfloor)-GD.chyba>1.00:
            return True       
    else:
            return False

def goToFloor(e,idVytahu,floorNumber):  #Zajišťuje, že se výtah rozjede do zadaného patra.
    myDict = GD.elevs_dict.get(idVytahu)
    pos = e.getPosition(idVytahu)
    myDict["cilovePatro"] = floorNumber
    if myDict.get("cilovePatro")-GD.chyba<pos<myDict.get("cilovePatro")+GD.chyba:
        return True
    elif pos<myDict.get("cilovePatro")+GD.chyba and myDict.get("stav")=="jede" and e.getSpeed(idVytahu) < myDict.get("max")-GD.chyba:   
        e.speedUp(idVytahu)
        return False
    elif pos>myDict.get("cilovePatro")-GD.chyba and myDict.get("stav")=="jede" and e.getSpeed(idVytahu) > -myDict.get("max") + GD.chyba:
        e.speedDown(idVytahu)
        return False  
    elif myDict.get("stav")=="ceka" and not myDict.get("cilovePatro")-GD.chyba<pos<myDict.get("cilovePatro")+GD.chyba:
        return False

def CloseAllDoors(e, idVytahu): #Zajišťuje zavírání dveří výtahu.
    myDict = GD.elevs_dict.get(idVytahu)
    dict = e.getDescription(idVytahu)
    floors = dict.get("floors")
    doors = dict.get("doors")
    for f in floors:
        if e.getDoorsPosition(idVytahu,f)-GD.chyba<0.05:
            continue
        elif e.getDoorsPosition(idVytahu,f)-GD.chyba>0.00 and myDict.get("DN")=="zavrit":
            e.closeDoors(idVytahu,f)
    SumOfDoorsStates = 0
    for i in doors:
        SumOfDoorsStates+=i
    if SumOfDoorsStates<0.01:
        return True
    else:
        return False

def Optimalise(e, idVytahu):    #Optimalizace pater v rámci jednoho výtahu (jedné šachty). 
    now = e.getPosition(idVytahu)
    myDict = GD.elevs_dict.get(idVytahu)
    dictPatra = myDict.get("dictPatra")
    for i in myDict.get("floors"):  #Odstraňuje z položky floors patra, která se tam vyskytují vícekrát, a současné patro, je-li zastoupeno. 
        while myDict.get("floors").count(i)>1:
            myDict["floors"].remove(i)
        if not(i-GD.chyba<now<i+GD.chyba) and i>now+GD.chyba and i>now-GD.chyba and i not in myDict.get("Qup"): #Zbytek pater je rozdělen do fronty pro jízdu nahoru a pro jízdu dolů.
            myDict["Qup"].append(i)
        elif not(i-GD.chyba<now<i+GD.chyba) and i<now+GD.chyba and i<now-GD.chyba and i not in myDict.get("Qdown"):
            myDict["Qdown"].append(i)
        elif i-2*GD.chyba<e.getPosition(idVytahu)<i+GD.chyba:
            myDict["floors"].remove(i)
    myDict["Qup"]=sorted(myDict["Qup"])
    myDict["Qdown"]=sorted(myDict["Qdown"])[::-1]
    if len(myDict.get("Qup"))==0 and len(myDict.get("Qdown"))==0:   #Následující řádky určují směr, jakým se výtah vydá. Vychází ale z předpokladu, že tlačítka nebyla stisknuta během jednoho kroku (tento předpoklad mi připadal adekvátní).
        myDict["smer"]="ceka"
    elif len(myDict.get("Qup"))>0 and len(myDict.get("Qdown"))==0:  
        myDict["smer"]="nahoru"
    elif len(myDict.get("Qup"))==0 and len(myDict.get("Qdown"))>0:  
        myDict["smer"]="dolu"
    if myDict.get("smer")=="nahoru":
        myDict["cilovePatro"]=myDict.get("Qup")[0]
        myDict["order"]=myDict.get("Qup")+myDict.get("Qdown")
    elif myDict.get("smer")=="dolu":
        myDict["cilovePatro"]=myDict.get("Qdown")[0]
        myDict["order"]=myDict.get("Qdown")+myDict.get("Qup")
    if int(len(myDict.get("Qup"))+len(myDict.get("Qdown")))>0:
        if goToFloor(e,idVytahu, myDict.get("cilovePatro"))!=True and dictPatra.get(myDict.get("cilovePatro")) not in e.displayQueue():
            e.addEvent(dictPatra.get(myDict.get("cilovePatro")))
        elif goToFloor(e,idVytahu, myDict.get("cilovePatro"))==True and myDict.get("cekam")>20: #Následující řádky obstarávají odstraňování cílového patra z fronty poté, co do něj výtah přijede.
            if myDict.get("cilovePatro") in myDict.get("floors"):
                myDict["floors"].remove(myDict.get("cilovePatro"))
            if myDict.get("smer")=="nahoru" and len(myDict.get("Qup"))>0:
                myDict.get("Qup").remove(myDict.get("Qup")[0])
                if len(myDict.get("Qup"))>0:
                    myDict["cilovePatro"]=myDict.get("Qup")[0]
            elif myDict.get("smer")=="dolu" and len(myDict.get("Qdown"))>0:
                myDict.get("Qdown").remove(myDict.get("Qdown")[0])
                if len(myDict.get("Qdown"))>0:
                    myDict["cilovePatro"]=myDict.get("Qdown")[0]
         
configFileName = 'r2.json'
elevators.runSimulation(configFileName,prechodovaFunkce)
