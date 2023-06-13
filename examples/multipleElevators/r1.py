import elevators
from numpy import sign

ERROR_BOUND = 0.005

class Elevator:
	def __init__(self, id):
		self.id = id
		self.speedStep = 0.0
		self.maxSpeed = 0.0
		self.targetFloor = 0
		self.floorsToVisit = []
		self.direction = 1
		self.e = None
		self.state = 0
		self.doorTimer = 0
	def setConfig(self, e):
		self.e = e
		config = e.getConfig()['elevators']
		for i in range(len(config)):
			if config[i]['id'] == self.id:
				self.speedStep = config[i]['speedStep']
				self.maxSpeed = config[i]['maxSpeed']

	def closeDoor(self, floor):
		doorPos = self.e.getDoorsPosition(self.id, floor)
		if doorPos == -1:
			return True
		if doorPos < 0 + ERROR_BOUND:
			return True
		self.e.closeDoors(self.id, floor)
		return False
	def openDoor(self, floor):
		doorPos = self.e.getDoorsPosition(self.id, floor)
		if doorPos == -1:
			return True
		if doorPos > 1 - ERROR_BOUND:
			return True
		self.e.openDoors(self.id, floor)
		return False

	def onOpenDoorButton(self):
		if self.state == 2 or self.state == 3:
			self.state = 0
	def onCloseDoorButton(self):
		if self.state == 1 or self.state == 0:
			self.state = 2

	def accelerate(self, targetFloor): # accelerate toward 'targetFloor'
		position = self.e.getPosition(self.id)
		direction = sign(targetFloor - position)
		if direction == 1:
			self.e.speedUp(self.id)
		else:
			self.e.speedDown(self.id)

	def deccelerate(self):
		speed = self.e.getSpeed(self.id)
		direction = sign(speed)
		if direction == 1:
			self.e.speedDown(self.id)
		elif direction == -1:
			self.e.speedUp(self.id)

	def goToFloor(self, targetFloor):
		position = self.e.getPosition(self.id)
		speed = self.e.getSpeed(self.id)
		direction = sign(targetFloor - position)
		if speed == 0 and abs(position - targetFloor) < ERROR_BOUND: #in floor, stopped
			return True
		if abs(speed - self.speedStep) < ERROR_BOUND and abs(position - targetFloor) < ERROR_BOUND: #in floor, stopping
			self.deccelerate()
			return False
		# calculating whether to speed up or slow down: calculate what would happen if we accelerate this step, and then slow down all the next steps until we stop. if that overshoots the target floor, we want to start slowing down, otherwise, we can still accelerate without overshooting the target floor
		nextSpeed = max(min(speed + direction*self.speedStep, self.maxSpeed), -self.maxSpeed) # if we accelerate this step, what the speed will be
		slowDownSteps = abs(nextSpeed / self.speedStep) # how many steps it will take to stop
		velocitySum = (nextSpeed + direction*self.speedStep)*slowDownSteps/2.0 # what the sum of the velocities until we stop will be (velocities will be a arithmestic series: 0.05 + 0.10 + 0.15 + ... + (nextSpeed - 0.05) + (nextSpeed))
		endPos = position + velocitySum/10.0 # where the elevator will end up after stoping
		if direction*(endPos - targetFloor) > ERROR_BOUND: # if elevator would overshoot
			if abs(speed - self.speedStep) < ERROR_BOUND: # if elevator is going slowly, dont stop, wait until elevator gets to target floor
				return False
			self.deccelerate()
			return False
		else:
			self.accelerate(targetFloor)
			return False

	def callToFloor(self, floor):
		if abs(self.e.getPosition(self.id) - floor) < ERROR_BOUND and self.state < 4: # already in this floor
			self.onOpenDoorButton()
			return
		if not floor in self.floorsToVisit:
			self.floorsToVisit.append(floor)
			self.chooseNextTargetFloor()

	def simulationStep(self):
		position = self.e.getPosition(self.id)

		if self.state == 0: # in floor, opening doors
			if self.openDoor(round(position)):
				self.doorTimer = 0
				self.state = 1
		elif self.state == 1: # in floor, doors open, waiting
			self.doorTimer += 1
			if self.doorTimer >= 15:
				self.state = 2
		elif self.state == 2: # in floor, closing doors
			if self.closeDoor(round(position)):
				self.state = 3
		elif self.state == 3: # in floor, choosing target floor / waiting to be called to a floor
			if self.chooseNextTargetFloor():
				self.state = 4
		elif self.state == 4: # moving to target floor
			if self.goToFloor(self.targetFloor):
				self.floorsToVisit.remove(self.targetFloor)
				self.state = 0

	def canStopInTime(self, floor):
		# if we start slowing down this step, will we stop before getting to `floor`? (function only gets called for floors in the direction that the elevator is moving)
		position = self.e.getPosition(self.id)
		speed = self.e.getSpeed(self.id)
		if speed == 0:
			return True

		nextSpeed = speed - self.direction*self.speedStep # if we slow down this step, what the speed will be
		slowDownSteps = abs(nextSpeed / self.speedStep) # how many more steps it will take to stop
		velocitySum = (nextSpeed + self.direction*self.speedStep)*slowDownSteps/2.0 # what the sum of the velocities until we stop will be (arithmetic series: 0.05 + 0.10 + 0.15 + ... + (nextSpeed - speedStep) + nextSpeed)
		endPos = position + velocitySum/10.0 # where the elevator will end up after stoping
		return self.direction*(floor - endPos) > -ERROR_BOUND

	def chooseNextTargetFloor(self):
		if len(self.floorsToVisit) == 0:
			return False
		position = self.e.getPosition(self.id)
		chosen = False
		for floor in self.floorsToVisit:
			if self.direction*(floor - position) > 0: # floor is in the direction the elevator is going in
				if self.canStopInTime(floor): # (if elevator is already moving) elevator can stop before getting to floor
					if self.direction*(self.targetFloor - floor) > 0 or not chosen: # we need to choose something OR floor is closer to elevator than target floor
						self.targetFloor = floor
						chosen = True
		if not chosen: # no more floors to cnotinue to, go back in the other direction
			self.direction *= -1
			return False
		return True

	def TimeToGetToFloor(self, floor):
		position = self.e.getPosition(self.id)
		time = 0
		if self.state < 3: # if the elevator is opening/closing doors or waiting in the floor
			time += 40
		if len(self.floorsToVisit) == 0: # just need to get to the floor
			time += abs(floor - position)*10
			return time
		if self.direction*(floor - position) > 0 and self.canStopInTime(floor): #floor is in the direction the elevator is going
			time += abs(floor - position)*10 #time it takes to get to the floor
			for f in self.floorsToVisit:
				if (floor < f and f < position) or (floor > f and f > position): # floor 'f' is between the elevator and floor 'floor'
					time += 55 #it takes roughly 55 steps to stop at a floor
			return time
		# else: need to go to the last floor in elevator direction, then back
		lastFloor = 0
		if self.direction == 1:
			lastFloor = max(self.floorsToVisit)
		else:
			lastFloor = min(self.floorsToVisit)
		time += abs(lastFloor - position)*10 #time to get to last floor in direction
		time += abs(lastFloor - floor)*10 #time to go to floor from the last floor
		for f in self.floorsToVisit:
			if (floor < f and f <= lastFloor) or (floor > f and f >= lastFloor): # floor 'f' is between floor 'floor' and floor 'lastFloor'
				time += 55 #it takes roughly 55 steps to stop at a floor
		return time

