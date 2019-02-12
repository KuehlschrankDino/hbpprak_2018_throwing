# Imported Python Transfer Function
@nrp.MapVariable("cur_grasp_state", initial_value="reset")
@nrp.MapRobotSubscriber("grasp_state", Topic("/grasp_state", std_msgs.msg.String))
@nrp.MapSpikeSource("input_2", nrp.brain.sensors[2], nrp.dc_source)
@nrp.MapSpikeSource("input_1", nrp.brain.sensors[1], nrp.dc_source)
@nrp.MapSpikeSource("input_0", nrp.brain.sensors[0], nrp.dc_source)
@nrp.Robot2Neuron()
def sensor2brain (t, input_2, input_1, input_0, cur_grasp_state, grasp_state):
    import rospy
    from std_msgs.msg import Int32
    from gazebo_msgs.srv import ApplyBodyWrench, GetModelState, DeleteModel, SpawnEntity, SpawnEntityRequest
    from rospy import ServiceProxy, wait_for_service
    if grasp_state.value:
        cur_grasp_state.value = grasp_state.value.data

    if(cur_grasp_state.value == "throw"):
            input_0.amplitude = 30.5
            input_1.amplitude = 0
            input_2.amplitude = 0

    
 