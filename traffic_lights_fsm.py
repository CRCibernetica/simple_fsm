import board
import keypad
import time
from ideaboard import IdeaBoard
from simple_fsm import State, StateMachine

# --- Hardware Setup ---
ib = IdeaBoard()
button_pins = (board.IO0,)
buttons = keypad.Keys(button_pins, value_when_pressed=False, pull=True)

# --- State Definitions ---

class Green(State):
    def enter(self):
        print("State: Green")
        ib.pixel = (0,10,0)
        self.start_time = time.monotonic()
        self.duration = 3.0
        
    def update(self):
        current_time = time.monotonic()
        if current_time - self.start_time >= self.duration:
            self.machine.transition_to(Yellow(self.machine))


class Yellow(State):
    def enter(self):
        print("State: Yellow")
        ib.pixel = (10,10,0)
        self.start_time = time.monotonic()
        self.duration = 1.0
        
    def update(self):
        current_time = time.monotonic()
        if current_time - self.start_time >= self.duration:
            self.machine.transition_to(Red(self.machine))

class Red(State):
    def enter(self):
        print("State: Red")
        ib.pixel = (10,0,0)
        self.start_time = time.monotonic()
        self.duration = 3.0
        
    def update(self):
        current_time = time.monotonic()
        if current_time - self.start_time >= self.duration:
            self.machine.transition_to(Green(self.machine))

# --- Main Execution ---

# Initialize Machine
robot_fsm = StateMachine()

# Start the machine in the initial state
robot_fsm.transition_to(Green(robot_fsm))

while True:
    event = buttons.events.get()
    
    if event:
        robot_fsm.handle_event(event)
        
    robot_fsm.update()