import time
from std_msgs.msg import Float32
import rospy
<<<<<<< HEAD
from std_msgs.msg import Float32, Int32
import numpy as np


class ThrowingSim():
    BRAIN_TEMPLATE = '''#-*- coding: utf-8 -*-
#pragma: no cover
__author__ = 'Template'
from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np
=======
>>>>>>> 4de7016a54c469e0daa29849e0caab3515e0f0a0
import logging
from brain_strings import BRAIN_SIMPLE
from hbp_nrp_virtual_coach.virtual_coach import VirtualCoach
import numpy as np

<<<<<<< HEAD
logger = logging.getLogger(__name__)

sim.setup(timestep=0.1, min_delay=0.1, max_delay=20.0, threads=1, rng_seeds=[1234])

sensors = sim.Population({}, cellclass=sim.IF_curr_exp())
actors = sim.Population({}, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight={}))

circuit = sensors + actors'''


    def __init__(self):
        self.exp_name = 'cleanThrowing'
        self.sim = None
        self.vc = None
        self.simulation_finished = False
        self.distance = -1000000
        self.distanceSub = None
        self.simFinSub = None
        self.start_time = 0
        self.restart = False
        self.counter = 0
        try:
            self.vc = VirtualCoach(environment='local', storage_username='nrpuser')
        except:
            self.vc = None
 
    def kill(self):
        self.stopSim()
        sys.kill()
        
    def initialized(self):
        return self.vc != None

    def stopSim(self):
        try:
            self.simulation_finished = True
            self.sim.stop()
            time.sleep(2.0)
        except:
            pass


    def getDistance(self):
        return self.distance



    def getDistanceCallback(self):
        def distanceCallback(data):
            distance = data.data
            print("#################DISTANCE RECEIVED#################")
            print(data.data)
            if distance > self.distance:
                self.sim.pause()
                self.simulation_finished = True
                self.distance = distance
        return distanceCallback


    def getSimFinshedCallback(self):
        def simFinished(data):
            if(data.data == 1):
                self.counter = self.counter +1
                print("#################SIMULATION TIMEOUT#################",  self.counter)
                self.sim.pause()
                self.simulation_finished = True
        return simFinished
    
    def getReStartSimCallback(self):
        def restartSimCB(data):
            if (data.data == 1):
                print("INITIATE RESET")
                self.restart = True
                self.simulation_finished = True
        return restartSimCB

    def reset_variables(self):
        self.simulation_finished = False
        self.counter = 0
        self.distance = -1000000
        self.restart = False

    
    def run(self, weights):
        if not self.initialized():
            print("VC is not initialized")
            return
        
        self.reset_variables()

        #Launching the experiment
        print("launching")
        try:
            self.sim = self.vc.launch_experiment(self.exp_name)
        except:
            self.stopSim()
            time.sleep(2.0)
            return
        print("setting brain")
        #setting experiment
        brain = self.BRAIN_TEMPLATE.format(weights.shape[0], weights.shape[1], np.array2string(weights,separator=","))
        self.sim.edit_brain(brain)
        
        try:
            self.distanceSub = rospy.Subscriber("/cylinder_distance", Float32, self.getDistanceCallback(), queue_size=1)
            self.simFinSub = rospy.Subscriber("/sim_finished", Int32, self.getSimFinshedCallback(), queue_size=1)
            #self.restartTry = rospy.Subscriber("/start_sim_new", Int32, self.getReStartSimCallback(), queue_size=1)
            #maybe add transfer function here



        except:
            print('######Unable to set callback function, transfer function or brain')
            self.stopSim()
            time.sleep(2.0)
            return
=======
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
                self.sim = self.vc.launch_experiment('template_manipulation_0')
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
>>>>>>> 4de7016a54c469e0daa29849e0caab3515e0f0a0

            self.sim.start()
<<<<<<< HEAD
            self.start_time = time.time()
        except:
            print("Unable to start the simulation")
            self.stopSim()
            time.sleep(2.0)
            return
        
        # Wait until end of experiment and stop it
        while not self.simulation_finished:
            time.sleep(0.2)
        self.stopSim()
        elapsedTime = time.time() - self.start_time
        print(elapsedTime)
        time.sleep(3.0)
        if (not self.restart):
            if(self.distance > -100000):
                return self.distance
            else:
                return 0
        else:
            return None
=======
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
>>>>>>> 4de7016a54c469e0daa29849e0caab3515e0f0a0
