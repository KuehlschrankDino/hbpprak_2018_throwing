import time
import os
import logging
from simulation import ThrowingExperiment

import numpy as np
WEIGHT_SHAPE = [3, 4]	


def mutatePopulation(pop, lr=0.5):
    pass

def initPopulation(count=1, scale=5):
    global WEIGHT_SHAPE
    return np.random.rand(count, WEIGHT_SHAPE[0],WEIGHT_SHAPE[1]) * scale



def main():
    print("NEUROBOTICS PLATFORM IS SOOOOOO MUCH FUN!!! HOLY SHIT I REALLLY LIKE IT!!")
    weights = initPopulation(5)
    experiment = ThrowingExperiment()
    print(experiment.run_experiment(weights))
    


if __name__ == '__main__':
    main()