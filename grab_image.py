# Imported Python Transfer Function
import numpy as np
import sensor_msgs.msg
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import Float32, String, Int32
import rospy
@nrp.MapRobotPublisher("topic", Topic("/visualizer", sensor_msgs.msg.Image))
@nrp.MapRobotPublisher("visualizer_hand", Topic("/visualizer", sensor_msgs.msg.Image))
@nrp.MapRobotPublisher("visualizer", Topic("/visualizer", sensor_msgs.msg.Image))
@nrp.MapRobotSubscriber("camera", Topic("/camera/image_raw", sensor_msgs.msg.Image))
@nrp.Robot2Neuron()
def grab_image (t, camera, visualizer, visualizer_hand, topic):
    from std_msgs.msg import Float32, String, Int32
    import rospy
    image_msg = camera.value
    low_H = 0
    low_S = 0
    low_V = 90
    high_H, high_S, high_V = 255, 255, 110
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    lower_orange = np.array([10, 50, 50])
    upper_orange = np.array([20,255,255])
    if image_msg is not None:
        img = CvBridge().imgmsg_to_cv2(image_msg, "rgb8")
        clientLogger.info(img.shape)
        kernel_hand = np.ones((3,3),np.uint8)
        kernel = np.ones((8,8),np.uint8)
        frame_HSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        hand_mask = cv2.inRange(frame_HSV, (low_H, low_S, low_V),
                                (high_H, high_S, high_V))
        orange_mask = cv2.inRange(frame_HSV, lower_orange, upper_orange)
        orange_mask = cv2.bitwise_not(orange_mask)
        blue_mask = cv2.inRange(frame_HSV, lower_blue, upper_blue)
        blue_mask_inv = cv2.bitwise_not(blue_mask)
        hand_mask = cv2.bitwise_and(cv2.bitwise_and(hand_mask,
                                                    blue_mask_inv), orange_mask)
        hand_mask = cv2.morphologyEx(hand_mask, cv2.MORPH_OPEN, kernel_hand)
        mm = cv2.moments(blue_mask)
        mm_hand = cv2.moments(hand_mask)
        cX, cY = 0, 0
        cX_hand, cY_hand = 0, 0
        if (mm["m00"] != 0):
            cX = int(mm["m10"] / mm["m00"])
            cY = int(mm["m01"] / mm["m00"])
        if (mm_hand["m00"] != 0):
            cX_hand = int(mm_hand["m10"] / mm_hand["m00"])
            cY_hand = int(mm_hand["m01"] / mm_hand["m00"])
        # display the centroid
        pub = rospy.Publisher('/cX_hand', Int32, queue_size=10)
        pub.publish(cX_hand)
        pub2 = rospy.Publisher('/cY_hand', Int32, queue_size=10)
        pub2.publish(cY_hand)
        pub3 = rospy.Publisher('/cX', Int32, queue_size=10)
        pub3.publish(cX)
        pub4 = rospy.Publisher('/cY', Int32, queue_size=10)
        pub4.publish(cY)
        clientLogger.info("cX_hand: " + str(cX_hand) + " cY_hand:" + str(cY_hand))
        clientLogger.info("cX: " + str(cX) + " cY:" + str(cY))
        vis_img = cv2.bitwise_or(np.array(blue_mask), np.array(hand_mask))
        cv2.circle(vis_img, (cX, cY), 5, 255, -1)
        cv2.circle(vis_img, (cX_hand, cY_hand), 5, 255, 5)
        msg_frame = CvBridge().cv2_to_imgmsg(vis_img, 'mono8')
        visualizer.send_message(msg_frame)
        height, width, channels = img.shape
        if(cX-30<0) :
            dx1 = 0
        else: 
            dx1 = cX-30
        if(cX+20>width):
            dx2 = width
        else: 
            dx2 = cX+30
        if(cY-30<0):
            dy1= 0
        else: 
            dy1 = cY-30
        if(cY+20>height):
            dy2=height
        else: 
            dy2 = cY+30
        small_image = vis_img[dy1:dy2, dx1:dx2]
        smaller_image = cv2.resize(small_image,None,fx=0.5,fy=0.5)
        clientLogger.info("shape of smaller image:" + str(smaller_image.shape))    
        distance = np.sqrt(np.power(cX - cX_hand, 2) + np.power(cY - cY_hand, 2))
        clientLogger.info("distance between center of hand and object " + str(distance))
        return cX, cY
