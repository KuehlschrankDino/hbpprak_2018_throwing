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
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight=
               [
                [
                    3.254354531084235, 
                    2.821871741864256, 
                    1.7299023283903532, 
                    4.9458594329071675, 
                    0.5811545932799065, 
                    5.307165425891784, 
                    5.566587775154859
                ], 
                [
                    3.1393408789476225, 
                    0.6187526600761787, 
                    5.01248773058184, 
                    3.25303404320481, 
                    6.10778993683471, 
                    4.256664160183157, 
                    2.036593577691959
                ], 
                [
                    0.12967889143912484, 
                    5.259340343582439, 
                    6.38633485190746, 
                    5.287597624266169, 
                    3.046838843081032, 
                    2.7921440518558676, 
                    4.872705276245005
                ]
            ]))

circuit = sensors + actors