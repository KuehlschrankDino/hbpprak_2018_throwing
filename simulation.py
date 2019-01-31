import time
from std_msgs.msg import Float32
import rospy
import logging
from brain_strings import BRAIN_SIMPLE
from hbp_nrp_virtual_coach.virtual_coach import VirtualCoach
import numpy as np

class ThrowingExperiment(object):
    
    def __init__(self):
        self.last_status = [None]
        self.vc = VirtualCoach(environment='local', storage_username='nrpuser')
        self.simulation_time = 40
        self.distances = []
        self.BRAIN_TEMPLATE = BRAIN_SIMPLE
        self.distance_received = False
        #disable global logging from the virtual coach
        logging.disable(logging.INFO)
        logging.getLogger('rospy').propagate = False
        logging.getLogger('rosout').propagate = False

    def wait_condition(self, timeout, condition):
        start = time.time()
        while time.time() < start + timeout:
            time.sleep(0.25)
            if condition(self.last_status[0]) or self.distance_received:
                return
        raise Exception('Condition check failed')        

    def on_status(self, status):
        self.last_status[0] = status

    def on_distance(self, data):  
        if(not self.distance_received):
            self.distances.append(abs(data.data))
            self.distance_received = True
    
    def reset_for_new_generation(self):
        self.distances = []
        self.distance_received = False
    
    def __create_current_Pop(self, weights):

        def key_func(e):
            return e['distance']

        pop = []
        for i, distance in enumerate(self.distances):
            pop.append({
                'weights': weights[i],
                'distance': distance
                })
        pop.sort(key=key_func, reverse=True)
        return pop

    def run_experiment(self, weights):
        self.reset_for_new_generation()
        for i, weight in enumerate(weights):
            try:
                self.sim = self.vc.launch_experiment('hbpprak_2018_throwing')
            except:
                print("COULD NOT LOAD EXPERIMENT")
                time.sleep(1)
            time.sleep(2)
            try:
                brain = self.BRAIN_TEMPLATE.format(weight.shape[0], weight.shape[1], np.array2string(weight,separator=","))
                self.sim.edit_brain(brain)
                self.distanceSub = rospy.Subscriber("/cylinder_distance", Float32, self.on_distance, queue_size=10)
            except:
                print("Failed to load das hirn.")
                self.sim.stop()
                time.sleep(10)
                continue

            self.sim.register_status_callback(self.on_status)
            self.wait_condition(10, lambda x: x is not None)

            self.sim.start()
            self.wait_condition(1500, lambda x: x['simulationTime'] == self.simulation_time)
            self.sim.pause()
            if(self.distance_received):
                print("Instance {}, Distance: {}".format(i, self.distances[-1]))
            else:
                self.distances.append(0)
            self.sim.stop()
            time.sleep(5)
            self.distance_received = False
        return self.__create_current_Pop(weights)