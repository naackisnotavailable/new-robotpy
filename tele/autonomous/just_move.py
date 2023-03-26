from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state


class JustMove(StatefulAutonomous):
    MODE_NAME = "Just Move"

    def initialize(self):
        self.initial_called = None
