import time
from simulation import ThrowingSim
import numpy as np
import os

def mutatePopulation(pop, keep= 3, lr = 0.5):
    new_weights = np.empty((len(pop), 3,3))
    for i, p in enumerate(pop):
        if(i < 3):
            new_weights[i, ] = pop[-1]['weights']
            for ii in range(3):
                x = np.random.randint(3)
                y = np.random.randint(3)
                new_weights[i,x,y] += np.power(-np.random.rand(0,1), np.random.randint(2)) 

        elif (i<5):
            new_weights[i, ] = pop[-2]
        else: 
            new_weights[i, ] = np.random.rand(3,3) * 5
    new_pop = []
    new_pop.append(pop[-1])
    new_pop.append(pop[-2])
    return new_weights, new_pop




def initPopulation(count=1, scale=5):
    # count (int): size of population
    # scale (float): upper bound for population values
    # return value (numpy array, shape=[count, 9])
    return np.random.rand(count, 3,3) * scale

def testPopulation(sim, weights):
    pop = []
    
    for i in range(weights.shape[0]):
        
        try:
            distance = abs(sim.run(weights[i]))
            # print("instance: {}, distance: {}".format(i, distance))

            pop.append({
            'weights': weights[i],
            'distance': distance
        })
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
    if(os.path.isfile("bestweights.npy") and os.path.isfile("distance.npy")):
        best_distance = float(np.load("distance.npy"))
        pop.append({
                'weights': np.load("bestweights.npy"),
                'distance': best_distance
            })
    weights = initPopulation(populationSize, 5)
    for i in range(num_generations):
        print("Starting generation {}".format(i))
        pop.extend(testPopulation(sim, weights))
        print(len(pop))
        pop.sort(key=key_func)
        if(best_distance < pop[-1]['distance']):
            np.save("bestweights.npy", pop[-1]['weights'])
            np.save("distance.npy", pop[-1]['distance'])
            best_distance = pop[-1]['distance']

        print(pop[0]['distance'])
        print(pop[-1]['distance'])
        weights, pop = mutatePopulation(pop)





if __name__ == '__main__':
    main()
