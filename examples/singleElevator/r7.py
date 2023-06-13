import elevators

class GD:
    PRECISION = 0.001 # should be lower than set speedStep in .json file
    WAITING_TIMEOUT = 20 # same meaning as in "Zdrojový kód 3. úlohy"
    waiting_from = - WAITING_TIMEOUT - 1 # to not wait on the beginning
    events_list = [] # temporary event storage for better handling

    # If some of the following variables are True, that means that elevator
    # hasn't been in the floor since relevant button was pressed
    floor0 = False
    floor1 = False
    floor2 = False
    floor3 = False

    # If some of the following variables are True, elevator next action (if user
    # don't interact is toward that
    open_door = False
    close_door = False
    open_door_automatically = True
    close_door_automatically  = False

    # Up-to date information about elevator position
    actual_position = 0
    elevator_in_floor = True
    actual_speed = 0

    id = "Alfa" # should be same as in .json file
    # The following two variables are needed for opening only closing door
    previous_door_position = 0
    actual_door_position = 0
    travelling_aim = [] # aims for elevator in order
    count_acceleration = 0 # number of elevator accelerations and deaccelaration

def isInFloor(e):
    upper_limit = round(GD.actual_position) + GD.PRECISION
    bottom_limit = round(GD.actual_position) - GD.PRECISION

    # Check if, elevator is in floor
    if GD.actual_position < upper_limit and GD.actual_position > bottom_limit:
        return True
    else:
        return False

def updateDoorPosition(e, id, floor):
    # Doors can be open only if elevator is in floor as well as speed is zero
    if GD.elevator_in_floor and GD.actual_speed == 0:
       GD.previous_door_position = GD.actual_door_position
       GD.actual_door_position = e.getDoorsPosition(id, int(round(floor)))
       return True
    else:
        # Otherwise all doors are closed
        # reset the values
        GD.previous_door_position = 0
        GD.actual_door_position = 0
        return False

# following two function are corresponding with "def zacniCekat(e)" and
# "def casUplynul(e)" in Zdrojový kód 3. úlohy"
def startWaiting(e):
    GD.waiting_from = e.getTime()

def enoutghWaiting(e):
    a = e.getTime() - GD.waiting_from > GD.WAITING_TIMEOUT
    if a:
        # reset the "clock" to default, so it is ready to next usage
        GD.waiting_from = - GD.WAITING_TIMEOUT - 1 # reset
        return True
    else:
        # time do not pass, still waiting
        return False

def checkDoorValues(e):
    # open_door and close_door are variables, which are set by user
    # because opening door is avaible only during its closing, it has higher
    # priority than closing them on user will
    # automatics movements has lower priority
    if GD.open_door:
        # when opening on user will, no other door movement is wanted
        GD.close_door = False
        GD.close_door_automatically = False
        GD.open_door_automatically = False
    elif GD.close_door:
        # same meaning as previous block
        GD.close_door_automatically = False
        GD.open_door_automatically = False
    else:
        pass
    return True

def moveDoor(e, id, floor):
    if GD.open_door_automatically or GD.open_door:
        # we want to open door
        # compensate deviations
        upper_limit = 1 + GD.PRECISION
        bottom_limit = 1 - GD.PRECISION
        # door are fully open
        if GD.actual_door_position < upper_limit and GD.actual_door_position >bottom_limit:
            # stop opening the door
            GD.open_door = False
            GD.open_door_automatically = False
            # get ready to close the door
            GD.close_door_automatically = True
            # Wait a while
            # actualy this is somehow illogically, because when the door is
            # closed, it is impossible to open them unless elevator move to
            # other floor
            # may better to close the door after pressing some buttom for
            # elevator movement (when GD.travelling_aim is not empty)
            startWaiting(e)
        # else door isn't fullly open so continue opening the door
        else:
            e.openDoors(id, floor)
    # analogous solution as for opening door
    elif GD.close_door_automatically or GD.close_door:
        upper_limit = 0 + GD.PRECISION
        bottom_limit = 0 - GD.PRECISION
        if GD.actual_door_position < upper_limit and GD.actual_door_position >bottom_limit:
            GD.close_door = False
            GD.close_door_automatically = False
            startWaiting(e)
        else:
            e.closeDoors(id, floor)
    else:
        pass

