#-*- coding: utf-8 -*-
#pragma: no cover
__author__ = 'Template'
from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np
import logging

logger = logging.getLogger(__name__)

sim.setup(timestep=0.1, min_delay=0.1, max_delay=20.0, threads=1, rng_seeds=[1234])

sensors = sim.Population(3, cellclass=sim.IF_curr_exp())
actors = sim.Population(6, cellclass=sim.IF_curr_exp())
sim.Projection(sensors, actors, sim.AllToAllConnector(), sim.StaticSynapse(weight=[
                [
                    0.0848322543454469, 
                    0.13531403228987351, 
                    0.815631575154865, 
                    -0.04622728308937002, 
                    0.44432011337618926, 
                    1.0386710391218974
                ], 
                [
                    0.7664867303783535, 
                    0.5340259758024044, 
                    0.3173829966883909, 
                    -0.02019334638721558, 
                    -0.1856238493825683, 
                    0.9144599185879352
                ], 
                [
                    0.7193285672582143, 
                    0.2449785419152155, 
                    0.2214651189818882, 
                    0.7643675334659238, 
                    0.33214627948158076, 
                    0.715196052556546
                ]
            ]))

circuit = sensors + actors




