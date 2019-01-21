#-*- coding: utf-8 -*-
#pragma: no cover
__author__ = 'Template'
from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np
import logging

logger = logging.getLogger(__name__)

sim.setup(timestep=0.1, min_delay=0.1, max_delay=20.0, threads=1, rng_seeds=[1234])

sensors = sim.Population(3, cellclass=sim.IF_curr_exp())
actors = sim.Population(3, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight=[[ 3.79389373,  0.78820845,  0.00718699],
       [ 3.43632477,  1.06599468,  1.45794234],
       [ 4.34523834,  1.08499074,  3.17544349]]))

circuit = sensors + actors