def getAllEvents(e):
    events_in_queue = e.numEvents()

    # transform each event into the list
    for i in range(e.numEvents()):
        GD.events_list.append(e.getNextEvent())

    removeDuplicateEvents(e)

    # Check and possibly react to button-event
    if 'Ground floor' in GD.events_list:
        if GD.floor0:
            # button has been already pressed and proceed
            pass
        else:
            if GD.elevator_in_floor and round(GD.actual_position) == 0:
                # ignore pressing the button
                GD.events_list.remove('Ground floor') # should be done after reaching the floor
                # elevator is already in the floor
                # no action is needed
                pass
            else:
                # mark request
                GD.floor0 = True
                # function, which optimalizate elevator movement
                addTravelAim(e, 0)
                GD.events_list.remove('Ground floor') # should be done after reaching the floor

    if '1. floor' in GD.events_list:
        if GD.floor1:
            pass
        else:
            if GD.elevator_in_floor and round(GD.actual_position) == 1:
                # ignore pressing the button
                GD.events_list.remove('1. floor')# should be done after reaching the floor
                # elevator is already in the floor
                # no action is needed
                pass
            else:
                # mark request
                GD.floor1 = True
                # function, which optimalizates elevator movement
                addTravelAim(e, 1)
                GD.events_list.remove('1. floor')# should be done after reaching the floor

    if '2. floor' in GD.events_list:
        if GD.floor2:
            pass
        else:
            if GD.elevator_in_floor and round(GD.actual_position) == 2:
                # ignore pressing the button
                GD.events_list.remove('2. floor')# should be done after reaching the floor
                # elevator is already in the floor
                # no action is needed
                pass
            else:
                # mark request
                GD.floor2 = True
                # function, which optimalizates elevator movement
                addTravelAim(e, 2)
                GD.events_list.remove('2. floor')# should be done after reaching the floor

    if '3. floor' in GD.events_list:
        if GD.floor3:
            pass
        else:
            if GD.elevator_in_floor and round(GD.actual_position) == 3:
                # ignore pressing the button
                GD.events_list.remove('3. floor')# should be done after reaching the floor
                # elevator is already in the floor
                # no action is needed
                pass
            else:
                # mark request
                GD.floor3 = True
                # function, which optimalizates elevator movement
                addTravelAim(e, 3)
                GD.events_list.remove('3. floor')# should be done after reaching the floor

    if 'Open the closing door' in GD.events_list:
        if GD.previous_door_position > GD.actual_door_position:
            # mark request
            GD.open_door = True
            GD.events_list.remove('Open the closing door')

    if 'Close door' in GD.events_list:
        # mark request
        GD.close_door = True
        GD.events_list.remove('Close door')

def addTravelAim(e, floor_number):
    # function to optimalizate elevator movement
    # it was composed with three following assumptions

    # 1) We don't want change elevator direction between the floors
    # otherwise jokes can summon the elevator from ground floor in such a way
    # that others passengers will never reach the first floor from ground floor

    # 2) We want attend to passengers in chronological orded
    # If two button are pressed in same cycle, there are consider as simultaneous
    # so it no matter, which request is handled first
    # otherwise (for example) if elevator is in the first floor and it is
    # pernamentaly summon from ground floor, passengers from third floor will
    # never make it

    # 3) When elevator is going to his aim throught floors, where was summon too
    # it will stop there (optimalization)
    if floor_number in GD.travelling_aim:
        # do nothing, elevator will go to that floor
        return "Already in travelling_aim"

    # set a counter
    a = 0
    if GD.travelling_aim:
        # Check if a new aim is placed between current position and (some) following aim
        for i in GD.travelling_aim:
            # following condition holds interval, where new aim should be to be added
            # one of the intervals is always blank
            if (i > floor_number and floor_number > GD.actual_position) \
                    or (i < floor_number and floor_number < GD.actual_position):
                # add aim
                GD.travelling_aim.insert(a, floor_number)
                # no need to contioue the function
                return True
            else:
                # update counter
                a += 1
        # add new aim at the end of the queue
        GD.travelling_aim.insert(a, floor_number)
    else:
        # no previous aim, place it as a first on
        GD.travelling_aim.append(floor_number)


def removeDuplicateEvents(e):
    # do not keep event order
    # however is very unlikely that program receive more than one button input
    # in one cycle (it is quit short time)
    # due to this the function may lost sense
    ls = GD.events_list
    no_duplicate_ls = [*set(ls)]
    GD.events_list = no_duplicate_ls

