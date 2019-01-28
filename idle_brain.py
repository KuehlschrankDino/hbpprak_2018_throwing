__author__ = 'Template'
from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np
import logging

logger = logging.getLogger(__name__)

sim.setup(timestep=0.1, min_delay=0.1, max_delay=20.0, threads=1, rng_seeds=[1234])

sensors = sim.Population(3, cellclass=sim.IF_curr_exp())
actors = sim.Population(4, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight=[[ 2.55891802,  3.1128487 ,  4.96337095,  2.1720421 ],
       [ 2.78477255,  0.13447206,  2.01123426,  0.08470332],
       [ 2.88209536,  3.32181436,  3.40667284,  0.47481324]]))

circuit = sensors + actors



