# Imported Python Transfer Function
@nrp.MapRobotSubscriber("bumper", Topic('/robot_bumper', gazebo_msgs.msg.ContactsState))
@nrp.Robot2Neuron()
def read_sensor(t, bumper):
    clientLogger.info(bumper.value) # type(bumper.value) = gazebo ContactsState
