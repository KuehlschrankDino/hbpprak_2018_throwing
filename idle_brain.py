#-*- coding: utf-8 -*-
#pragma: no cover
__author__ = 'Template'
from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np
import logging

logger = logging.getLogger(__name__)

sim.setup(timestep=0.4, min_delay=0.4, max_delay=20.0, threads=1, rng_seeds=[1234])

sensors = sim.Population(3, cellclass=sim.IF_curr_exp())
actors = sim.Population(7, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight= [
                [
                    3.5893883795830943, 
                    3.247198458350082, 
                    1.8104187165805774, 
                    4.9717028751509345, 
                    0.28473963337491215, 
                    5.357209500054974, 
                    4.84808988443095
                ], 
                [
                    3.2708440877298557, 
                    0.4695065564288154, 
                    5.036586914339509, 
                    3.7752657649176116, 
                    5.850311105348753, 
                    4.109394994228576, 
                    2.4029178952145585
                ], 
                [
                    0.02181800414174151, 
                    5.657258339258725, 
                    6.169034167789124, 
                    5.119674371518959, 
                    2.866078295298095, 
                    2.3773351910158755, 
                    5.017313403039511
                ]
            ]))

circuit = sensors + actors