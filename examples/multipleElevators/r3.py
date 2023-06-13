import elevators




class GD: #Global Data
                
                cilovePatroA = -1 # cilove patro pro vytah Alfa
                cilovePatroB = -1 # cilove patro pro vytah Beta
                cilovePatroG = -1 # cilove patro pro vytah Gama
                

def AlfaDoPatra (e,cilovePatroA):

    #print ('AlfaDoPatra')
    #print ('cilovePatroA = ',cilovePatroA)
    #print ('pozice Alfa = ', e.getPosition('Alfa'))
    #print ('Dvere Alfa = ',e.getDoors ('Alfa'))

    Dvere0A = e.getDoorsPosition('Alfa',0)
    Dvere1A = e.getDoorsPosition('Alfa',1)
    Dvere2A = e.getDoorsPosition('Alfa',2)

    
    if (((Dvere0A <= 0.05 and Dvere0A >= -0.05) and (Dvere1A <= 0.05 and Dvere1A >= -0.05) and (Dvere2A <= 0.05 and Dvere2A >= -0.05)) or (e.getPosition('Alfa') >= cilovePatroA-0.05 and e.getPosition('Alfa') <= cilovePatroA+0.05)):
    #pokud jsou vsechny dvere zavrene (+- odchylka), nebo se nachazim v potrebnem patre (+- odchylka).
            
        if (e.getPosition('Alfa') >= GD.cilovePatroA-0.05 and e.getPosition('Alfa') <= GD.cilovePatroA+0.05):# pokud jsi v cilovem patre (+- odchylka)
                                
            if (e.getSpeed('Alfa') > 0): # jedes-li nahoru
                                
                e.speedDown('Alfa')# brzdi!

            elif (e.getSpeed('Alfa') < 0): # jedes-li dolu 
                                        
                    e.speedUp('Alfa') # brzdi!

            elif (e.getSpeed('Alfa') == 0): # zabrzdeno?

                if (e.getDoorsPosition('Alfa',cilovePatroA) < 1): # pokud jsou dvere v cilovem patre zavrene
                    
                    e.openDoors ('Alfa',cilovePatroA) # otevri je

        elif (GD.cilovePatroA > e.getPosition ('Alfa')): # pokud jsi pod cilovym patrem
            e.speedUp('Alfa') # zrychli

        elif (GD.cilovePatroA < e.getPosition ('Alfa')): # pokud jsi nad cilovym patrem
                e.speedDown('Alfa') # zpomal

    else: 
        
        if (Dvere0A > 0.05): # pokud nejsou dvere v prizemi zavrene (+- odchylka)
            e.closeDoors ('Alfa',0)

        if (Dvere1A > 0.05):# pokud nejsou dvere v prvnim patre zavrene (+- odchylka)
            e.closeDoors ('Alfa',1)
            
        if (Dvere2A > 0.05):# pokud nejsou dvere v druhem patre zavrene (+- odchylka)
            e.closeDoors ('Alfa',2)

