import time
from simulation import ThrowingSim
import numpy as np
import os

<<<<<<< HEAD
WEIGHT_SHAPE = [4, 4]
=======
WEIGHT_SHAPE = [3, 4]
>>>>>>> 4de7016a54c469e0daa29849e0caab3515e0f0a0
distance_file = "distance_{}_{}.npy.".format(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1])
weights_file = "weights_{}_{}.npy".format(WEIGHT_SHAPE[0], WEIGHT_SHAPE[1])

def mutatePopulation(pop, keep= 3, lr = 0.5):
    new_weights = np.empty((len(pop), WEIGHT_SHAPE[0], WEIGHT_SHAPE[0]))
    for i, p in enumerate(pop):
        new_weights[i, ] = p['weights']
        if(i < 3):
            for ii in range(3): #todo: maybe adjust amount of weights to be changed to WEIGHT_SHAPE
                x = np.random.randint(WEIGHT_SHAPE[0])
                y = np.random.randint(WEIGHT_SHAPE[1])
                if (i < 2 ):
                    new_weights[i, ] = p['weights'][x,y] +  (pop[-1]['weights'][x,y] - p['weights'][x,y]) * lr
                else:
                    new_weights[i, ] = p['weights'][x,y] + ( pop[-2]['weights'][x,y] - p['weights'][x,y]) * lr
        else: 
            new_weights[i, ] = np.random.rand(WEIGHT_SHAPE[0],WEIGHT_SHAPE[1]) * 5
    new_pop = []
    new_pop.append(pop[-1])
    new_pop.append(pop[-2])
    return new_weights, new_pop




def initPopulation(count=1, scale=5):
    # count (int): size of population
    # scale (float): upper bound for population values
    # return value (numpy array, shape=[count, 9])
    return np.random.rand(count, WEIGHT_SHAPE[0],WEIGHT_SHAPE[1]) * scale

def testPopulation(sim, weights):
    pop = []
    
    for i in range(weights.shape[0]):
        distance = None
        while distance is None:
            print("jajajajajajja")
            distance = sim.run(weights[i])
            if(distance is None):
                print("#################################RESTARTING SIM!!")
            else:
                distance = abs(distance)
            
        pop.append({
        'weights': weights[i],
        'distance': distance
        })
        try:
            pass

        except:
            sim.stopSim()

    return pop

def key_func(e):
    print(e['distance'])
    return e['distance']

def main():
    sim = ThrowingSim()
    print(sim.initialized())
    populationSize = 8
    num_generations = 5
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
        print("Starting generation {}".format(i))
        pop.extend(testPopulation(sim, weights))
        print(len(pop))
        pop.sort(key=key_func)
        if(len(pop)>0):
            if(best_distance < pop[-1]['distance']):
                np.save("bestweights.npy", pop[-1]['weights'])
                np.save("distance.npy", pop[-1]['distance'])
                best_distance = pop[-1]['distance']

        print(pop[0]['distance'])
        print(pop[-1]['distance'])
        weights, pop = mutatePopulation(pop)





if __name__ == '__main__':
    main()
