# Imported Python Transfer Function
@nrp.MapVariable("counter", initial_value=5)
@nrp.MapVariable("cur_grasp_state", initial_value="reset")
@nrp.MapRobotSubscriber("grasp_state", Topic("/grasp_state", std_msgs.msg.String))
@nrp.MapSpikeSource("input_2", nrp.brain.sensors[2], nrp.dc_source)
@nrp.MapSpikeSource("input_1", nrp.brain.sensors[1], nrp.dc_source)
@nrp.MapSpikeSource("input_0", nrp.brain.sensors[0], nrp.dc_source)
@nrp.Robot2Neuron()
def sensor2brain(t, input_2, input_1, input_0, grasp_state, cur_grasp_state, counter):
    import rospy
    from std_msgs.msg import Int32
    from gazebo_msgs.srv import ApplyBodyWrench, GetModelState, DeleteModel, SpawnEntity, SpawnEntityRequest
    from rospy import ServiceProxy, wait_for_service
    if grasp_state.value:
        cur_grasp_state.value = grasp_state.value.data
    if(cur_grasp_state.value == "throw"):
        state_proxy = ServiceProxy('/gazebo/get_model_state', GetModelState, persistent=True)
        try:
            current_cylinder_state = state_proxy("cylinder", "world")
            clientLogger.info('input 1: {}'.format(float(int( current_cylinder_state.pose.position.x * 100)) / 100))
            clientLogger.info('input 2: {}'.format(float(int( current_cylinder_state.pose.position.y * 100)) / 100))
            clientLogger.info('input 3: {}'.format(float(int( current_cylinder_state.pose.position.z * 100)) / 100))
            input_0.amplitude = float(int( current_cylinder_state.pose.position.x * 100)) / 100
            input_1.amplitude = float(int( current_cylinder_state.pose.position.y * 100)) / 100
            input_2.amplitude = float(int( current_cylinder_state.pose.position.z * 100)) / 100
        except rospy.ServiceException as exc:
            clientLogger.info(str(exc))    
    else :
        counter.value = 5
