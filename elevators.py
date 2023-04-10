import sys
import json
import random
from queue import Queue
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QBrush, QPainter, QPen, QColor, QTextOption
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QWidget,
)

#TODO
#
# passengers path through multiple elevators
# what to do when passenger is in doors but elevator starts moving
# statistics
# UI - stats, on/off button, spawn rate options
# passengers lag behind in moving elevator (due to lerp)
#
# docs
#
# elevator door tearing when opening/closing
# max elevator capacity?

class Lerp:
    def __init__(self, lerpTime, time):
        self.startPos = QPointF(0, 0)
        self.endPos = QPointF(0, 0)
        self.lerpTime = lerpTime
        self.startTime = time

    def sample(self, time):
        t = min((time - self.startTime)/self.lerpTime, 1)
        return self.startPos*(1-t) + self.endPos*(t)

class SimulationView(QGraphicsView):
    def __init__(self, parent):
        super(SimulationView, self).__init__(parent)
        self.scale(1,-1)
        self._zoom = 0
    
    def reset_fit(self):
        r = self.scene().itemsBoundingRect()
        self.resetTransform()
        self.setSceneRect(r)
        self.fitInView(r, Qt.KeepAspectRatio)
        self._zoom = 0
        self.scale(1, -1)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        if self._zoom > 0:
            self.centerOn(QPointF( event.position().x(), -event.position().y() ))
            self.scale(factor, factor)
        elif self._zoom == 0:
            self.reset_fit()
        else:
            self._zoom = 0

class DoorItem(QGraphicsItem):
    SIZE = 200

    def __init__(self, floor):
        super(DoorItem, self).__init__()
        self.setZValue(2)
        self.floor = floor
        self.doorPosition = 0
    
    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.black, 5))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawRect(int(self.SIZE*0.25), int(self.SIZE*self.floor), int(self.SIZE*0.5), int(self.SIZE*0.75))
        painter.setBrush(QBrush(QColor(0, 128, 0, 128)))
        painter.drawRect(int(self.SIZE*(0.25-self.doorPosition*0.25)), int(self.SIZE*self.floor), int(self.SIZE*0.25), int(self.SIZE*0.75))
        painter.drawRect(int(self.SIZE*(0.5+self.doorPosition*0.25)), int(self.SIZE*self.floor), int(self.SIZE*0.25), int(self.SIZE*0.75))

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, self.SIZE*self.floor, self.SIZE, self.SIZE*0.75 )
    
    def setDoorPosition(self, position):
        self.doorPosition = position

