# Imported Python Transfer Function
@nrp.MapSpikeSource("input_2", nrp.brain.sensors[2], nrp.dc_source)
@nrp.MapSpikeSource("input_1", nrp.brain.sensors[1], nrp.dc_source)
@nrp.MapSpikeSource("input_0", nrp.brain.sensors[0], nrp.dc_source)
@nrp.Robot2Neuron()
def sensor2brain(t, input_2, input_1, input_0):
    import rospy
    from std_msgs.msg import Int32
    from gazebo_msgs.srv import ApplyBodyWrench, GetModelState, DeleteModel, SpawnEntity, SpawnEntityRequest
    from rospy import ServiceProxy, wait_for_service
    def callback (data):
        if(data.data == 3):
            state_proxy = ServiceProxy('/gazebo/get_model_state',
                                         GetModelState, persistent=True)
            try:
                current_cylinder_state = state_proxy("cylinder", "world")
                input_0.amplitude = current_cylinder_state.pose.position.x
                input_1.amplitude = current_cylinder_state.pose.position.y
                input_2.amplitude = current_cylinder_state.pose.position.z
            except rospy.ServiceException as exc:
                clientLogger.info(str(exc))
    sub = rospy.Subscriber('/bebbel_state', Int32, callback, queue_size=1)