def BetaDoPatra (e,cilovePatroB):

    #print ('BetaDoPatra')
    #print ('cilovePatroB = ',cilovePatroB)
    #print ('pozice Beta = ', e.getPosition('Beta'))
    #print ('Dvere Beta = ',e.getDoors ('Beta'))

    Dvere0B = e.getDoorsPosition('Beta',0)
    Dvere1B = e.getDoorsPosition('Beta',1)
    Dvere2B = e.getDoorsPosition('Beta',2)

    
    if (((Dvere0B <= 0.05 and Dvere0B >= -0.05) and (Dvere1B <= 0.05 and Dvere1B >= -0.05) and (Dvere2B <= 0.05 and Dvere2B >= -0.05)) or (e.getPosition('Beta') >= cilovePatroB-0.05 and e.getPosition('Beta') <= cilovePatroB+0.05)):
    #pokud jsou vsechny dvere zavrene (+- odchylka), nebo se nachazim v potrebnem patre (+- odchylka).
            
        if (e.getPosition('Beta') >= GD.cilovePatroB-0.05 and e.getPosition('Beta') <= GD.cilovePatroB+0.05):# pokud jsi v cilovem patre (+- odchylka)
                                
            if (e.getSpeed('Beta') > 0): # jedes-li nahoru
                                
                e.speedDown('Beta')# brzdi!

            elif (e.getSpeed('Beta') < 0): # jedes-li dolu 
                                        
                    e.speedUp('Beta') # brzdi!

            elif (e.getSpeed('Beta') == 0): # zabrzdeno?

                if (e.getDoorsPosition('Beta',cilovePatroB) < 1): # pokud jsou dvere v cilovem patre zavrene
                    
                    e.openDoors ('Beta',cilovePatroB) # otevri je

        elif (GD.cilovePatroB > e.getPosition ('Beta')): # pokud jsi pod cilovym patrem
            e.speedUp('Beta') # zrychli

        elif (GD.cilovePatroB < e.getPosition ('Beta')): # pokud jsi nad cilovym patrem
                e.speedDown('Beta') # zpomal

    else:
        
        if (Dvere0B > 0.05):# pokud nejsou dvere v prizemi zavrene (+- odchylka)
            e.closeDoors ('Beta',0)

        if (Dvere1B > 0.05):# pokud nejsou dvere v prvnim patre zavrene (+- odchylka)
            e.closeDoors ('Beta',1)
            
        if (Dvere2B > 0.05):# pokud nejsou dvere v druhem patre zavrene (+- odchylka)
            e.closeDoors ('Beta',2)
            
def GamaDoPatra (e,cilovePatroG):

    #print ('GamaDoPatra')
    #print ('cilovePatroG = ',cilovePatroG)
    #print ('pozice Gama = ', e.getPosition('Gama'))
    #print ('Dvere Gama = ',e.getDoors ('Gama'))

    Dvere0G = e.getDoorsPosition('Gama',0)
    Dvere1G = e.getDoorsPosition('Gama',1)
    Dvere2G = e.getDoorsPosition('Gama',2)
    Dvere3G = e.getDoorsPosition('Gama',3)
    Dvere4G = e.getDoorsPosition('Gama',4)

    
    if (((Dvere0G <= 0.05 and Dvere0G >= -0.05) and (Dvere1G <= 0.05 and Dvere1G >= -0.05) and (Dvere2G <= 0.05 and Dvere2G >= -0.05) and(Dvere3G <= 0.05 and Dvere3G >= -0.05) and (Dvere4G <= 0.05 and Dvere4G >= -0.05)) or (e.getPosition('Gama') >= cilovePatroG-0.05 and e.getPosition('Gama') <= cilovePatroG+0.05)):
    #pokud jsou vsechny dvere zavrene (+- odchylka), nebo se nachazim v potrebnem patre (+- odchylka).
            
        if (e.getPosition('Gama') >= GD.cilovePatroG-0.05 and e.getPosition('Gama') <= GD.cilovePatroG+0.05):# pokud jsi v cilovem patre (+- odchylka)
                                
            if (e.getSpeed('Gama') > 0): # jedes-li nahoru
                                
                e.speedDown('Gama')# brzdi!

            elif (e.getSpeed('Gama') < 0): # jedes-li dolu 
                                        
                    e.speedUp('Gama') # brzdi!

            elif (e.getSpeed('Gama') == 0): # zabrzdeno?

                if (e.getDoorsPosition('Gama',cilovePatroG) < 1): # pokud jsou dvere v cilovem patre zavrene
                    
                    e.openDoors ('Gama',cilovePatroG) # otevri je

        elif (GD.cilovePatroG > e.getPosition ('Gama')): # pokud jsi pod cilovym patrem
            e.speedUp('Gama') # zrychli

        elif (GD.cilovePatroG < e.getPosition ('Gama')): # pokud jsi nad cilovym patrem
                e.speedDown('Gama') # zpomal

    else:
        
        if (Dvere0G > 0.05):# pokud nejsou dvere v prizemi zavrene (+- odchylka)
            e.closeDoors ('Gama',0)

        if (Dvere1G > 0.05):# pokud nejsou dvere v prvnim patre zavrene (+- odchylka)
            e.closeDoors ('Gama',1)
            
        if (Dvere2G > 0.05):# pokud nejsou dvere v druhem patre zavrene (+- odchylka)
            e.closeDoors ('Gama',2)
                        
        if (Dvere3G > 0.05):# pokud nejsou dvere v tretim patre zavrene (+- odchylka)
            e.closeDoors ('Gama',3)
                        
        if (Dvere4G > 0.05):
            e.closeDoors ('Gama',4)


