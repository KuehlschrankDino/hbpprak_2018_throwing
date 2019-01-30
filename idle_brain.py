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
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight=[[ 3.00731051,  2.9136005 ,  1.58271879,  2.49663017],
       [ 0.23435238,  3.60735157,  3.51980248,  3.84681013],
       [ 2.26153034,  4.61704958,  1.12518098,  3.28715384]]))

circuit = sensors + actors


