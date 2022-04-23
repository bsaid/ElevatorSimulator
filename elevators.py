import sys
import json
from queue import Queue
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QBrush, QPainter, QPen, QColor
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

class ElevatorItem(QGraphicsItem):
    SIZE = 200
    ID = 'default'

    def __init__(self, description):
        super(ElevatorItem, self).__init__()
        self.desc = description
        self.minFloor = min(description['floors'])
        self.maxFloor = max(description['floors'])
        self.elePosition = 0
        self.doors = [-1]*(self.maxFloor-self.minFloor+1)
        for i in sorted(description['floors']):
            self.doors[i-self.minFloor] = 0
    
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

        # Draw doors
        if self.ID == 'Bravo':
            print(self.doors)
        for i in range(self.minFloor, self.maxFloor+1):
            if self.doors[i-self.minFloor] != -1:
                painter.setBrush(QBrush(Qt.transparent))
                painter.drawRect(int(self.SIZE*0.25), int(self.SIZE*i), int(self.SIZE*0.5), int(self.SIZE*0.75))
                painter.setBrush(QBrush(QColor(0, 128, 0, 128)))
                painter.drawRect(int(self.SIZE*(0.25-self.doors[i-self.minFloor]*0.25)), int(self.SIZE*i), int(self.SIZE*0.25), int(self.SIZE*0.75))
                painter.drawRect(int(self.SIZE*(0.5+self.doors[i-self.minFloor]*0.25)), int(self.SIZE*i), int(self.SIZE*0.25), int(self.SIZE*0.75))

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, self.SIZE*self.minFloor, self.SIZE, self.SIZE*(self.maxFloor-self.minFloor+1) )
    
    def setAttributes(self, attributes):
        self.elePosition = attributes['position']
        self.doors = attributes['doors']
    
    def setPosition(self, position):
        self.elePosition = position
    
    def setDoorsPositions(self, doors):
        self.doors = doors


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
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

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

        for i in range(len(self.elevators)):
            self.elevators[i].setPosition(self.simulator.getPosition(self.elevators[i].ID))
            self.elevators[i].setDoorsPositions(self.simulator.getDoors(self.elevators[i].ID))
        self.scene.update()

    def addEvent(self):
        self.simulator.addEvent(self.buttonsComboBox.currentText())
    
    def toggleTimer(self):
        if self.timer.remainingTime() > 0:
            self.timer.stop()
            self.toggleTimerButton.setText('Start')
        else:
            self.timer.start(100)
            self.toggleTimerButton.setText('Stop')

class Simulator:
    ELEVATOR_WIDTH = 200

    def __init__(self, configFileName, elevatorsSimulationStep):
        self.elevatorSimulationStep = elevatorsSimulationStep
        self.queue = Queue()
        with open(configFileName) as f:
            self.config = json.load(f)
        self.ele = {}
        for e in self.config['elevators']:
            e['position'] = 0
            e['speed'] = 0
            e['speedDiff'] = 0
            e['maxFloor'] = max(e['floors'])
            e['minFloor'] = min(e['floors'])
            e['doors'] = [-1]*(e['maxFloor']-e['minFloor']+1)
            e['doorsDiff'] = [0]*len(e['doors'])
            for i in sorted(e['floors']):
                e['doors'][i-e['minFloor']] = 0
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
    
    def i_computeNextState(self):
        self.elevatorSimulationStep(self)
        for id in self.getAllElevators():
            self.ele[id]['speed'] += self.ele[id]['speedDiff']
            self.ele[id]['speedDiff'] = 0
            if self.ele[id]['speed'] < -self.ele[id]['maxSpeed']:
                self.ele[id]['speed'] = -self.ele[id]['maxSpeed']
            if self.ele[id]['speed'] > self.ele[id]['maxSpeed']:
                self.ele[id]['speed'] = self.ele[id]['maxSpeed']
            self.ele[id]['position'] += self.ele[id]['speed']/10
            if abs(self.ele[id]['speed']) < abs(self.ele[id]['speedStep']):
                self.ele[id]['speed'] = 0
            for i in range(len(self.ele[id]['doors'])):
                if self.ele[id]['doors'][i] != -1:
                    self.ele[id]['doors'][i] += 0.1*self.ele[id]['doorsDiff'][i]
                    self.ele[id]['doorsDiff'][i] = 0


def runSimulation(configFileName, elevatorsSimulationStep):
    simulator = Simulator(configFileName, elevatorsSimulationStep)
    app = QApplication(sys.argv)
    w = Window(simulator)
    w.show()
    app.exec()


if __name__ == '__main__':
    print('You should use this file as a library. Please create a new Python script where you "import elevators" and call the elevators.runSimulation(...) function. You can see "example.py" for inspiration.')