def elevatorSimulationStep(e):
        
        while (e.numEvents() > 0):
                event = e.getNextEvent()
                
                if (event == 'AlfaDo0'):                    
                    GD.cilovePatroA = 0
                    #print ('event')
                    AlfaDoPatra(e,GD.cilovePatroA)

                elif (event == 'AlfaDo1'):                    
                    GD.cilovePatroA = 1
                   #print ('event')
                    AlfaDoPatra(e,GD.cilovePatroA)


                elif (event == 'AlfaDo2'):                    
                    GD.cilovePatroA = 2
                    #print ('event')
                    AlfaDoPatra(e,GD.cilovePatroA)
                        
                elif (event == 'BetaDo0'):                    
                    GD.cilovePatroB = 0
                    #print ('event')
                    BetaDoPatra(e,GD.cilovePatroB)

                elif (event == 'BetaDo1'):                    
                    GD.cilovePatroB = 1
                    #print ('event')
                    BetaDoPatra(e,GD.cilovePatroB)
                    
                elif (event == 'BetaDo2'):                    
                    GD.cilovePatroB = 2
                    #print ('event')
                    BetaDoPatra(e,GD.cilovePatroB)
                                            
                elif (event == 'GamaDo0'):                    
                    GD.cilovePatroG = 0
                    #print ('event')
                    GamaDoPatra(e,GD.cilovePatroG)
                        
                elif (event == 'GamaDo1'):                    
                    GD.cilovePatroG = 1
                    #print ('event')
                    GamaDoPatra(e,GD.cilovePatroG)
                        
                elif (event == 'GamaDo2'):                    
                    GD.cilovePatroG = 2
                    #print ('event')
                    GamaDoPatra(e,GD.cilovePatroG)

                elif (event == 'GamaDo3'):                    
                    GD.cilovePatroG = 3
                    #print ('event')
                    GamaDoPatra(e,GD.cilovePatroG)

                elif (event == 'GamaDo4'):                    
                    GD.cilovePatroG = 4
                    #print ('event')
                    GamaDoPatra(e,GD.cilovePatroG)

                elif (event == 'DoPatra0'):
                    #print ('event')
                    poziceA = e.getPosition('Alfa')
                    poziceB = e.getPosition('Beta')
                    poziceG = e.getPosition('Gama')
                    #print ('poziceA = ', poziceA)
                    #print ('poziceB = ', poziceB)
                    #print ('poziceG = ', poziceG)
                    vzdalenostOdCilovehoPatraA = round (abs(poziceA)) # vzdalenost vytahu Alfa od ciloveho patra (zaokrouhlena)
                    vzdalenostOdCilovehoPatraB = round (abs(poziceB)) # vzdalenost vytahu Beta od ciloveho patra (zaokrouhlena)
                    vzdalenostOdCilovehoPatraG = round (abs(poziceG)) # vzdalenost vytahu Gama od ciloveho patra (zaokrouhlena)
                    #print ('vzdalenostOdCilovehoPatraA = ', vzdalenostOdCilovehoPatraA)
                    #print ('vzdalenostOdCilovehoPatraB = ', vzdalenostOdCilovehoPatraB)
                    #print ('vzdalenostOdCilovehoPatraG = ', vzdalenostOdCilovehoPatraG)

                    if ((poziceA == 0) or ((vzdalenostOdCilovehoPatraA <= vzdalenostOdCilovehoPatraB) and (vzdalenostOdCilovehoPatraA <= vzdalenostOdCilovehoPatraG) and (e.getSpeed('Alfa') == 0))):
                        # pokud je vytah Alfa v cilovem patre, nebo je mu nejblize a nejede nikam jinam
                        GD.cilovePatroA = 0
                    
                    elif ((poziceB == 0) or ((vzdalenostOdCilovehoPatraB <= vzdalenostOdCilovehoPatraA) and (vzdalenostOdCilovehoPatraB <= vzdalenostOdCilovehoPatraG) and (e.getSpeed('Beta') == 0))):
                        # pokud je vytah Beta v cilovem patre, nebo je mu nejblize a nejede nikam jinam
                        GD.cilovePatroB = 0

                    elif ((poziceG == 0) or ((vzdalenostOdCilovehoPatraG <= vzdalenostOdCilovehoPatraA) and (vzdalenostOdCilovehoPatraG <= vzdalenostOdCilovehoPatraB) and (e.getSpeed('Gama') == 0))):
                        # pokud je vytah Beta v cilovem patre, nebo je mu nejblize a nejede nikam jinam
                        GD.cilovePatroG = 0

                    

                elif (event == 'DoPatra1'):
                    #print ('event')
                    poziceA = e.getPosition('Alfa')
                    poziceB = e.getPosition('Beta')
                    poziceG = e.getPosition('Gama')
                    #print ('poziceA = ', poziceA)
                    #print ('poziceB = ', poziceB)
                    #print ('poziceG = ', poziceG)
                    vzdalenostOdCilovehoPatraA = round (abs(poziceA - 1)) # vzdalenost vytahu Alfa od ciloveho patra (zaokrouhlena)
                    vzdalenostOdCilovehoPatraB = round (abs(poziceB - 1)) # vzdalenost vytahu Beta od ciloveho patra (zaokrouhlena)
                    vzdalenostOdCilovehoPatraG = round (abs(poziceG - 1)) # vzdalenost vytahu Gama od ciloveho patra (zaokrouhlena)
                    #print ('vzdalenostOdCilovehoPatraA = ', vzdalenostOdCilovehoPatraA)
                    #print ('vzdalenostOdCilovehoPatraB = ', vzdalenostOdCilovehoPatraB)
                    #print ('vzdalenostOdCilovehoPatraG = ', vzdalenostOdCilovehoPatraG)

                    if ((poziceA == 1) or ((vzdalenostOdCilovehoPatraA <= vzdalenostOdCilovehoPatraB) and (vzdalenostOdCilovehoPatraA <= vzdalenostOdCilovehoPatraG) and (e.getSpeed('Alfa') == 0))):
                        # pokud je vytah Alfa v cilovem patre, nebo je mu nejblize a nejede nikam jinam
                        GD.cilovePatroA = 1
                    
                    elif ((poziceB == 1) or ((vzdalenostOdCilovehoPatraB <= vzdalenostOdCilovehoPatraA) and (vzdalenostOdCilovehoPatraB <= vzdalenostOdCilovehoPatraG) and (e.getSpeed('Beta') == 0))):
                        # pokud je vytah Beta v cilovem patre, nebo je mu nejblize a nejede nikam jinam
                        GD.cilovePatroB = 1

                    elif ((poziceG == 1) or ((vzdalenostOdCilovehoPatraG <= vzdalenostOdCilovehoPatraA) and (vzdalenostOdCilovehoPatraG <= vzdalenostOdCilovehoPatraB) and (e.getSpeed('Gama') == 0))):
                        # pokud je vytah Beta v cilovem patre, nebo je mu nejblize a nejede nikam jinam
                        GD.cilovePatroG = 1

                elif (event == 'DoPatra2'):
                    #print ('event')
                    poziceA = e.getPosition('Alfa')
                    poziceB = e.getPosition('Beta')
                    poziceG = e.getPosition('Gama')
                    #print ('poziceA = ', poziceA)
                    #print ('poziceB = ', poziceB)
                    #print ('poziceG = ', poziceG)
                    vzdalenostOdCilovehoPatraA = round (abs(poziceA - 2)) # vzdalenost vytahu Alfa od ciloveho patra (zaokrouhlena)
                    vzdalenostOdCilovehoPatraB = round (abs(poziceB - 2)) # vzdalenost vytahu Beta od ciloveho patra (zaokrouhlena)
                    vzdalenostOdCilovehoPatraG = round (abs(poziceG - 2)) # vzdalenost vytahu Gama od ciloveho patra (zaokrouhlena)
                    #print ('vzdalenostOdCilovehoPatraA = ', vzdalenostOdCilovehoPatraA)
                    #print ('vzdalenostOdCilovehoPatraB = ', vzdalenostOdCilovehoPatraB)
                    #print ('vzdalenostOdCilovehoPatraG = ', vzdalenostOdCilovehoPatraG)

                    if ((poziceA == 2) or ((vzdalenostOdCilovehoPatraA <= vzdalenostOdCilovehoPatraB) and (vzdalenostOdCilovehoPatraA <= vzdalenostOdCilovehoPatraG) and (e.getSpeed('Alfa') == 0))):
                        # pokud je vytah Alfa v cilovem patre, nebo je mu nejblize a nejede nikam jinam
                        GD.cilovePatroA = 2
                    
                    elif ((poziceB == 2) or ((vzdalenostOdCilovehoPatraB <= vzdalenostOdCilovehoPatraA) and (vzdalenostOdCilovehoPatraB <= vzdalenostOdCilovehoPatraG) and (e.getSpeed('Beta') == 0))):
                        # pokud je vytah Beta v cilovem patre, nebo je mu nejblize a nejede nikam jinam
                        GD.cilovePatroB = 2

                    elif ((poziceG == 2) or ((vzdalenostOdCilovehoPatraG <= vzdalenostOdCilovehoPatraA) and (vzdalenostOdCilovehoPatraG <= vzdalenostOdCilovehoPatraB) and (e.getSpeed('Gama') == 0))):
                        # pokud je vytah Beta v cilovem patre, nebo je mu nejblize a nejede nikam jinam
                        GD.cilovePatroG = 2

                elif (event == 'DoPatra3'):                    
                    GD.cilovePatroG = 3
                    #print ('event')
                    GamaDoPatra(e,GD.cilovePatroG)

                elif (event == 'DoPatra4'):                    
                    GD.cilovePatroG = 4
                    #print ('event')
                    GamaDoPatra(e,GD.cilovePatroG)

