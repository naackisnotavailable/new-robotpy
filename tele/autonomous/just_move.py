from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state


class JustMove(StatefulAutonomous):
    MODE_NAME = "Just Move"


    def on_enable(self):
        return super().on_enable()
        