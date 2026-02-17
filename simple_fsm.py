# simple_fsm.py
class State:
    """Base class for all states."""
    def __init__(self, machine):
        self.machine = machine

    def enter(self):
        """Called when entering this state."""
        pass

    def exit(self):
        """Called when exiting this state."""
        pass

    def update(self):
        """Called every loop cycle."""
        pass

    def on_event(self, event):
        """Handle hardware events (like button presses)."""
        pass

class StateMachine:
    def __init__(self):
        self.state = None

    def transition_to(self, new_state):
        if self.state:
            self.state.exit()
        self.state = new_state
        self.state.enter()

    def update(self):
        if self.state:
            self.state.update()

    def handle_event(self, event):
        if self.state:
            self.state.on_event(event)