def goTofloor(e, id, floor):
    bottom_limit = round(GD.actual_position, 2) - GD.PRECISION
    upper_limit = round(GD.actual_position, 2) + GD.PRECISION

    # Check, if is in final destination
    # following block is only for travelling up
    if floor >= bottom_limit:
        if isInFloor(e):
            print("Elevator is in a floor.")
            if round(GD.actual_position) == floor:
                print("Aim has been reached.")
                GD.count_acceleration += 1
                if (floor == 0) and (GD.floor0):
                    # stop the elevator
                    if e.getSpeed(id) > 0:
                        e.speedDown(id)
                    else:
                        e.speedUp(id)
                    # aim was reached, so set settings to default
                    GD.floor0 = False
                    GD.travelling_aim.pop(0)
                    GD.count_acceleration = 0
                elif (floor == 1) and (GD.floor1):
                    if e.getSpeed(id) > 0:
                        e.speedDown(id)
                    else:
                        e.speedUp(id)
                    GD.floor1 = False
                    GD.travelling_aim.pop(0)
                    GD.count_acceleration = 0
                elif (floor == 2) and (GD.floor2):
                    if e.getSpeed(id) > 0:
                        e.speedDown(id)
                    else:
                        e.speedUp(id)
                    GD.floor2 = False
                    GD.travelling_aim.pop(0)
                    GD.count_acceleration = 0
                elif (floor == 3) and (GD.floor3):
                    if e.getSpeed(id) > 0:
                        e.speedDown(id)
                    else:
                        e.speedUp(id)
                    GD.floor3 = False
                    GD.travelling_aim.pop(0)
                    GD.count_acceleration = 0
                print("-"*80)
                # elevator has reached its aim, so open the door
                GD.open_door = True
                return True
            elif e.getSpeed(id) == 0:
                # otherwise elevator is in some floor and it has to continue to
                # its destination
                # Up, because in this branch is aim higher than actual_position
                e.speedUp(id)
            else:
                # not necessary
                GD.count_acceleration = 0
                pass
        # elevator firstly accelerate
        # than once is its speed constant
        # then deaccelerate (same times as accelerate)
        # that cycle is done on distance of one floor, which allow elevator to
        # stop in a floor and react to relevant button before reaching the floor
        # That movement I chose due to optimalization e.g. when elevator is
        # going to 3. floor, it is possible to stop in 2. floor (if its elevator
        # actual position under 2. floor
        # For the following constant is important that speedStep is set to 0.5
        elif GD.count_acceleration < 3:
            e.speedUp(id)
            print("Speed up")
            GD.count_acceleration += 1
        elif GD.count_acceleration == 3:
            GD.count_acceleration += 1
            print("ELse")
        elif GD.count_acceleration < 7:
            GD.count_acceleration += 1
            print("Speed down")
            e.speedDown(id)
        elif GD.count_acceleration % 2 == 0:
            GD.count_acceleration += 1
            print("Speed was not change")
        else:
            pass

    # when target floor is lower than elevator actual position
    # analogous as previous branch
    else:
        if isInFloor(e):
            print("Elevator is in floor 2")
            if round(GD.actual_position) == floor:
                # never go into this brench
                pass
            elif e.getSpeed(id) == 0:
                e.speedDown(id)
            else:
                GD.count_acceleration = 0
                pass
        elif GD.count_acceleration < 3:
            e.speedDown(id)
            print("Speed Down 2")
            GD.count_acceleration += 1
        elif GD.count_acceleration == 3:
            GD.count_acceleration += 1
            print("ELse")
        elif GD.count_acceleration < 7:
            GD.count_acceleration += 1
            print("Speed Up 2")
            e.speedUp(id)
        elif GD.count_acceleration % 2 == 0:
            GD.count_acceleration += 1
            print("Speed was not change")
        else:
            pass

    print("round", GD.count_acceleration)
    print("position: ", e.getPosition(id))
    print("speed: ", e.getSpeed(id))
    print("-"*80)
    return False

def prechodovaFunkce(e):
    # gain basic information
    GD.actual_position = e.getPosition(GD.id)
    GD.actual_speed = e.getSpeed(GD.id)
    # update more complex information
    updateDoorPosition(e, GD.id, round(GD.actual_position))
    elevator_in_floor = isInFloor(e)
    getAllEvents(e)
    checkDoorValues(e)

    # Check, if elevator should wait
    # imediately close doors on user will
    if GD.close_door and GD.elevator_in_floor:
        # reset the "clock" to default, so it is ready to next usage
        GD.waiting_from = - GD.WAITING_TIMEOUT - 1 # reset
        moveDoor(e, GD.id, int(round(GD.actual_position)))
    elif (not(GD.open_door)) and (not(GD.close_door)) and \
            (not(GD.open_door_automatically)) and (not(GD.close_door_automatically)):
        try:
            if goTofloor(e,GD.id, GD.travelling_aim[0]):
                # start open a door
                pass
        except IndexError:
            print("No aim was given.")
    elif enoutghWaiting(e):
        if updateDoorPosition(e, GD.id, GD.actual_position):
            moveDoor(e, GD.id, int(round(GD.actual_position)))
        else:
            # elevator is not in floor with zero speed
            pass
    else:
        # wait
        pass

elevators.runSimulation("r7.json", prechodovaFunkce)
