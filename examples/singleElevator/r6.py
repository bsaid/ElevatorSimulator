from typing import Optional
from ElevatorSimulator import elevators
from enum import Enum
from heapq import heapify, heappop, heappush

PRECISION = 0.01
ACCELERATION = 1
WAIT = 20
ID = 'A'

class MinHeap:
    """Wrapper for minimum heap"""

    def __init__(self):
        self.h = []
        heapify(self.h)

    def push(self, v: int) -> None:
        heappush(self.h, v)

    def pop(self) -> int:
        return heappop(self.h)

    def empty(self) -> bool:
        return len(self.h) == 0


class MaxHeap:
    """Wrapper for maximum heap"""

    def __init__(self):
        self.h = []
        heapify(self.h)

    def push(self, v: int) -> None:
        heappush(self.h, v * -1)

    def pop(self) -> int:
        return heappop(self.h) * -1

    def empty(self) -> bool:
        return len(self.h) == 0


class Direction(Enum):
    down = 0
    up = 1

class LiftState(Enum):
    inactive = 0
    accelerating = 1
    disceleration = 2

class DoorState(Enum):
    closed = 0
    closing = 1
    opened = 2
    opening = 3

class GD:
    direction = Direction.up
    lift = LiftState.inactive
    door = DoorState.opening
    flat = 0
    above = MinHeap()
    below = MaxHeap()
    dest: Optional[int] = None
    start = 0
    waitUntil = WAIT

def processButtons(e: elevators.Simulator):
    while e.numEvents() > 0:
        ev = e.getNextEvent()
        if ev.isnumeric():
            # Patro, podle kterého dělím přidávaná patra na horní a dolní
            # je buď patro, ve které výtah stojí nebo kde má cíl jízdy
            curFlat = GD.start if GD.dest is None else GD.dest
            newFlat = int(ev)
            if newFlat > curFlat:
                GD.above.push(newFlat)
            elif newFlat < curFlat:
                GD.below.push(newFlat)
        elif GD.lift == LiftState.inactive:
            if ev == "Open":
                GD.door = DoorState.opening
            else:
                GD.door = DoorState.closing
                GD.waitUntil = e.getTime()

def openDoor(e: elevators.Simulator, floor: int) -> bool:
    if e.getDoorsPosition(ID, floor) > 1 - PRECISION / 2:
        return True
    else:
        e.openDoors(ID, floor)
        return False

def closeDoor(e: elevators.Simulator, floor: int) -> bool:
    if e.getDoorsPosition(ID, floor) < PRECISION / 2:
        return True
    else:
        e.closeDoors(ID, floor)
        return False

def elevatorSimulationStep(e: elevators.Simulator):
    processButtons(e)
    if GD.door == DoorState.closing and closeDoor(e, GD.start):
        GD.door = DoorState.closed
    elif GD.door == DoorState.opening and openDoor(e, GD.start):
        GD.door = DoorState.opened
        GD.lift = LiftState.inactive
    if GD.lift == LiftState.inactive:
        # Nastavit nový cíl cesty
        if GD.dest is None:
            if (GD.above.empty() and GD.below.empty()) or e.getTime() < GD.waitUntil:
                return
            elif GD.above.empty() and GD.direction == Direction.up:
                GD.direction = Direction.down
            elif GD.below.empty() and GD.direction == Direction.down:
                GD.direction = Direction.up

            if GD.direction == Direction.up:
                GD.dest = GD.above.pop()
            else:
                GD.dest = GD.below.pop()

            if GD.door != DoorState.closed:
                GD.door = DoorState.closing
        # Připraveno k cestě
        elif GD.door == DoorState.closed:
            GD.lift = LiftState.accelerating

    if GD.lift == LiftState.accelerating:
        disceleration_dist = ((e.getSpeed(ID)) ** 2) / (2 * ACCELERATION)
        if disceleration_dist - PRECISION >= abs(GD.dest - e.getPosition(ID)):
            GD.lift = LiftState.disceleration
        elif GD.direction == Direction.up:
            e.speedUp(ID)
        else:
            e.speedDown(ID)

    if GD.lift == LiftState.disceleration:
        if abs(e.getSpeed(ID)) < PRECISION / 2:
            if abs(GD.dest - e.getPosition(ID)) > PRECISION:
                GD.lift = LiftState.accelerating
            else:
                GD.lift = LiftState.inactive
                GD.door = DoorState.opening
                GD.start = GD.dest
                GD.dest = None
                GD.waitUntil = e.getTime() + WAIT
        elif GD.direction == Direction.up:
            e.speedDown(ID)
        else:
            e.speedUp(ID)
    
configFileName = 'r6.json'
elevators.runSimulation(configFileName, elevatorSimulationStep)
