import wpilib
import wpimath

#class ExampleTrajectory(object):
#    def generateTrajectory(self):
#        # 2018 cross scale auto waypoints.
#        side_start = Pose2d(Units.feet_to_meters(1.54), Units.feet_to_meters(23.23),
#                            Rotation2d.from_degrees(-180))
#        cross_scale = Pose2d(Units.feet_to_meters(23.7), Units.feet_to_meters(6.8),
#                             Rotation2d.from_degrees(-160))
#
#        interior_waypoints = []
#        interior_waypoints.append(wpimath.Translation2d(Units.feet_to_meters(14.54), Units.feet_to_meters(23.23)))
#        interior_waypoints.append(Translation2d(Units.feet_to_meters(21.04), Units.feet_to_meters(18.23)))
#
#        config = TrajectoryConfig(Units.feet_to_meters(12), Units.feet_to_meters(12))
#        config.reversed = True
#
#        trajectory = TrajectoryGenerator.generate_trajectory(
#            side_start,
#            interior_waypoints,
#            cross_scale,
#            config)