class ElevatorItem(QGraphicsItem):
    SIZE = 200
    ID = 'default'

    def __init__(self, description):
        super(ElevatorItem, self).__init__()
        self.setZValue(0)
        self.desc = description
        self.minFloor = min(description['floors'])
        self.maxFloor = max(description['floors'])
        self.elePosition = 0
        self.doors = [-1]*(self.maxFloor-self.minFloor+1)
        for i in sorted(description['floors']):
            self.doors[i-self.minFloor] = 0
        self.doorItems = [None]*(self.maxFloor-self.minFloor+1)
        for i in range(self.minFloor, self.maxFloor+1):
            if self.doors[i-self.minFloor] != -1:
                self.doorItems[i-self.minFloor] = DoorItem(i)
    
    def paint(self, painter, option, widget):
        # Draw floors
        painter.setBrush(QBrush(Qt.transparent))
        painter.setPen(QPen(Qt.black, 5))
        painter.drawRect(self.boundingRect())
        for i in range(self.minFloor, self.maxFloor+1):
            if self.doors[i-self.minFloor] == -1:
                painter.setBrush(QBrush(Qt.gray))
            else:
                painter.setBrush(QBrush(Qt.white))
            painter.setPen(QPen(Qt.black, 3))
            painter.drawRect(0, self.SIZE*i, self.SIZE, self.SIZE)
        
        # Draw ground line
        painter.setBrush(QBrush(Qt.black))
        painter.setPen(QPen(Qt.black, 10))
        painter.drawLine(-self.SIZE, 0, self.SIZE*2, 0)
        painter.setPen(QPen(Qt.black, 5))

        # Draw elevator
        painter.setBrush(QBrush(QColor(128, 0, 0, 255)))
        painter.setPen(QPen(QColor(96, 96, 96, 255), 4))
        painter.drawLine(int(self.SIZE*0.4), int(self.SIZE*(self.maxFloor+1)), int(self.SIZE*0.4), int(self.SIZE*self.elePosition))
        painter.drawLine(int(self.SIZE*0.6), int(self.SIZE*(self.maxFloor+1)), int(self.SIZE*0.6), int(self.SIZE*self.elePosition))
        painter.setPen(QPen(Qt.black, 5))
        painter.drawRect(int(0.2*self.SIZE), int(self.SIZE*self.elePosition), int(self.SIZE*0.6), int(self.SIZE*0.8))

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, self.SIZE*self.minFloor, self.SIZE, self.SIZE*(self.maxFloor-self.minFloor+1) )
    
    def setAttributes(self, attributes):
        self.elePosition = attributes['position']
        self.setDoorsPositions(attributes['doors'])
    
    def setPosition(self, position):
        self.elePosition = position
    
    def setDoorsPositions(self, doors):
        self.doors = doors
        for i in range(self.minFloor, self.maxFloor+1):
            if self.doors[i-self.minFloor] != -1:
                self.doorItems[i-self.minFloor].setDoorPosition(self.doors[i-self.minFloor])

class PassengerItem(QGraphicsItem):
    SIZE = 30
    MOVE_TIME = 10.0

    def __init__(self):
        super(PassengerItem, self).__init__()
        self.setZValue(3)
        self.targetposition = QPointF(0, 0)
        self.draw = True
        self.goalFloor = -1
    
    def paint(self, painter, option, widget):
        if self.draw:
            painter.setBrush(QBrush(QColor(0, 153, 255, 128)))
            painter.setPen(QPen(Qt.black, 3))
            painter.drawRect(self.boundingRect())
            painter.scale(1, -1)
            font = painter.font();
            font.setPointSize ( 20 );
            painter.setFont(font);
            painter.drawText(3, -5, str(self.goalFloor))
            painter.scale(1, 1)

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, 0, self.SIZE, self.SIZE)
    
    def updatePassenger(self, data, simulator):
        if data == False:
            self.draw = False
            return
        self.draw = True
        self.goalFloor = data['goalFloor']
        elevator = None
        elevatorIndex = -1
        if data['elevatorId'] != '':
            elevator = simulator.ele[data['elevatorId']]
            elevatorIndex = list(simulator.ele).index(data['elevatorId'])
        if data['inDoors']:
            self.targetposition = QPointF(elevatorIndex*200 + 100 - self.SIZE/2, elevator['position']*200)
            self.setZValue(2)
        elif data['inElevator']:
            positionInElevator = elevator['passengers'].index(data)
            positionInElevatorX = positionInElevator % 3
            positionInElevatorY = int((positionInElevator+1) / 3 - 0.1)
            self.targetposition = QPointF(elevatorIndex*200 + 50 + (self.SIZE+5)*positionInElevatorX, elevator['position']*200 + 10 + (self.SIZE+5)*positionInElevatorY)
            self.setZValue(1)
        else: #passenger in floor
            placeInFloorQueue = 0
            for i in range(len(simulator.passengers)):
                if simulator.passengers[i] == data:
                    break
                if simulator.passengers[i]['currentFloor'] == data['currentFloor'] and not simulator.passengers[i]['inElevator'] and not simulator.passengers[i]['inDoors']:
                    placeInFloorQueue += 1
            self.targetposition = QPointF(-placeInFloorQueue * (self.SIZE + 5), data['currentFloor'] * 200)
            self.setZValue(3)

        if not 'lerp' in data:
            data['lerp'] = Lerp(self.MOVE_TIME, simulator.simulationTime)
            data['lerp'].startPos = self.targetposition
            data['lerp'].endPos = self.targetposition

        if self.targetposition != data['lerp'].endPos:
            data['lerp'].startPos = data['lerp'].endPos
            data['lerp'].endPos = self.targetposition
            data['lerp'].startTime = simulator.simulationTime

        self.setPos(data['lerp'].sample(simulator.simulationTime))

    

