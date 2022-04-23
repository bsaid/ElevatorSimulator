# Elevators Simulator
Simulator of elevators written in Python using PyQt5 as GUI. The structure of elevators is defined in JSON file. This simulator is designed for practising of programming automata.

## How to run

1. Clone or download this repository: `git clone https://github.com/bsaid/ElevatorSimulator.git`
2. Install [Python3](https://www.python.org/downloads/) if you do not have it.
3. Install the required Python packages: `pip3 install PyQt5`
4. Run the [example.py](/example.py): `python3 ./example.py`
5. A new window with the simulation should appear. After clicking the `Start` button you should see something like this:

![example4](/docs/example4.gif)

## Examples

### (1) Configuration in JSON file

The structure of elevators is defined in JSON format. The JSON file defines the number of elevators, the number of floors, where each elevator stops and what buttons are used to control the elevators. Here is a simple example for one elevator:

[docs/example1.json](/docs/example1.json)

```json
# /docs/example1.json
```

The result:

![example1](/docs/example1.png)

### (2) More complex structure

We can define more complex structure in the JSON file. Please notice that the elevator does not have to be able to stop in every floor:

[docs/example2.json](/docs/example2.json)

```json
# /docs/example2.json
```

The result:

![example2](/docs/example2.json)

### (3) Buttons to control the elevators

The JSON file also contains a list of all buttons. Currently, we will assign only `id` for each button, but we can also set their color, caption, and where they are displayed in the simulation scene:

[docs/example3.json](/docs/example3.json)

```json
# /docs/example3.json
```

The result:

![example3](/docs/example3.json)

### (4) Writing the code

The user code is a Python3 file that needs to `import elevators`, and then it has to call `elevators.runSimulation(configFileName, elevatorSimulationStep)` where `configFileName` is the name of the `elevators.json` file and `def elevatorSimulationStep(e)` is a procedure that needs to be implemented by user and that is called inside the simulation loop. The parameter `e` is a class with the current information about all the elevators and it also contains API to interact with the elevators during the simulation.

Example of the user code:

[docs/example4.py](/docs/example4.py)

```python
# /docs/example4.py
```

JSON configuration:

[docs/example4.json](/docs/example4.json)

```
# /docs/example4.json
```

The result:

![example4](/docs/example4.gif)

## Simulation API

- `e.getConfig()` - Return the whole configuration as Python dictionary.

- `e.addEvent(eventText)` - Creates a new event with `eventText` string.

- `e.getAllElevators()` - Returns a list of string IDs of all elevators.

- `e.getDescription(id)` - Returns a dictionary of all parametrs for given elevator ID.

- `e.getPosition(id)` - Returns position of the given elevator as float. Integers represent that the elevator is exactly in given floor. Decimal numbers represent positions between floors.

- `e.getSpeed(id)` - Returns the current speed of the given elevator. Positive number represents climbing direction. Number 1.0 represents a speed of 1.0 floors per second.

- `e.speedUp(id)` - Increases speed of the given elevator. If the elevator is descending (has negative speed), this negative speed is decreased.

- `e.speedDown(id)` - Opposite function to `e.speedUp(id)`.

- `e.numEvents()` - Returns the number of events in the queue.

- `e.getNextEvent()` - Returns the string of the first event in the queue and removes this event from the queue.

- `e.getDoors(id)` - Returns a list of float numbers representing all door positions for the given elevator. Zero means closed doors, one means fully opened doors.

- `e.openDoors(id, floor)` - Start or keep opening of the doors for given elevator at given floor. This function must be called repeatedly until the doors are fully opened.

- `e.closeDoors(id, floor)` - Oposite function to `e.openDoors(id, floor)`.

- `e.getDoorsPosition(id, floor)` - Returns position of the doors for given elevator at given floor. Zero means closed doors, one means fully opened doors.
