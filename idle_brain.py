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
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight=[[ 4.11461461,  2.41755365,  1.01574498,  2.65863267],
       [ 0.54659679,  0.69951996,  4.73606566,  1.7634229 ],
       [ 3.64337662,  1.2035121 ,  2.13919966,  0.13242723]]))

circuit = sensors + actors


