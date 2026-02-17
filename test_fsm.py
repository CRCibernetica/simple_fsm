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

class MovingForward(State):
    def enter(self):
        print("State: Moving Forward")
        self.pixel_state = False
        self.start_time = time.monotonic()
        self.duration = 0.5
        
    def update(self):
        current_time = time.monotonic()
        if current_time - self.start_time >= self.duration:
            ib.pixel = (0,10*self.pixel_state,0)
            self.pixel_state = not self.pixel_state
            self.start_time = current_time

    def on_event(self, event):
        # Only care about sensor (button) release in this state
        if event.released:
            self.machine.transition_to(Avoiding(self.machine))

class Avoiding(State):
    def enter(self):
        print("State: Avoiding...")
        ib.pixel = (0, 0, 10) # Blue
        # Record the time we started avoiding
        self.start_time = time.monotonic()
        self.duration = 2.0 

    def update(self):
        # Non-blocking check: Has 2 seconds passed?
        current_time = time.monotonic()
        if current_time - self.start_time >= self.duration:
            print("Avoidance complete.")
            self.machine.transition_to(MovingForward(self.machine))

# --- Main Execution ---

# Initialize Machine
robot_fsm = StateMachine()

# Start the machine in the initial state
robot_fsm.transition_to(MovingForward(robot_fsm))

while True:
    event = buttons.events.get()
    
    if event:
        robot_fsm.handle_event(event)
        
    robot_fsm.update()