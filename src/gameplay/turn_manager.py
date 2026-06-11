class TurnManager:
    def __init__(self):
        self.phases = ["start", "draw", "main", "action", "end"]
        self.phase_index = 0
        self.turn_number = 1

    @property
    def current_phase(self):
        return self.phases[self.phase_index]

    def advance_phase(self):
        self.phase_index += 1

        if self.phase_index >= len(self.phases):
            self.phase_index = 0
            self.turn_number += 1

        return self.current_phase
