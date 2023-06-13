import elevators

## Program je rozdělen do několika částí:
## - OBJEKTY, kde jsou definovány classy používané v programu
## - POMOCNE FUNKCE, kde jsou pomocné funkce, které nepoužívají výtahové API
## - FUNKCE  VYTAHU, kde jsou pomocné funkce využívající výtahové API
## - HLAVNI LOOP, která obsahuje přechodovou funkci s ovládáním výtahůROZHODOVACI JEDNOTKA, která zpracovává příchozí příkazy od tlačítek

#OBJEKTY ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class GD:
    dataVytahu = [] #array elevDat (pro kazdy vytah)
    lastUsedIndex = 0 #index naposledy vyuziteho vytahu

    currentPatro = 0 #pozustatek z minuleho cisla jen na ulozeni dat, nechce se mi predelavat trizeni action queue kdyz mi tu staci dat jednu promenou :)

class elevData: #objekt drzici info o vytahu
    def __init__(self, id1, dostupnePatra1):
        self.id = id1 #vytah ke kteremu se tento objekt vztahuje
        self.dostupnePatra = dostupnePatra1 #kam vytah muze jet
        self.pozastavitFunkce = [0, 0] #[0] je bool jestli funkce maji byt pozastaveny, [1] je ktera funkce se ma provadet (otevrit == 0, zavrit == 1)
        self.listOfEvents = []
        self.currentPatro = 0
        self.stav = "ceka"
        self.cilovePatro = 0
        self.startovaciPatro = 0


#POMOCNE FUNKCE ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def IndexToId(index2): #funkce pro ziskani ID vytahu v dataVytahu podle indexu
    return GD.dataVytahu[index2].id
def IdToIndex(id2): #funkce pro ziskani indexu vytahu v dataVytahu podle id
    for i in range(len(GD.dataVytahu)):
        if GD.dataVytahu[i].id == id2:
            return i
def copyArray(array): #kopirovani arrayu pomoci "=" mi nekdy delalo bordel, tak to radsi udelam pojednom :)
    out = []
    for i in array:
        out.append(i)
    return out
def sortEventList(e): #funkce na trizeni listOfEvents vytahu podle vzdalenosti od patra v argumentu
    return abs(GD.currentPatro - e)

#FUNKCE VYTAHU ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def goToFloor(e, idVytahu, floorNumber):
    allDone = True #kdyz vytah neni na konecnem miste, toto se setne na false a dalsi iteration se to bude opakovat
    if(e.getPosition(idVytahu) < floorNumber - 0.01): #pohyb nahoru
        allDone = False 
        if(e.getSpeed(idVytahu) < 0.5): #zrychlovani a zpomalovani vytahu na zacatku a na konci
            e.speedUp(idVytahu)
        if(e.getPosition(idVytahu) > floorNumber - 0.5 and e.getSpeed(idVytahu) > 0.1):
            e.speedDown(idVytahu)
    
    if(e.getPosition(idVytahu) > floorNumber + 0.01): #pohyb dolu
        allDone = False
        if(e.getSpeed(idVytahu) > -0.5): #zrychlovani a zpomalovani vytahu na zacatku a na konci
            e.speedDown(idVytahu)
        if(e.getPosition(idVytahu) < floorNumber + 0.5 and e.getSpeed(idVytahu) < -0.1):
            e.speedUp(idVytahu)
    
    if allDone:
        if(e.getSpeed(idVytahu) > 0): #zastaveni vytahu
            e.speedDown(idVytahu)
        elif(e.getSpeed(idVytahu) < 0):
            e.speedUp(idVytahu)
    
    return allDone

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

