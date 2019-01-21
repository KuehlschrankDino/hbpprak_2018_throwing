try:
    from hbp_nrp_virtual_coach.virtual_coach import VirtualCoach 
except ImportError as e:
    print(e)
    raise e
import time
import sys
import rospy
from std_msgs.msg import Float32, Int32
import numpy as np

def numpyArrayToInitStr(array):
    # array: 1- or 2-dimentional numpy array
    # return value: initialization string to create array
    if len(array.shape) == 1:
        string = '['
        for j in range(3):
            string += '['
            for i in range(3):
                string += str(array[j*3 + i]) + ','
            if string[-1] == ',':
                string = string[:-1]
            string += '],'
        if string[-1] == ',':
            string = string[:-1]
        string += ']'
        return string
    elif len(array.shape) == 2:
        string = '['
        for row in array:
            string += '['
            for element in row:
                string += str(element) + ','
            if string[-1] == ',':
                string = string[:-1]
            string += '],'
        if string[-1] == ',':
            string = string[:-1]
        string += ']'
        return string
    else:
        return ''

class ThrowingSim():
    BRAIN_TEMPLATE = '''#-*- coding: utf-8 -*-
#pragma: no cover
__author__ = 'Template'
from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np
import logging

logger = logging.getLogger(__name__)

sim.setup(timestep=0.1, min_delay=0.1, max_delay=20.0, threads=1, rng_seeds=[1234])

sensors = sim.Population(3, cellclass=sim.IF_curr_exp())
actors = sim.Population(3, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight={syn_weights}))

circuit = sensors + actors'''


    def __init__(self):
        self.exp_name = 'template_manipulation_0'
        self.sim = None
        self.vc = None
        self.simulation_finished = False
        self.distance = -1000000
        self.distanceSub = None
        self.simFinSub = None
        self.start_time = 0
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
    
    def run(self, weights):
        if not self.initialized():
            print("VC is not initialized")
            return
        self.simulation_finished = False
        self.counter = 0
        self.distance = -1000000
        #Launching the experiment
        try:
            self.sim = self.vc.launch_experiment(self.exp_name)
        except:
            self.stopSim()
            time.sleep(2.0)
            return
        
        #setting experiment
        brain = self.BRAIN_TEMPLATE.format(**{'syn_weights': numpyArrayToInitStr(weights)})
        self.sim.edit_brain(brain)
        
        try:
            # self.sim.register_status_callback(self.getStatusCallback())
            self.distanceSub = rospy.Subscriber("/cylinder_distance", Float32, self.getDistanceCallback(), queue_size=1)
            self.simFinSub = rospy.Subscriber("/sim_finished", Int32, self.getSimFinshedCallback(), queue_size=1)
            #maybe add transfer function here



        except:
            print('######Unable to set callback function, transfer function or brain')
            self.stopSim()
            time.sleep(2.0)
            return

        
        #running the experiment
        try:
            print("Trying to start the simulation.")
            self.sim.start()
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
        if(self.distance > -100000):
            return self.distance
        else:
            return 0