class Window(QWidget):
    def __init__(self, simulator):
        super().__init__()
        self.setWindowTitle('Elevators simulator')
        self.simulator = simulator
        self.scene = QGraphicsScene(-500, -500, 500, 500)

        items = list(simulator.getAllElevators())
        self.elevators = []
        for i in range(len(items)):
            ei = ElevatorItem(self.simulator.getDescription(items[i]))
            ei.ID = items[i]
            ei.setPos(i*simulator.ELEVATOR_WIDTH, 0)
            self.elevators.append(ei)
            self.scene.addItem(ei)
            for j in range(len(ei.doorItems)):
                if ei.doorItems[j] != None:
                    ei.doorItems[j].setPos(i*simulator.ELEVATOR_WIDTH, 0)
                    self.scene.addItem(ei.doorItems[j])
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

        self.passengerPool = []

        # Define the main simulation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextStep)

        # Define the UI
        hbox = QHBoxLayout()
        self.toggleTimerButton = QPushButton("Start")
        self.toggleTimerButton.clicked.connect(self.toggleTimer)
        hbox.addWidget(self.toggleTimerButton)
        self.buttonsComboBox = QComboBox()
        for b in simulator.getConfig()['buttons']:
            self.buttonsComboBox.addItem(b['id'])
        hbox.addWidget(self.buttonsComboBox)
        self.button = QPushButton("Push selected button")
        self.button.clicked.connect(self.addEvent)
        hbox.addWidget(self.button)
        self.view = SimulationView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox)
        vbox.addWidget(self.view)
        self.setLayout(vbox)

        self.positions = [0,0]
    
    def nextStep(self):
        self.simulator.i_computeNextState()

        while(len(self.passengerPool) < len(self.simulator.passengers)):
            newPassenger = PassengerItem()
            self.passengerPool.append(newPassenger)
            self.scene.addItem(newPassenger)

        for i in range(len(self.elevators)):
            self.elevators[i].setPosition(self.simulator.getPosition(self.elevators[i].ID))
            self.elevators[i].setDoorsPositions(self.simulator.getDoors(self.elevators[i].ID))
        for i in range(len(self.passengerPool)):
            if i < len(self.simulator.passengers):
                self.passengerPool[i].updatePassenger(self.simulator.passengers[i], self.simulator)
            else:
                self.passengerPool[i].updatePassenger(False, self.simulator)
        self.scene.update()

    def addEvent(self):
        self.simulator.addEvent(self.buttonsComboBox.currentText())
    
    def toggleTimer(self):
        if self.timer.remainingTime() > 0:
            self.timer.stop()
            self.toggleTimerButton.setText('Start')
        else:
            self.timer.start(3)
            self.toggleTimerButton.setText('Stop')