# HLAVNI LOOP ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def prechodovaFunkce(e):
    #pocatecni setup na ukladani dat o vytazich, probehne pouze pri 1. iterationu teto funkce
    if e.getTime() == 0:
        for elevID in e.getAllElevators():
            newElevator = elevData(elevID, e.getDescription(elevID)["floors"])
            GD.dataVytahu.append(newElevator) #pro kazdy vytah vytvari objekt elevData, ktery o nem drzi informace

            #taky se na zacatku muzou otevrit dvere, ale vzhledem k tomu, ze vytah se tlacitkem privolava, nedava to moc smysl :D 
            # GD.dataVytahu[GD.lastUsedIndex].pozastavitFunkce[1] = 0
            # GD.dataVytahu[GD.lastUsedIndex].pozastavitFunkce[0] = 1
        

    for vytah in GD.dataVytahu: #projde vsechny vytahy a vykona u nich pozadovane akce (pokud nejake jsou)
        #zavirani a otevirani dveri tlacitkem
        if vytah.stav == "ceka" and vytah.pozastavitFunkce[0] == 1: #pozastavitFunkce je ovladani dveri
            if vytah.pozastavitFunkce[1] == 1:
                if(zavritDvere(e, vytah.currentPatro, vytah.id)):
                    vytah.pozastavitFunkce[0] = 0
            else:
                if(otevritDvere(e, vytah.currentPatro, vytah.id)):
                    vytah.pozastavitFunkce[0] = 0

        #reseni presouvani vytahu
        if vytah.stav == "jede":
            if(vytah.startovaciPatro == vytah.cilovePatro):
                vytah.stav = "ceka"
                print("Vytah ", vytah.id, " uz je v " + str(vytah.cilovePatro) + ". patre.")
            
            #zavirani a otevirani dveri tlacitkem
            if vytah.pozastavitFunkce[0] == 1:
                if(vytah.pozastavitFunkce[1] == 0):
                    if(otevritDvere(e, vytah.currentPatro, vytah.id)):
                        vytah.pozastavitFunkce[0] = 0

                
            #presouvani vytahu
            else:    
                if(zavritDvere(e, vytah.startovaciPatro, vytah.id)):
                    if goToFloor(e, vytah.id, vytah.cilovePatro):
                        if otevritDvere(e, vytah.cilovePatro, vytah.id):
                            vytah.stav = "ceka"
                            print("Vytah ", vytah.id, " dorazil do " + str(vytah.cilovePatro) + ". patra.")

    # ROZHODOVACI JEDNOTKA ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if(e.numEvents() > 0): 
        for vytah in GD.dataVytahu:
            vytah.currentPatro = round(e.getPosition(vytah.id))
            
        
        while e.numEvents() > 0:
            event = e.getNextEvent()
            destinace = 0
            #ovladani dveri tlacitky
            if event == "otevrit dvere (uvnitr kazdeho vytahu)" or event == "zavrit dvere (uvnitr kazdeho vytahu)":
                
                if event == "otevrit dvere (uvnitr kazdeho vytahu)":
                    if GD.dataVytahu[GD.lastUsedIndex].startovaciPatro == GD.dataVytahu[GD.lastUsedIndex].currentPatro or GD.dataVytahu[GD.lastUsedIndex].stav == "ceka":
                        GD.dataVytahu[GD.lastUsedIndex].pozastavitFunkce[1] = 0 #pozastavitFunkce je promena rikajici co maji delat dvere, jak se na ne ma cekat atd
                        GD.dataVytahu[GD.lastUsedIndex].pozastavitFunkce[0] = 1
                    
                elif event == "zavrit dvere (uvnitr kazdeho vytahu)":
                    if GD.dataVytahu[GD.lastUsedIndex].stav == "ceka":
                        GD.dataVytahu[GD.lastUsedIndex].pozastavitFunkce[1] = 1
                        GD.dataVytahu[GD.lastUsedIndex].pozastavitFunkce[0] = 1
                
                continue

            #ovladani pater tlacitky
            elif event == "prizemi (tlacitko k privolani u vsech vytahu v prizemi)":
                destinace = 0
            else:
                asdf = event.split(".")[0]
                if (str.isdigit(asdf[1:]) or len(asdf) == 1): #kdyz pred teckou neni pismeno (aka tlacitko neni uvnitr vytahu), destinace je simply cast pred 1. teckou (a musi se ignorovat 1. character, nebot to muze byt -)
                    destinace = int(asdf)
                else: #kdyz obsahuje pismeno, znamena to, ze na to misto ma jet specificky vytah
                    indexVytahu = IdToIndex(str(asdf[len(asdf)-1]))
                    destinace = int(asdf[:len(asdf)-1]) #vzhledem k tomu, ze id vytahu mam vzdy 1 charakter dlouhy, pro ziskani cisla ordiznu jen posledni character
                    #nebot nemusim hledat optimalni vytah, rovnou ho tam poslu
                    GD.dataVytahu[indexVytahu].listOfEvents.append(destinace)
                    GD.currentPatro = GD.dataVytahu[indexVytahu].cilovePatro
                    GD.dataVytahu[indexVytahu].listOfEvents.sort(key=sortEventList)
                    GD.lastUsedIndex = indexVytahu
                    continue


            #sezene nejvhodnejsi vytah od patra, kde bylo zmacknuto privolavaci tlacitko a priradi mu do q ukol
            temp = [999999999,0] #[0] je vzdalenost nejblizsiho vytahu od pozadovaneho patra, [1] je id toho vytahu (to vysoke cislo je tam jako default value, nemuze tam byt 0 :) )
            for vytah in GD.dataVytahu:
                if not (destinace in vytah.dostupnePatra):
                    continue
                if vytah.stav == "ceka":
                    vzdalenost = abs(destinace - vytah.currentPatro)
                    if vzdalenost < temp[0]:
                        temp[0] = vzdalenost
                        temp[1] = IdToIndex(vytah.id)
                else: #pro pripad ze vytah zrovna nekam jede, ostatni vytahy jsou daleko a cas (nebo spis vzdalenost, ale to je jedno) nez dojede na pozadovane patro je porad nizsi, nez kdyby prijel dalsi vytah
                    vzdalenost = abs(vytah.cilovePatro - vytah.currentPatro) #neni 100% presne, ale to neni potreba (pro 100% presnost by byl potreba dalsi call na api, meh)

                    #zkopiruje si action queue daneho vytahu, prida tam nove patro z tohoto requestu, sortne ji podle vzdalenosti od pozice, kam ted dojede a zjisti jakou drahu vytah ujede nez se dostane do pozadovaneho patra
                    newListOfEvents = copyArray(vytah.listOfEvents)
                    newListOfEvents.append(destinace)
                    GD.currentPatro = vytah.cilovePatro
                    newListOfEvents.sort(key=sortEventList)
                    minulePatro = vytah.cilovePatro
                    for patroVQ in newListOfEvents: #prida vzdalenost, kterou by vytah musel urazit nez by dojel do pozadovaneho patra
                            vzdalenost += abs(minulePatro-patroVQ)
                            if(patroVQ == destinace):
                                break

                    if vzdalenost < temp[0]:
                        temp[0] = vzdalenost
                        temp[1] = IdToIndex(vytah.id)

            #pridani toho privolani vytahu do queue nejoptimalnejsiho vytahu
            GD.dataVytahu[temp[1]].listOfEvents.append(destinace)
            GD.currentPatro = GD.dataVytahu[temp[1]].cilovePatro
            GD.dataVytahu[temp[1]].listOfEvents.sort(key=sortEventList)
            GD.lastUsedIndex = temp[1]
        
        
    #nastavovani patra kam vytah jede
    for vytah in GD.dataVytahu:
        if vytah.stav == "ceka" and len(vytah.listOfEvents) > 0:
            event = vytah.listOfEvents.pop(0)
            vytah.cilovePatro = event
            vytah.stav = "jede"
            vytah.startovaciPatro = round(e.getPosition(vytah.id))
        
elevators.runSimulation('r6.json', prechodovaFunkce)
