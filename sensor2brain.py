# Imported Python Transfer Function
@nrp.MapVariable("cur_grasp_state", initial_value="reset")
@nrp.MapRobotSubscriber("grasp_state", Topic("/grasp_state", std_msgs.msg.String))
@nrp.MapSpikeSource("input_1", nrp.brain.sensors[1], nrp.dc_source)
@nrp.MapSpikeSource("input_0", nrp.brain.sensors[0], nrp.dc_source)
@nrp.Robot2Neuron()
def sensor2brain (t, input_1, input_0, cur_grasp_state, grasp_state):
    import rospy
    from std_msgs.msg import Int32
    from gazebo_msgs.srv import ApplyBodyWrench, GetModelState, DeleteModel, SpawnEntity, SpawnEntityRequest
    from rospy import ServiceProxy, wait_for_service
    if grasp_state.value:
        cur_grasp_state.value = grasp_state.value.data

    if(cur_grasp_state.value == "throw"):
<<<<<<< Updated upstream
        state_proxy = ServiceProxy('/gazebo/get_model_state', GetModelState, persistent=True)
        try:
            current_cylinder_state = state_proxy("cylinder", "world")
            input_0.amplitude = current_cylinder_state.pose.position.x
            input_1.amplitude = current_cylinder_state.pose.position.y
            input_2.amplitude = current_cylinder_state.pose.position.z
        except rospy.ServiceException as exc:
            clientLogger.info(str(exc))
=======
            input_0.amplitude = 30.5
            input_1.amplitude = 0
    elif(cur_grasp_state.value == "release"):
            input_0.amplitude = 0
            input_1.amplitude = 30.5

>>>>>>> Stashed changes
    
 