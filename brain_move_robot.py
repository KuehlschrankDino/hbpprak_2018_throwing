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
@nrp.MapSpikeSink("output_2", nrp.brain.actors[2], nrp.population_rate)
@nrp.MapSpikeSink("output_1", nrp.brain.actors[1], nrp.population_rate)
@nrp.MapSpikeSink("output_0", nrp.brain.actors[0], nrp.population_rate)
@nrp.MapRobotPublisher("arm_3", Topic("/robot/arm_3_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_2", Topic("/robot/arm_2_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.Robot2Neuron()
def brain_move_robot(t, output_1, output_0, output_2, arm_3, arm_2,  hand_index_proximal, hand_index_distal, hand_middle_proximal, hand_middle_distal, hand_ring_proximal, hand_ring_distal, hand_pinky_proximal, hand_pinky_distal, hand_thumb_flexion, hand_thumb_distal):
    
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
            
    arm_2.send_message(std_msgs.msg.Float64(-1.0 + output_1.rate / 50.0))
    arm_3.send_message(std_msgs.msg.Float64(-1.0 + output_2.rate / 50.0))
    grasp(-1.0 + output_2.rate / 50.0)