class Simulator:
    ELEVATOR_WIDTH = 200

    def __init__(self, configFileName, elevatorsSimulationStep, getPassengerEvent):
        self.elevatorSimulationStep = elevatorsSimulationStep
        self.getPassengerEvent = getPassengerEvent
        self.simulationTime = 0
        self.queue = Queue()
        with open(configFileName) as f:
            self.config = json.load(f)
        self.passengerManager = PassengerManager(self)
        self.passengers = []
        self.minFloor = float('inf')
        self.maxFloor = -float('inf')
        self.ele = {}
        self.accesibleFloors = []
        for e in self.config['elevators']:
            e['position'] = 0
            e['speed'] = 0
            e['speedDiff'] = 0
            e['maxFloor'] = max(e['floors'])
            e['minFloor'] = min(e['floors'])
            e['passengers'] = []
            e['passengerInDoors'] = False
            self.minFloor = min(self.minFloor, e['minFloor'])
            self.maxFloor = max(self.maxFloor, e['maxFloor'])
            e['doors'] = [-1]*(e['maxFloor']-e['minFloor']+1)
            e['doorsDiff'] = [0]*len(e['doors'])
            for i in sorted(e['floors']):
                e['doors'][i-e['minFloor']] = 0
                if not i in self.accesibleFloors:
                    self.accesibleFloors.append(i)
            self.ele[e['id']] = e
    
    def getConfig(self):
        return self.config
    
    def addEvent(self, eventText):
        self.queue.put(eventText)

    def getAllElevators(self):
        return self.ele.keys()
    
    def getDescription(self, id):
        return self.ele[id]
    
    def getPosition(self, id):
        return self.ele[id]['position']

    def getSpeed(self, id):
        return self.ele[id]['speed']
    
    def speedUp(self, id):
        self.ele[id]['speedDiff'] = self.ele[id]['speedStep']

    def speedDown(self, id):
        self.ele[id]['speedDiff'] = -self.ele[id]['speedStep']

    def numEvents(self):
        return self.queue.qsize()
    
    def getNextEvent(self):
        return self.queue.get()
    
    def getDoors(self, id):
        return self.ele[id]['doors']
    
    def openDoors(self, id, floor):
        self.ele[id]['doorsDiff'][floor-self.ele[id]['minFloor']] = 1
    
    def closeDoors(self, id, floor):
        self.ele[id]['doorsDiff'][floor-self.ele[id]['minFloor']] = -1
    
    def getDoorsPosition(self, id, floor):
        return self.ele[id]['doors'][floor-self.ele[id]['minFloor']]
    
    def getTime(self):
        return self.simulationTime
    
    def doorSensor(self, id):
        return self.ele[id]['passengerInDoors']

    def i_computeNextState(self):
        self.passengerManager.computePassengers()
        self.elevatorSimulationStep(self)
        for id in self.getAllElevators():
            self.ele[id]['speed'] += self.ele[id]['speedDiff']
            self.ele[id]['speedDiff'] = 0
            if self.ele[id]['speed'] < -self.ele[id]['maxSpeed']:
                self.ele[id]['speed'] = -self.ele[id]['maxSpeed']
            if self.ele[id]['speed'] > self.ele[id]['maxSpeed']:
                self.ele[id]['speed'] = self.ele[id]['maxSpeed']
            self.ele[id]['position'] += self.ele[id]['speed']/10
            if abs(self.ele[id]['speed']) < abs(self.ele[id]['speedStep']/2):
                self.ele[id]['speed'] = 0
            for i in range(len(self.ele[id]['doors'])):
                if self.ele[id]['doors'][i] != -1:
                    self.ele[id]['doors'][i] += 0.1*self.ele[id]['doorsDiff'][i]
                    self.ele[id]['doorsDiff'][i] = 0
                    if self.ele[id]['passengerInDoors'] and round(self.ele[id]['position']) == i + self.ele[id]['minFloor']:
                        self.ele[id]['doors'][i] = max(self.ele[id]['doors'][i], 0.3)
        self.simulationTime += 1