# Vzhledem k tomu, ze tlacitko je stisknuto vzdy pouze jednou, a funkce "vytahDoPatra" by se tedy spustila jen jednou, musel jsem zavest "obchvat", ktery bude funkci opakovat dokud bude treba

        if (GD.cilovePatroA == 0):
                AlfaDoPatra(e,GD.cilovePatroA)
                        
        if (GD.cilovePatroA == 1):
                #print ('obchvat')
                AlfaDoPatra(e,GD.cilovePatroA)
                        
        if (GD.cilovePatroA == 2):            
                #print ('obchvat')
                AlfaDoPatra(e,GD.cilovePatroA)
                        
        if (GD.cilovePatroB == 0):            
                #print ('obchvat')
                BetaDoPatra(e,GD.cilovePatroB)

        if (GD.cilovePatroB == 1):            
                #print ('obchvat')
                BetaDoPatra(e,GD.cilovePatroB)

        if (GD.cilovePatroB == 2):            
                #print ('obchvat')
                BetaDoPatra(e,GD.cilovePatroB)

        if (GD.cilovePatroG == 0):            
                #print ('obchvat')
                GamaDoPatra(e,GD.cilovePatroG)                
                        
        if (GD.cilovePatroG == 1):            
                #print ('obchvat')
                GamaDoPatra(e,GD.cilovePatroG)
                        
        if (GD.cilovePatroG == 2):        
                #print ('obchvat')
                GamaDoPatra(e,GD.cilovePatroG)
                        
        if (GD.cilovePatroG == 3):           
                #print ('obchvat')
                GamaDoPatra(e,GD.cilovePatroG)

        if (GD.cilovePatroG == 4):        
                #print ('obchvat')
                GamaDoPatra(e,GD.cilovePatroG)


configFileName = 'r3.json' # konfiguraci vytahu ber ze souboru:
elevators.runSimulation(configFileName, elevatorSimulationStep)
