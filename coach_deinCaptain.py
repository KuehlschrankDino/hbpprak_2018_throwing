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
from sklearn.preprocessing import normalize


#before running for the first time install json_tricks and path.py with pip using following commands:
#cle-virtual-coach pip install json_tricks --user
#cle-virtual-coach pip install path.py --user

#experiments settings
WEIGHT_SHAPE = [3, 7]	
N_GENERATIONS = 100
POPULATION_SIZE = 2
LR_DECAY = 0.7
LR = 1


def mutatePopulation(pop, local_max_counter,current_gen,weights_mapping):
    global LR
    new_weights_mapping= []
    if(len(pop)>50):
        pop = pop[:50]
    if(current_gen>0):
        new_weights = np.empty((len(pop)*2, WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]))
    else:
        new_weights = np.empty((len(pop), WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]))
   
    for i, p in enumerate(pop):
        new_weights[i, ] = pop[i]['weights']
        #if local_max_counter is high the propability to be in local maximum is high and weights are randomly reset
        if (local_max_counter == 10 and i < 10):
            new_weights[i,] = np.random.uniform(2,6,(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1])) 
            new_weights_mapping.append({
                    'newweights': new_weights[i],
                    'oldweights': [[0 for x in range(WEIGHT_SHAPE[1] )] for y in range(WEIGHT_SHAPE[0])],
                    'distance': 0
                    })
        elif(i < 10):
            for ii in range(3): 
                x = np.random.randint(WEIGHT_SHAPE[0])
                y = np.random.randint(WEIGHT_SHAPE[1])
                new_weights[i,x,y] += np.random.rand(1) * np.power(-1, np.random.randint(2)) * LR
                new_weights_mapping.append({
                    'newweights': new_weights[i],
                    'oldweights': pop[i]['weights'],
                    'distance': pop[i]['distance']
                    })
        elif(i < 18 ):
            value = np.random.randint(len(pop))
            new_weights[i, ]= pop[value]['weights']+ np.random.uniform(2, 6, (WEIGHT_SHAPE[0], WEIGHT_SHAPE[1])) * LR
            new_weights_mapping.append({
                    'newweights': new_weights[i],
                    'oldweights': pop[value]['weights'],
                    'distance': pop[value]['distance']
                    })
        else: 
            new_weights[i, ] = np.random.uniform(2,6,(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1])) 
            new_weights_mapping.append({
                    'newweights': new_weights[i],
                    'oldweights': [[0 for x in range(WEIGHT_SHAPE[1] )] for y in range(WEIGHT_SHAPE[0])],
                    'distance': 0
                    })
        
    
    if(current_gen> 0 and current_gen %10 == 0) :
        
        for i,p in enumerate(pop) :
            if(i< len(pop)/2):
                value = np.random.randint(WEIGHT_SHAPE[0])
                value2 = i
                new_weights[i+len(pop)][:value]= pop[-(i+1)]['weights'][:value]
                new_weights[i+len(pop)][value:]= pop[i]['weights'][value:]
            else :
                value2 = np.random.randint(len(pop))
                value3 = np.random.randint(len(pop))
                
                value = np.random.randint(WEIGHT_SHAPE[0])
                new_weights[i+len(pop)][:value]= pop[value2]['weights'][:value]
                new_weights[i+len(pop)][value:]= pop[value3]['weights'][value:]
            new_weights_mapping.append({
                    'newweights': new_weights[i+len(pop)],
                    'oldweights': pop[value2]['weights'] ,
                    'distance': pop[value2]['distance']
                    })
                
             
    elif(current_gen > 0):
        for i, p in enumerate(pop):
            old_weights = searchForOldWeights(weights_mapping, pop[i]['weights'])
            dif =pop[i]['weights']-old_weights['oldweights']
            norm_dif = normalize(dif, norm='l2')
            if(pop[i]['distance']>old_weights['distance']):
                new_weights[i+len(pop)] = pop[i]['weights']+norm_dif* LR
            else :
                new_weights[i+len(pop)] = old_weights['oldweights']-norm_dif* LR
            new_weights_mapping.append({
                'newweights': new_weights[i+len(pop)],
                'oldweights': pop[i]['weights'],
                'distance':pop[i]['distance']
                })
    
                    
                
    #todo: also return best instances but do not together with weights
    LR *= LR_DECAY
    
    return new_weights,new_weights_mapping

def searchForOldWeights(weights_mapping, new_weights):
    for i,p in enumerate(weights_mapping):
        if((new_weights==weights_mapping[i]['newweights']).all):
            return weights_mapping[i]
            
def initPopulation(count=1, scale=6):
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
    local_max_counter = 0
    best_distance = 0

    
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
    new_weights_mapping=[]
    for current_gen in range(N_GENERATIONS):
        print("#################GENERATION -{}-#################".format(current_gen))

        #running Experiments for current generation
        
        current_population = experiment.run_experiment(weights)
        if (current_population[0]['distance'] > best_distance):
            best_distance = current_population [0]['distance']
            local_max_counter = 0
        else:
            local_max_counter += 1
        #save current population and distance to json 
        population_file = os.path.join(output_dir, "{}_population.json".format(current_gen))
        print("\n{} generation finished. Best distance this genaration: {}".format(current_gen, current_population[0]["distance"]))
        print("overall best_distance: {}".format(best_distance))
        #save best distances in csv file
        bestDistances.append(best_distance)
        with open('distances_{}_{}'.format(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]), 'wb') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(bestDistances)
        #save current_population to file
        print("#################population -{}".format(current_population))
        with open(population_file, 'w') as f:
            json.dump(current_population, f, sort_keys=True, indent=4)
        
        weights, new_weights_mapping = mutatePopulation(current_population,local_max_counter,current_gen,new_weights_mapping)
        
        
        


if __name__ == '__main__':
    main()
