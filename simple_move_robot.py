# Imported Python Transfer Function
@nrp.MapSpikeSink("output_6", nrp.brain.actors[4], nrp.population_rate)
@nrp.MapSpikeSink("output_5", nrp.brain.actors[5], nrp.population_rate)
@nrp.MapSpikeSink("output_4", nrp.brain.actors[6], nrp.population_rate)
@nrp.MapVariable("cur_grasp_state", initial_value="reset")
@nrp.MapRobotSubscriber("grasp_state", Topic("/grasp_state", std_msgs.msg.String))
@nrp.MapSpikeSink("output_3", nrp.brain.actors[3], nrp.population_rate)
@nrp.MapSpikeSink("output_2", nrp.brain.actors[2], nrp.population_rate)
@nrp.MapSpikeSink("output_1", nrp.brain.actors[1], nrp.population_rate)
@nrp.MapSpikeSink("output_0", nrp.brain.actors[0], nrp.population_rate)
@nrp.MapRobotPublisher("hand_Thumb_Opposition", Topic("/robot/hand_Thumb_Opposition/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_Thumb_Helper", Topic("/robot/hand_Thumb_Helper/cmd_pos", std_msgs.msg.Float64))
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
@nrp.MapRobotPublisher("arm_6", Topic("/robot/arm_6_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_5", Topic("/robot/arm_5_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_4", Topic("/robot/arm_4_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_3", Topic("/robot/arm_3_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_2", Topic("/robot/arm_2_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("arm_1", Topic("/robot/arm_1_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.Neuron2Robot()
<<<<<<< HEAD
def simple_move_robot(t, output_1, output_0, output_2, output_3, hand_index_proximal, hand_index_distal, hand_middle_proximal, hand_middle_distal, hand_ring_proximal, hand_ring_distal, hand_pinky_proximal, hand_pinky_distal, hand_thumb_flexion, hand_thumb_distal, arm_1, arm_2, arm_3, arm_4, arm_5, arm_6, sebbel_time, sebbel_state, last_action_time, cylinder_height, go_to_init):
    import hbp_nrp_excontrol.nrp_states as states
    from smach import StateMachine
    from smach.state import State
    from gazebo_msgs.srv import ApplyBodyWrench, GetModelState, DeleteModel, SpawnEntity, SpawnEntityRequest
    from geometry_msgs.msg import Wrench, Vector3, Point
    from std_msgs.msg import Float32, String, Int32
    import rospy
    from rospy import ServiceProxy, wait_for_service
    from hbp_nrp_excontrol.logs import clientLogger
    cylinder_height_init = 1.12015
    def callback_height (data): 
        cylinder_height.value = data.data
    def callback (data):
        if (data.data == "init_pos"):
            sebbel_state = 4
            last_action_time = t
            go_to_init.value = 1
        else :
            go_to_init.value = 0
    def evaluate_height(): 
        state_proxy = ServiceProxy('/gazebo/get_model_state',
                                         GetModelState, persistent=True)
        try:
            current_cylinder_state = state_proxy("cylinder", "world")
        except rospy.ServiceException as exc:
            clientLogger.info(str(exc))
            return 1
        clientLogger.info(current_cylinder_state.pose.position.z)
        if ((current_cylinder_state.pose.position.z - cylinder_height_init)>0.02):
            return 0
        else: 
            return 1
    def evaluate_state(sebbel_state=0, last_action_time=0, act_time=0):
        if (sebbel_state == 0): 
            if (act_time - last_action_time) > 2: 
                if(go_to_init.value == 0) :
                    sebbel_state = 1
                else:
                    sebbel_state = 4 
                last_action_time = t
                return sebbel_state, last_action_time
        if (sebbel_state == 1): 
            if (act_time -last_action_time) > 3: 
                if(go_to_init.value == 0) :
                    sebbel_state = 2
                else:
                    sebbel_state = 4 
                sebbel_state = 2
                last_action_time = act_time
                return sebbel_state, last_action_time
        if (sebbel_state == 2): 
            if (act_time - last_action_time) > 0.7: 
                if(go_to_init.value == 0) :
                    sebbel_state = 99
                else:
                    sebbel_state = 4 
                last_action_time = act_time 
                return sebbel_state, last_action_time
        if (sebbel_state == 99):          
            if (act_time - last_action_time) > 1.5: 
                pub_reset = rospy.Publisher("/start_sim_new", Int32, queue_size=1)     
                pub_reset.publish(evaluate_height())
                if(go_to_init.value == 0) :
                    sebbel_state = 3
                else:
                    sebbel_state = 0 
                last_action_time = act_time 
                return sebbel_state, last_action_time
        if (sebbel_state == 3): 
            if (act_time -last_action_time) > 2: 
                clientLogger.info("state3")
                if(go_to_init.value == 0) :
                    sebbel_state = 4
                else:
                    sebbel_state = 0 
                last_action_time = act_time
                return sebbel_state, last_action_time
        if (sebbel_state == 4): 
            if (act_time - last_action_time) > 2: 
                reset_pub = rospy.Publisher("/sim_finished", Int32, queue_size=1)
                reset_pub.publish(1)
                clientLogger.info("ENDE BANANE")
                rospy.Subscriber("/state", String, callback, queue_size=1)
                sebbel_state = 0
                last_action_time = act_time 
        return sebbel_state, last_action_time
=======
def simple_move_robot(t, output_1, output_0, output_2, output_3, output_4, output_5, output_6, grasp_state, hand_Thumb_Opposition, hand_Thumb_Helper, hand_thumb_distal, hand_thumb_flexion, hand_pinky_distal, hand_pinky_proximal, hand_ring_distal, hand_ring_proximal, hand_middle_distal, hand_middle_proximal, hand_index_distal, hand_index_proximal, arm_6, arm_5, arm_4, arm_3, arm_2, arm_1, cur_grasp_state):
    if grasp_state.value:
        cur_grasp_state.value = grasp_state.value.data
    import numpy as np
>>>>>>> 4de7016a54c469e0daa29849e0caab3515e0f0a0
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
    if(cur_grasp_state.value == "approach"):
        arm_1.send_message(std_msgs.msg.Float64(-3.65))
        arm_2.send_message(std_msgs.msg.Float64(0.95))
        arm_3.send_message(std_msgs.msg.Float64(-1.2))
        arm_4.send_message(std_msgs.msg.Float64(3.2))
        arm_5.send_message(std_msgs.msg.Float64(-0.8))
        arm_6.send_message(std_msgs.msg.Float64(0.2))
        grasp(0)
        hand_Thumb_Opposition.send_message(std_msgs.msg.Float64(1.2))
    elif(cur_grasp_state.value == "grasp"):
        grasp(0.8)
        arm_1.send_message(std_msgs.msg.Float64(-3.71))
    elif(cur_grasp_state.value == "turn_hand"):
        arm_6.send_message(std_msgs.msg.Float64(-2))
    elif(cur_grasp_state.value == "raise"):
        pass
    elif(cur_grasp_state.value == "throw"):
        clientLogger.info('output 1: {}'.format(output_1.rate)) 
        clientLogger.info('output 2: {}'.format(output_2.rate)) 
        clientLogger.info('output 3: {}'.format(output_3.rate)) 
        clientLogger.info('output 4: {}'.format(output_4.rate)) 
        clientLogger.info('output 5: {}'.format(output_5.rate)) 
        clientLogger.info('output 6: {}'.format(output_6.rate)) 
        clientLogger.info('output 0: {}'.format(output_0.rate)) 
        arm_2.send_message(std_msgs.msg.Float64(-5.0 + output_1.rate ))
        arm_3.send_message(std_msgs.msg.Float64(-5.0 + output_2.rate ))
        arm_5.send_message(std_msgs.msg.Float64(-5.0 + output_3.rate ))
        arm_1.send_message(std_msgs.msg.Float64(-5.0 + output_4.rate ))
        arm_4.send_message(std_msgs.msg.Float64(-5.0 + output_5.rate ))
        arm_6.send_message(std_msgs.msg.Float64(-5.0 + output_6.rate ))
        grasp(output_0.rate/5 - 2 )
    elif(cur_grasp_state.value == "reset"):
        grasp(0)
        arm_1.send_message(std_msgs.msg.Float64(-1.705))
        arm_2.send_message(std_msgs.msg.Float64(1.075))
        arm_3.send_message(std_msgs.msg.Float64(-1.0))
        arm_4.send_message(std_msgs.msg.Float64(3.1))
        arm_5.send_message(std_msgs.msg.Float64(-0.99))
        arm_6.send_message(std_msgs.msg.Float64(-2))
        hand_Thumb_Opposition.send_message(std_msgs.msg.Float64(1.2))
