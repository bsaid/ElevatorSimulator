from typing import Dict, List
import elevators
from enum import Enum
from dataclasses import dataclass
from heapq import heapify, heappop, heappush

PRECISION = 0.01
ACCELERATION = 1
WAIT = 20


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

    def size(self) -> int:
        return len(self.h)


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

    def size(self) -> int:
        return len(self.h)


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


class Elevator:
    def __init__(self, el_id: str) -> None:
        self.el_id: str = el_id
        self.direction = Direction.up
        self.lift = LiftState.inactive
        self.door = DoorState.opening
        self.flat = 0
        self.above = MinHeap()
        self.below = MaxHeap()
        self.add_after_arrival: Dict[int, List[int]] = {
            -1: [],
            0: [],
            1: [],
            2: [],
            3: [],
        }
        self.dest: int = 0
        self.waitUntil = WAIT

    def _to_queue(self, flat: int):
        if flat < self.dest:
            self.below.push(flat)
        elif flat > self.dest:
            self.above.push(flat)

    def secondary_to_queue(self, start: int):
        """Add the flats which have to be visited after visiting 'start' flat to the queue"""
        for flat in self.add_after_arrival[start]:
            self._to_queue(flat)
        self.add_after_arrival[start].clear()

    def add_to_queue(self, flat: int, dest: int):
        self._to_queue(flat)
        self.add_after_arrival[flat].append(dest)
        if self.flat == flat:
            self.secondary_to_queue(flat)

    def get_load(self) -> int:
        return self.above.size() + self.below.size()

    def process(self, e: elevators.Simulator):
        if self.door == DoorState.closing and closeDoor(e, self.el_id, self.flat):
            self.door = DoorState.closed
        elif self.door == DoorState.opening and openDoor(e, self.el_id, self.flat):
            self.door = DoorState.opened
            self.lift = LiftState.inactive
            self.waitUntil = e.getTime() + WAIT
        elif self.lift == LiftState.inactive:
            # Nastavit nový cíl cesty
            if self.dest == self.flat:
                if (
                    self.above.empty() and self.below.empty()
                ) or e.getTime() < self.waitUntil:
                    return
                elif self.above.empty() and self.direction == Direction.up:
                    self.direction = Direction.down
                elif self.below.empty() and self.direction == Direction.down:
                    self.direction = Direction.up

                if self.direction == Direction.up:
                    self.dest = self.above.pop()
                else:
                    self.dest = self.below.pop()

                if self.door != DoorState.closed:
                    self.door = DoorState.closing
            # Připraveno k cestě
            elif self.door == DoorState.closed:
                self.lift = LiftState.accelerating
        if self.lift == LiftState.accelerating:
            disceleration_dist = ((e.getSpeed(self.el_id)) ** 2) / (2 * ACCELERATION)
            if disceleration_dist - PRECISION >= abs(
                self.dest - e.getPosition(self.el_id)
            ):
                self.lift = LiftState.disceleration
            elif self.direction == Direction.up:
                e.speedUp(self.el_id)
            else:
                e.speedDown(self.el_id)

        if self.lift == LiftState.disceleration:
            if abs(e.getSpeed(self.el_id)) < PRECISION / 2:
                if abs(self.dest - e.getPosition(self.el_id)) > PRECISION:
                    self.lift = LiftState.accelerating
                else:
                    self.flat = self.dest
                    self.lift = LiftState.inactive
                    self.door = DoorState.opening
                    self.waitUntil = e.getTime() + WAIT
                    self.secondary_to_queue(self.flat)
            elif self.direction == Direction.up:
                e.speedDown(self.el_id)
            else:
                e.speedUp(self.el_id)


@dataclass
class GlobalData:
    A = Elevator(el_id="A")
    B = Elevator(el_id="B")
    C = Elevator(el_id="C")

    def least_loaded(self):
        """Return ID of the least loaded elevator"""
        m = 10e9 + 7
        m_i = -1
        load = [self.A.get_load(), self.B.get_load(), self.C.get_load()]
        for i in range(len(load)):
            if m > load[i]:
                m = load[i]
                m_i = i
        if m_i == 0:
            return "A"
        elif m_i == 1:
            return "B"
        else:
            return "C"


GD = GlobalData()


def processButtons(e: elevators.Simulator):
    while e.numEvents() > 0:
        ev = e.getNextEvent()
        action, parameter = ev.split("_")
        if action.isnumeric() or action[1:].isnumeric():
            if int(action) == -1:
                GD.A.add_to_queue(int(parameter), -1)
            elif int(parameter) == -1:
                GD.A.add_to_queue(-1, int(action))
            elif int(action) == 3:
                GD.C.add_to_queue(int(parameter), 3)
            elif int(parameter) == 3:
                GD.C.add_to_queue(3, int(action))
            else:
                least_loaded_ID = GD.least_loaded()
                if least_loaded_ID == "A":
                    GD.A.add_to_queue(int(parameter), int(action))
                elif least_loaded_ID == "B":
                    GD.B.add_to_queue(int(parameter), int(action))
                else:
                    GD.C.add_to_queue(int(parameter), int(action))
        elif action == "Open":
            if parameter == "A" and GD.A.lift == LiftState.inactive:
                GD.A.door = DoorState.opening
            elif parameter == "B" and GD.B.lift == LiftState.inactive:
                GD.B.door = DoorState.opening
            elif parameter == "C" and GD.C.lift == LiftState.inactive:
                GD.C.door = DoorState.opening
        elif action == "Close":
            if parameter == "A" and (
                GD.A.door == DoorState.opening or GD.A.door == DoorState.opened
            ):
                GD.A.door = DoorState.closing
            elif parameter == "B" and (
                GD.B.door == DoorState.opening or GD.B.door == DoorState.opened
            ):
                GD.B.door = DoorState.closing
            elif parameter == "C" and (
                GD.C.door == DoorState.opening or GD.C.door == DoorState.opened
            ):
                GD.C.door = DoorState.closing
        else:
            raise Exception("Unknown event")


def openDoor(e: elevators.Simulator, el_id: str, floor: int) -> bool:
    if e.getDoorsPosition(el_id, floor) > 1 - PRECISION / 2:
        return True
    else:
        e.openDoors(el_id, floor)
        return False


def closeDoor(e: elevators.Simulator, el_id: str, floor: int) -> bool:
    if e.getDoorsPosition(el_id, floor) < PRECISION / 2:
        return True
    else:
        e.closeDoors(el_id, floor)
        return False


def elevatorSimulationStep(e: elevators.Simulator):
    processButtons(e)
    GD.A.process(e)
    GD.B.process(e)
    GD.C.process(e)

configFileName = "r5.json"
elevators.runSimulation(configFileName, elevatorSimulationStep)
