import sys
import time
import os
import logging
import datetime
import numpy as np
from path import Path
import json_tricks as json
import argparse
import csv

from simulation import ThrowingExperiment

#before running for the first time install json_tricks and path.py using following commands:
#cle-virtual-coach pip install json_tricks --user
#cle-virtual-coach pip install path.py --user

#experiments settings
WEIGHT_SHAPE = [2, 6]	
N_GENERATIONS = 40
POPULATION_SIZE = 10
LR_DECAY = 0.99
LR = 0.01
# WEIGHT_SCALE = 1.0




def main(pop_file = ''):
    ct = datetime.datetime.now()
    output_dir = Path(os.path.join("output","{}_{}_{}-{}_{}".format(ct.year, ct.month, ct.day, ct.hour, ct.minute)))
    bestDistances = []
    
    if not output_dir.exists():
        output_dir.makedirs()

    #initialize weights either random or from previous experiments
    #POPULATION_SIZE MIGHT INCREASE WHEN LOADING FROM FILE

    
        
    distance_file = os.path.join(output_dir,'distances_{}_{}.csv'.format(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]))

    experiment = ThrowingExperiment()
    sigma = 0.1 # noise standard deviation
    alpha = 0.001 # learning rate
    w = np.around(np.random.rand(WEIGHT_SHAPE[0],WEIGHT_SHAPE[1]), decimals=4)
    
    for current_gen in range(N_GENERATIONS):
        print("#################GENERATION -{}-#################".format(current_gen))


        N = np.around(np.random.randn(POPULATION_SIZE, WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]), decimals=3)
        R = np.zeros(POPULATION_SIZE)
        w_try = np.zeros((POPULATION_SIZE, WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]))
        for j in range(POPULATION_SIZE):
            w_try[j,] = np.around(w + sigma*N[j], decimals=4) # jitter w using gaussian of sigma 0.1

        #running Experiments for current generation
        current_population = experiment.run_experiment(w_try)

        #save current population and distance to json 
        population_file = os.path.join(output_dir, "{}_population.json".format(current_gen))
        print("\n{} generation finished. Best distance this genaration: {}".format(current_gen, current_population[0]["distance"]))

        #save best distances in csv file
        bestDistances.append(current_population[0]["distance"])
        with open(distance_file, 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(bestDistances)

        #save current_population to file
        with open(population_file, 'w') as f:
            json.dump(current_population, f, sort_keys=True, indent=4)

        #mutate populatioin and get new weights
        for i, p in enumerate(current_population):
            R[i] = -1000 - p['distance']
        
        A = (R - np.mean(R)) / np.std(R)
        N = N.reshape((POPULATION_SIZE, -1))
        w = w.reshape((-1))
        w = w + alpha/(POPULATION_SIZE*sigma) * np.dot(N.T, A)
        w = w.reshape((WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]))


if __name__ == '__main__':
    main()