import csv
import time
from simulation import ThrowingSim
import numpy as np
import os

WEIGHT_SHAPE = [3, 7]			
distance_file = "distance_{}_{}.npy.".format(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1])
weights_file = "weights_{}_{}.npy".format(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1])
decay = 0.002
act_generation = 0

def mutatePopulation(pop, keep=3, lr=1):
    new_weights = np.empty((len(pop), WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]))
	
    lr -= act_generation *  decay
    for i, p in enumerate(pop):
        new_weights[i, ] = pop[-1]['weights']
        if(i < 3):
            for ii in range(3): 
                x = np.random.randint(WEIGHT_SHAPE[0])
                y = np.random.randint(WEIGHT_SHAPE[1])
                new_weights[i,x,y] += np.random.rand(1) * np.power(-1, np.random.randint(2)) * lr
        elif (i<5):
            new_weights[i, ] = pop[-2]['weights']
            for ii in range(3): 
                x = np.random.randint(WEIGHT_SHAPE[0])
                y = np.random.randint(WEIGHT_SHAPE[1])
                new_weights[i,x,y] += np.random.rand(1) * np.power(-1, np.random.randint(2)) * lr 
        else: 
            new_weights[i, ] = np.random.rand(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]) * 5
    new_pop = []
    new_pop.append(pop[-1])
    new_pop.append(pop[-2])
    return new_weights, new_pop

def initPopulation(count=1, scale=5):
    population = np.random.rand(count, WEIGHT_SHAPE[0],WEIGHT_SHAPE[1]) * scale
    population[0,] = np.array([[ 0.49045169,  4.68628222,  0.80539149,  3.63458529, 2,2,2],
       [ 2.23115595,  4.51167628,  2.95645606,  4.53557952,2,2,2],
       [ 0.54636356,  0.27761012,  3.34335455,  3.76459593,2,2,2]])
    # count (int): size of population
    # scale (float): upper bound for population values
    # return value (numpy array, shape=[count, 9])
    #return np.random.rand(count, WEIGHT_SHAPE[0],WEIGHT_SHAPE[1]) * scale
    return population
    
def testPopulation(sim, weights):
    pop = []
    for i in range(weights.shape[0]):
        count = 0
        distance = None
        while distance is None and count < 3:
            print("start simulation..")
            distance = sim.run(weights[i])
            if(distance is None):
                print("#################################RESTARTING SIM!!")
                count = count + 1
            else:
                distance = abs(distance)
            
        pop.append({
        'weights': weights[i],
        'distance': distance
        })

    return pop

def key_func(e):
    print(e['distance'])
    return e['distance']

def main():
    sim = ThrowingSim()
    print(sim.initialized())
    best_distances = []
    populationSize = 20
    num_generations = 500
    best_distance = 0
    pop = []
    if(os.path.isfile(distance_file) and os.path.isfile(weights_file)):
        best_distance = float(np.load(distance_file))
        pop.append({
                'weights': np.load(weights_file),
                'distance': best_distance
            })
    weights = initPopulation(populationSize, 5)
    for i in range(num_generations):
        act_generation = i;
        print("Starting generation {}".format(i))
        pop.extend(testPopulation(sim, weights))
        print(len(pop))
        pop.sort(key=key_func)
        if(len(pop)>0):
            if(best_distance < pop[-1]['distance']):
                np.save(weights_file, pop[-1]['weights'])
                np.save("distance.npy", pop[-1]['distance'])
                best_distance = pop[-1]['distance']
        best_distances.append(pop[-1]['distance'])

        print(pop[0]['distance'])
        print(pop[-1]['distance'])
        weights, pop = mutatePopulation(pop)
        
        with open('distances_{}_{}'.format(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1]), 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(best_distances)
        




if __name__ == '__main__':
    main()
