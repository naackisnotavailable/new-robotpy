from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state


class moveAndPlace(StatefulAutonomous):
    MODE_NAME = "moveAndPlace"

    def initialize(self):
        self.initial_called = None