#-*- coding: utf-8 -*-
#pragma: no cover
__author__ = 'Template'
from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np
import logging

logger = logging.getLogger(__name__)

sim.setup(timestep=0.1, min_delay=0.1, max_delay=20.0, threads=1, rng_seeds=[1234])

<<<<<<< Updated upstream
sensors = sim.Population(3, cellclass=sim.IF_curr_exp())
actors = sim.Population(4, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight=[
                [
                    4.0990892076512475, 
                    2.168762054277453, 
                    1.3051158238409317, 
                    4.447377345815192
                ], 
                [
                    1.371942370843562, 
                    3.739192062317888, 
                    1.817521394837223, 
                    0.18815221813527705
                ], 
                [
                    2.012561639682582, 
                    1.4921141940864489, 
                    4.193936264989586, 
                    5.7395397791408636
=======
sensors = sim.Population(2, cellclass=sim.IF_curr_exp())
actors = sim.Population(6, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight=[
                [
                    0.55990, 
                    0.2916, 
                    0.539900, 
                    0.4464, 
                    0.6029, 
                    0.193
                ], 
                [
                    0.338, 
                    0.5223, 
                    0.6888000000000001, 
                    0.5495, 
                    0.5439999999999999, 
                    0.5014
>>>>>>> Stashed changes
                ]
            ]))

circuit = sensors + actors




