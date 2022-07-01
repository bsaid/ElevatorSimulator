[English version](/README.md) - If you understand the English Python terminology, I would recommend you to switch to the English version when you understand Czech, too.

# Simulátor výtahů

Tento simulátor výtahů je napsaný v jazyce Python a používá PyQt5 jako grafické rozhraní. Strukturu simulovaných výtahů definuje uživatel ve formátu JSON (vysvětleno níže). Simulátor slouží jako nástroj na procvičování programování stavových automatů.

![example2](/docs/example2.png)

## Jak simulátor nainstalovat a spustit

1. [Stáhněte si simulátor jako ZIP archív.](https://github.com/bsaid/ElevatorSimulator/archive/refs/heads/main.zip). Pokud umíte s GITem, tak si raději naklonujte tento repozitář: `git clone https://github.com/bsaid/ElevatorSimulator.git`
2. Nainstalujte si [Python3](https://www.python.org/downloads/), pokud ho ještě nemáte. Během instalace zatrhněte možnost "Add to PATH". Podrobnější návod, jak nainstalovat Python3, najdete například [zde](https://naucse.python.cz/lessons/beginners/install/).
3. Doinstalujte si balíček PyQt5 zadáním příkazu do příkazové řádky (terminálu): `pip3 install PyQt5` Podrobnější návod, jak pracovat s příkazovou řádkou, najdete například [zde](https://naucse.python.cz/course/pyladies/beginners/cmdline/).
4. Otestujte spuštění simulátoru pomocí příkladu [example.py](/example.py). Opět můžete zadat následující příkaz do příkazové řádky, pokud se nacházíte ve stejné složce: `python3 ./example.py` Na Windows můžete také v průzkumníku kliknout pravým tlačítkem na soubor [example.py](/example.py) a vybrat položku `Edit in IDLE`. V otevřeném editoru lze kód upravovat nebo spustit pomocí klávesy `F5`.
5. Mělo by se objevit nové okno. Po kliknutí na tlačítko `Start` byste měli vidět něco takového:

![example4](/docs/example4.gif)

## Něco nefunguje

1. Ověřte si, že jste během instalace Pythonu opravdu zaškrtli políčko "Add to PATH". Pokud si nejste jisti, raději Python přeinstalujte.
2. Pokud používáte Windows a nefunguje vám v příkazové řádce `cmd.exe` příkaz `pip3 install PyQt5`, můžete místo něho zkusit `C:/path/to/python.exe -m pip install PyQt5`
3. Ukázkový příklad [example.py](/example.py): `python3 ./example.py` můžete také otevřít v programu `IDLE`, který se na Windows instaluje společně s Pythonem, a následně ho v tomto programu spustit pomocí `F5`.
4. Pokud stále něco nefunguje, můžete založit [Isuue tady na GitHubu](https://github.com/bsaid/ElevatorSimulator/issues). Řešitelé [Korespondenčního semináře M&M](https://mam.mff.cuni.cz/) mě můžou kontaktovat e-mailem zveřejněným společně se zadáním každého čísla.

## Příklady

### (1) Konfigurace v souboru JSON

Struktura výtahů je definována ve formátu JSON. V souboru je specifikován počet výtahů, počet pater, ve kterých patrech jednotlivé výtahy zastavují a jaká tlačítka máme k dispozici pro ovládání celého komplexu. Zde je ukázka specifikace jednoho výtahu pomocí tohoto formátu:

[docs/example1.json](/docs/example1.json)

```json
{
  "buttons": [],
  "elevators": [
    {
	  "id": "Alfa",
	  "floors": [-1,0,1,2],
	  "maxSpeed": 1.0,
	  "speedStep": 0.05
	}
  ]
}
```

Výsledek:

![example1](/docs/example1.png)

### (2) Struktura více výtahů

V JSON souboru můžeme definovat libovolný počet výtahů. Všimněte si, že výtah nemusí mít dveře v každém patře:

[docs/example2.json](/docs/example2.json)

```json
{
  "buttons": [],
  "elevators": [
    { "id": "A", "floors": [-1,0,1,2], "maxSpeed": 1.0, "speedStep": 0.05 },
	{ "id": "B", "floors": [0,1,2], "maxSpeed": 1.0, "speedStep": 0.05 },
	{ "id": "C", "floors": [-1,1,2], "maxSpeed": 1.0, "speedStep": 0.05 },
	{ "id": "D", "floors": [-1,0,1], "maxSpeed": 1.0, "speedStep": 0.05 },
	{ "id": "E", "floors": [0,2], "maxSpeed": 1.0, "speedStep": 0.05 },
	{ "id": "F", "floors": [-1,2], "maxSpeed": 1.0, "speedStep": 0.05 }
  ]
}
```

Výsledek:

![example2](/docs/example2.png)

### (3) Tlačítka pro řízení výtahů

Konfigurační JSON soubor také obsahuje seznam všech tlačítek. Každému tlačítku přiřadíme jeho název `id`, podle kterého jej později identifikujeme. Pro každé tlačítko můžeme nastavit různou barvu, popisek a pozice, kde je umístěno:

[docs/example3.json](/docs/example3.json)

```json
{
  "buttons": [
    {"id" : "Up"},
    {"id" : "Down"},
    {"id" : "Stop"}
  ],
  "elevators": [
    { "id": "A", "floors": [0,1], "maxSpeed": 1.0, "speedStep": 0.05 }
  ]
}
```

Výsledek:

![example3](/docs/example3.png)

### (4) Psaní kódu a spuštění vlastní simulace

Kód simulace píšeme v jazyce Python3. Na začátku potřebujeme importovat knihovnu `import elevators`, potom můžeme zavolat funkci `elevators.runSimulation(configFileName, elevatorSimulationStep)`, kde `configFileName` je jméno soubor s JSON konfigurací struktury výtahů `elevators.json` a `def elevatorSimulationStep(e)` je procedura, která musí být implementována uživatelem. Tato procedura je simulátorem zavolána v každém kroku simulace. Parametr `e` je třída s aktuálními informacemi o všech výtazích a také obsahuje programátorské rozhraní (API) pro interakci s výtahy během simulace.

Ukázka uživatelského kódu:

[docs/example4.py](/docs/example4.py)

```python
import elevators

class GlobalData:
    alfaDirection = 1
    deltaDirection = 0
    doorsDirection = 1

def processEvents(e):
    while e.numEvents() > 0:
        event = e.getNextEvent()
        if event == 'DeltaUp':
            GlobalData.deltaDirection = 1
        elif event == 'DeltaDown':
            GlobalData.deltaDirection = -1
        elif event == 'DeltaStop':
            GlobalData.deltaDirection = 0
        else:
            print('Unknown event.')

def processAlfa(e):
    if e.getSpeed('Alfa') > 1.9:
        GlobalData.alfaDirection = -1
    if e.getSpeed('Alfa') < -1.9:
        GlobalData.alfaDirection = 1
    if GlobalData.alfaDirection  == 1:
        e.speedUp('Alfa')
    else:
        e.speedDown('Alfa')

def processDelta(e):
    if GlobalData.deltaDirection == 1:
        e.speedUp('Delta')
    elif GlobalData.deltaDirection == -1:
        e.speedDown('Delta')
    else:
        speed = e.getSpeed('Delta')
        if speed > 0:
            e.speedDown('Delta')
        elif speed < 0:
            e.speedUp('Delta')

def processDoors(e):
    if e.getDoorsPosition('Delta', 0) > 0.9:
        GlobalData.doorsDirection = -1
    elif e.getDoorsPosition('Delta', 0) < 0.1:
        GlobalData.doorsDirection = 1

    if GlobalData.doorsDirection == 1:
        e.openDoors('Delta', 0)
    else:
        e.closeDoors('Delta', 0)

def printTelemetry(e):
    print(e.getSpeed('Alfa'), e.getDoorsPosition('Delta', 0))

def elevatorSimulationStep(e):
    processEvents(e)
    processAlfa(e)
    processDelta(e)
    processDoors(e)
    printTelemetry(e)
    
configFileName = 'elevators.json'
elevators.runSimulation(configFileName, elevatorSimulationStep)
```

JSON configuration:

[docs/example4.json](/docs/example4.json)

```
{
  "buttons": [
    {"id" : "DeltaUp"},
    {"id" : "DeltaDown"},
    {"id" : "DeltaStop"}
  ],
  "elevators": [
    {"id": "Alfa", "floors": [0,1,2], "maxSpeed": 2.0, "speedStep": 0.2},
    {"id": "Delta", "floors": [0,2], "maxSpeed": 0.5, "speedStep": 0.05}
  ]
}
```

Výsledek:

![example4](/docs/example4.gif)

### (5) Jak navrhnout bezpečnou, spolehlivou a uživatelsky přátelskou strukturu výtahů?

Odpověď na tuto otázku zůstavá jako cvičení pro uživatele. Cílem tohoto simulátoru je poskytnout simulované prostředí pro experimentování a procvičování programovaní stavových automatů.

## Funkce dostupné pro uživatele

- `e.getConfig()` - Vrací celou konfiguraci výtahů jako slovník.

- `e.addEvent(eventText)` - Vytvoří novou událost s textem `eventText`.

- `e.getAllElevators()` - Vrací seznam jmen všech výtahů.

- `e.getDescription(id)` - Vrací slovník všech parametrů pro daný výtah podle jeho ID.

- `e.getPosition(id)` - Vrací pozici daného výtahu jako float. Celé číslo říká, že výtah se nachází v patře a může otevřít dveře. Desetinné číslo říká, kde se mezi danými dvěma patry nachází.

- `e.getSpeed(id)` - Vrací rychlost daného výtahu. Kladné číslo reprezentuje stoupání. Číslo 1.0 udává rychlost stoupání jedno patro za sekundu.

- `e.speedUp(id)` - Zvýší rychlost výtahu o 0.01. Pokud výtah klesá (rychlost je záporná), tak výtah zpomalí.

- `e.speedDown(id)` - Opačná funkce k `e.speedUp(id)`.

- `e.numEvents()` - Vrací počet událostí ve frontě. Události jsou zejména stisknutá tlačítka.

- `e.getNextEvent()` - Vrací text první události ve frontě, a tuto událost z fronty odstraní.

- `e.getDoors(id)` - Dává informace o otevřených dveřích daného výtahu. Vrací seznam desetinných čísel, kde každé číslo je na intervalu od 0 do 1. Hodnota 0 znamená zavřené dveře, hodnota 1 otevřené dveře. Hodnoty jsou v seznamu seřazeny vzestupně podle čísla patra.

- `e.openDoors(id, floor)` - Začne otevírat dveře daného výtahu `id` v daném patře `floor`. Tato funkce musí být volána periodicky, dokud se dveře zcela neotevřou.

- `e.closeDoors(id, floor)` - Opačná funkce k `e.openDoors(id, floor)`.

- `e.getDoorsPosition(id, floor)` - Vrací desetinné číslo od 0 do 1 pro daný výtah `id` v daném patře `floor`. Nula znamená plně zavřené dveře a jedna znamená plně otevřené dveře.
