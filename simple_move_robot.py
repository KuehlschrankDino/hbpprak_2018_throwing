# Imported Python Transfer Function
@nrp.MapVariable("sebbel_time", initial_value=0)
@nrp.MapVariable("sebbel_state", initial_value=0)
@nrp.MapVariable("last_action_time", initial_value=0)
@nrp.MapSpikeSink("output_2", nrp.brain.actors[2], nrp.population_rate)
@nrp.MapSpikeSink("output_1", nrp.brain.actors[1], nrp.population_rate)
@nrp.MapSpikeSink("output_0", nrp.brain.actors[0], nrp.population_rate)
@nrp.MapRobotPublisher("arm_6", Topic("/robot/arm_6_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_5", Topic("/robot/arm_5_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_4", Topic("/robot/arm_4_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_3", Topic("/robot/arm_3_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_2", Topic("/robot/arm_2_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_1", Topic("/robot/arm_1_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_thumb_distal", Topic("/robot/hand_j3/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_thumb_flexion", Topic("/robot/hand_j4/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_pinky_distal", Topic("/robot/hand_j13/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_pinky_proximal", Topic("/robot/hand_Pinky/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_ring_distal", Topic("/robot/hand_j12/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_ring_proximal", Topic("/robot/hand_Ring_Finger/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_middle_distal", Topic("/robot/hand_Middle_Finger_Distal/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_middle_proximal", Topic("/robot/hand_Middle_Finger_Proximal/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_index_distal", Topic("/robot/hand_Index_Finger_Distal/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_index_proximal", Topic("/robot/hand_Index_Finger_Proximal/cmd_pos", std_msgs.msg.Float64))
@nrp.Neuron2Robot()

def simple_move_robot(t, hand_index_proximal, hand_index_distal, hand_middle_proximal, hand_middle_distal, hand_ring_proximal, hand_ring_distal, hand_pinky_proximal, hand_pinky_distal, hand_thumb_flexion, hand_thumb_distal, arm_1, arm_2, arm_3, arm_4, arm_5, arm_6, sebbel_time, sebbel_state, last_action_time, output_1, output_0, output_2):
    import hbp_nrp_excontrol.nrp_states as states
    from smach import StateMachine
    from smach.state import State
    from gazebo_msgs.srv import ApplyBodyWrench, GetModelState, DeleteModel, SpawnEntity, SpawnEntityRequest
    from geometry_msgs.msg import Wrench, Vector3, Point
    from std_msgs.msg import Float32, String, Int32
    import rospy
    from rospy import ServiceProxy, wait_for_service
    from hbp_nrp_excontrol.logs import clientLogger
    
    def callback (data):
        if (data.data == "init_pos"):
            sebbel_state.value = 0 
            last_action_time.value= t
    def evaluate_state(sebbel_state=0, last_action_time=0, act_time=0):
        if (sebbel_state == 0): 
            if (act_time - last_action_time) > 2: 
                sebbel_state = 1
                last_action_time = t
                return sebbel_state, last_action_time
        if (sebbel_state == 1): 
            if (act_time -last_action_time) > 3: 
                sebbel_state = 2
                last_action_time = act_time
                return sebbel_state, last_action_time
        if (sebbel_state == 2): 
            if (act_time - last_action_time) > 0.7: 
                sebbel_state = 3
                last_action_time = act_time 
                return sebbel_state, last_action_time
        if (sebbel_state == 3): 
            if (act_time -last_action_time) > 2: 
                sebbel_state = 4
                last_action_time = act_time
                return sebbel_state, last_action_time
        if (sebbel_state == 4): 
            if (act_time - last_action_time) > 4: 
                reset_pub = rospy.Publisher("/sim_finished", Int32, queue_size=1)
                reset_pub.publish(1)
                clientLogger.info("ENDE BANANE")
                rospy.Subscriber("/state", String, callback)
                sebbel_state = 0
                last_action_time = act_time 
        return sebbel_state, last_action_time
    def grasp(strength):
        for topic in [
                hand_index_proximal,
                hand_index_distal,
                hand_middle_proximal,
                hand_middle_distal,
                hand_ring_proximal,
                hand_ring_distal,
                hand_pinky_proximal,
                hand_pinky_distal,
                hand_thumb_flexion,
                hand_thumb_distal
        ]:
            topic.send_message(std_msgs.msg.Float64(strength))

    sebbel_state.value, last_action_time.value = evaluate_state(sebbel_state.value, last_action_time.value, t)
    if (sebbel_state.value == 0): 
        #approach
        arm_1.send_message(std_msgs.msg.Float64(-3.705))
        arm_2.send_message(std_msgs.msg.Float64(1.07))
        arm_3.send_message(std_msgs.msg.Float64(-1.0))
        arm_4.send_message(std_msgs.msg.Float64(3.1))
        arm_5.send_message(std_msgs.msg.Float64(-0.99))
        arm_6.send_message(std_msgs.msg.Float64(0.2))
    elif (sebbel_state.value == 1): 
        #grasp 
        grasp(5)
        arm_1.send_message(std_msgs.msg.Float64(-3.71))

    elif (sebbel_state.value == 2): 
        #accalerate

        arm_2.send_message(std_msgs.msg.Float64(1.1))
        arm_6.send_message(std_msgs.msg.Float64(-2))
    elif(sebbel_state.value == 3):
        arm_2.send_message(std_msgs.msg.Float64(-1.0 + output_1.rate / 50.0))
        arm_3.send_message(std_msgs.msg.Float64(-1.0 + output_2.rate / 50.0))
        grasp(-1.0 + output_2.rate / 50.0)

    elif (sebbel_state.value == 4): 
        #reinitiate
        grasp(0)
        arm_1.send_message(std_msgs.msg.Float64(-1.705))
        arm_2.send_message(std_msgs.msg.Float64(1.075))
        arm_3.send_message(std_msgs.msg.Float64(-1.0))
        arm_4.send_message(std_msgs.msg.Float64(3.1))
        arm_5.send_message(std_msgs.msg.Float64(-0.99))
        arm_6.send_message(std_msgs.msg.Float64(0.2))

    pub = rospy.Publisher('/bebbel_state', Int32, queue_size=10)
    pub.publish(sebbel_state.value)