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

#before running for the first time install json_tricks and path.py with pip using following commands:
#cle-virtual-coach pip install json_tricks --user
#cle-virtual-coach pip install path.py --user

#experiments settings
WEIGHT_SHAPE = [3, 7]	
N_GENERATIONS = 100
POPULATION_SIZE = 8
LR_DECAY = 0.99
LR = 0.5

def mutatePopulation(pop):
    global LR
    new_weights = np.empty((len(pop), WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]))
    
    for i, p in enumerate(pop):
        new_weights[i, ] = pop[0]['weights']
        if(i < 3):
            for ii in range(3): 
                x = np.random.randint(WEIGHT_SHAPE[0])
                y = np.random.randint(WEIGHT_SHAPE[1])
                new_weights[i,x,y] += np.random.rand(1) * np.power(-1, np.random.randint(2)) * LR
        elif (i<5):
            new_weights[i, ] = pop[1]['weights']
            for ii in range(3): 
                x = np.random.randint(WEIGHT_SHAPE[0])
                y = np.random.randint(WEIGHT_SHAPE[1])
                new_weights[i,x,y] += np.random.rand(1) * np.power(-1, np.random.randint(2)) * LR 
        else: 
            new_weights[i, ] = np.random.rand(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]) * 5
    #todo: also return best instances but do not together with weights
    LR *= LR_DECAY
    return new_weights


def initPopulation(count=1, scale=5):
    return np.random.rand(count, WEIGHT_SHAPE[0],WEIGHT_SHAPE[1]) * scale


def load_population_from_json(json_file):
    global WEIGHT_SHAPE
    global POPULATION_SIZE
    with open(json_file, 'r') as f:
        loaded_population = json.load(f)
        w = loaded_population[0]["weights"]
        WEIGHT_SHAPE = w.shape
        POPULATION_SIZE = len(loaded_population)
    return loaded_population

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--pop_file',
                        help='file to population for initialization',
                        required = False,
                        type = str,
                        default="")
    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    print("NEUROBOTICS PLATFORM IS SOOOOOO MUCH FUN!!! HOLY SHIT I REALLLY LIKE IT!!")
    ct = datetime.datetime.now()
    output_dir = Path(os.path.join("output","{}_{}_{}-{}_{}".format(ct.year, ct.month, ct.day, ct.hour, ct.minute)))
    bestDistances = []
    
    
    if not output_dir.exists():
        output_dir.makedirs()

    #initialize weights either random or from previous experiments
    if(os.path.isfile(args.pop_file)):
        current_population = load_population_from_json(args.pop_file)
        weights = mutatePopulation(current_population)
    else:
        weights = initPopulation(POPULATION_SIZE)
 
    #initialize Experiment
    experiment = ThrowingExperiment()

    for current_gen in range(N_GENERATIONS):
        print("#################GENERATION -{}-#################".format(current_gen))

        #running Experiments for current generation
        current_population = experiment.run_experiment(weights)

        #save current population and distance to json 
        population_file = os.path.join(output_dir, "{}_population.json".format(current_gen))
        print("\n{} generation finished. Best distance this genaration: {}".format(current_gen, current_population[0]["distance"]))
        #save best distances in csv file
        bestDistances.append(current_population[0]["distance"])
        with open('distances_{}_{}'.format(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]), 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(bestDistances)
        #save current_population to file
        with open(population_file, 'w') as f:
            json.dump(current_population, f, sort_keys=True, indent=4)
        weights = mutatePopulation(current_population)
        
        
        


if __name__ == '__main__':
    main()