class PassengerManager:
    def __init__(self, simulator):
        self.simulator = simulator
        self.passengerSpawnRate = 100

    def spawnPassengers(self):
        if self.simulator.simulationTime % self.passengerSpawnRate == 0:
            startFloor = random.choice(self.simulator.accesibleFloors)
            goalFloor  = random.choice(self.simulator.accesibleFloors)
            i = 0
            while goalFloor == startFloor or not self.isFloorAccesible(startFloor, goalFloor):
                i += 1
                if i >= 100:
                    return
                goalFloor = random.choice(self.simulator.accesibleFloors)
            passenger = {'passengerId': random.randint(0, 10000000), 'inElevator': False, 'inDoors': False, 'doorsTimer': 0, 'elevatorId': '', 'currentFloor': startFloor, 'targetFloor': goalFloor, 'goalFloor': goalFloor}
            self.simulator.addEvent(self.simulator.getPassengerEvent({'isInElevator': passenger['inElevator'], 'elevator': passenger['elevatorId'], 'currentFloor': passenger['currentFloor'], 'targetFloor': passenger['targetFloor']}))
            self.simulator.passengers.append(passenger)

    def computePassengers(self):
        if self.simulator.getPassengerEvent == None:
            return
        if len(self.simulator.accesibleFloors) <= 1:
            return
        self.spawnPassengers()

        i = 0
        while i < len(self.simulator.passengers):
            passenger = self.simulator.passengers[i]
            if passenger['inDoors']:
                elevator = self.simulator.ele[passenger['elevatorId']]
                if elevator['doors'][passenger['currentFloor']] > 0.95: #passenger only enters/exits the elevator when doors are fully opened (if they are not, the passenger will wait until they are)
                    passenger['doorsTimer'] -= 1
                if passenger['doorsTimer'] <= 0:
                    passenger['inElevator'] = not passenger['inElevator']
                    passenger['inDoors'] = False
                    elevator['passengerInDoors'] = False
                    if passenger['currentFloor'] == passenger['goalFloor'] and passenger['inElevator'] == False:
                        self.simulator.passengers.remove(passenger)
                        i -= 1
                        continue
                    self.simulator.addEvent(self.simulator.getPassengerEvent({'isInElevator': passenger['inElevator'], 'elevator': passenger['elevatorId'], 'currentFloor': passenger['currentFloor'], 'targetFloor': passenger['targetFloor']}))
            elif passenger['inElevator']:
                elevator = self.simulator.ele[passenger['elevatorId']]
                if elevator['speed'] == 0 and abs(elevator['position'] - passenger['targetFloor']) < 0.05 and elevator['doors'][passenger['targetFloor']] > 0.95 and not elevator['passengerInDoors']:
                    passenger['inDoors'] = True
                    elevator['passengerInDoors'] = True
                    passenger['currentFloor'] = passenger['targetFloor']
                    passenger['doorsTimer'] = 15
                    #GET PASSENGER NEXT TARGET FLOOR#########################################
                    passenger['targetFloor'] = passenger['goalFloor']
                    elevator['passengers'].remove(passenger)
            else: #in floor
                availableElevatorIds = []
                for j in self.simulator.getAllElevators():
                    if self.simulator.ele[j]['speed'] == 0 and abs(self.simulator.ele[j]['position'] - passenger['currentFloor']) < 0.05 and self.simulator.ele[j]['doors'][passenger['currentFloor']] > 0.95 and not self.simulator.ele[j]['passengerInDoors']:
                        availableElevatorIds.append(j)
                if len(availableElevatorIds) != 0:
                    targetElevatorId = random.choice(availableElevatorIds)
                    passenger['inDoors'] = True
                    passenger['elevatorId'] = targetElevatorId
                    passenger['doorsTimer'] = 15
                    self.simulator.ele[targetElevatorId]['passengerInDoors'] = True
                    self.simulator.ele[targetElevatorId]['passengers'].append(passenger)
            i += 1

    def isFloorAccesible(self, startFloor, endFloor):
        accesibleFloors = [startFloor]
        elevators = self.simulator.ele.copy()

        i = 0
        while i < len(accesibleFloors): #MAKE MORE EFFICIENT
            for id in elevators:
                if accesibleFloors[i] in elevators[id]['floors']:
                    for floor in elevators[id]['floors']:
                        if not floor in accesibleFloors:
                            accesibleFloors.append(floor)
            i += 1

        return endFloor in accesibleFloors


def runSimulation(configFileName, elevatorsSimulationStep, getPassengerEvent=None):
    simulator = Simulator(configFileName, elevatorsSimulationStep, getPassengerEvent)
    app = QApplication(sys.argv)
    w = Window(simulator)
    w.show()
    app.exec()


if __name__ == '__main__':
    print('You should use this file as a library. Please create a new Python script where you "import elevators" and call the elevators.runSimulation(...) function. You can see "example.py" for inspiration.')