class GD:
	Elevators = {'A': Elevator('A'), 'B': Elevator('B'), 'C': Elevator('C')}
	
def proccesEvent(e, event):
	if event.startswith("elevator"):
		event = event.split("elevator ")[1]
		floor = int(event[-1])
		elevatorId = event[0]
		GD.Elevators[elevatorId].callToFloor(floor)
	elif event.startswith("call"):
		if event.endswith("(roof)"):
			floor = int(event.split(" floor ")[1][0])
			GD.Elevators['A'].callToFloor(floor)
		else:
			floor = int(event.split(" floor ")[1][0])
			if floor == 6 or floor == 5:
				GD.Elevators['A'].callToFloor(floor)
				return
			# choose the elevator that will get to the floor the fastest
			smallestTime = 0
			bestElevatorId = ''
			for id in GD.Elevators:
				ele = GD.Elevators[id]
				time = ele.TimeToGetToFloor(floor)
				if time < smallestTime or bestElevatorId == '':
					bestElevatorId = id
					smallestTime = time
			GD.Elevators[bestElevatorId].callToFloor(floor)
	else:
		id = event[-1]
		if event.startswith("open"):
			GD.Elevators[id].onOpenDoorButton()
		else:
			GD.Elevators[id].onCloseDoorButton()

def elevatorSimulationStep(e):
	GD.Elevators['A'].setConfig(e)
	GD.Elevators['B'].setConfig(e)
	GD.Elevators['C'].setConfig(e)

	while e.numEvents() > 0:
		proccesEvent(e, e.getNextEvent())

	for id in GD.Elevators:
		GD.Elevators[id].simulationStep()


configFileName = 'r1.json'
elevators.runSimulation(configFileName, elevatorSimulationStep)
