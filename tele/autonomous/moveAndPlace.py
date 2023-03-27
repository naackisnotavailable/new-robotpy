from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state


class moveAndPlace(StatefulAutonomous):
    MODE_NAME = "moveAndPlace"

    def on_enable(self):
        return super().on_enable()