#-*- coding: utf-8 -*-
#pragma: no cover
__author__ = 'Template'
from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np
import logging

logger = logging.getLogger(__name__)

sim.setup(timestep=0.1, min_delay=0.1, max_delay=20.0, threads=1, rng_seeds=[1234])

sensors = sim.Population(3, cellclass=sim.IF_curr_exp())
actors = sim.Population(4, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight=[[ 2.68458825,  1.79860733,  2.13979478,  2.09815662],
       [ 1.22167809,  2.13534494,  0.52599432,  0.72355767],
       [ 1.13772255,  2.23725738,  3.21246595,  0.02056443]]))

circuit = sensors + actors


