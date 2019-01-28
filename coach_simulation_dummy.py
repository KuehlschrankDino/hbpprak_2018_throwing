import time
import numpy as np
import os
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


WEIGHT_SHAPE = 2	
decay = 0.001
act_generation = 0

def mutate_population(pop, keep=3, lr=0.5):
    new_weights = np.empty((len(pop), WEIGHT_SHAPE))
	
    lr -= act_generation * decay
    print("actual learning rate: {}".format(lr))
    for i, p in enumerate(pop):
        new_weights[i, ] = pop[-1]['weights']
        if(i < 4):
            for ii in range(3): 
                x = np.random.randint(WEIGHT_SHAPE)
                new_weights[i,x] += np.power(-np.random.rand(1), np.random.randint(2))[0] * lr
        elif (i < 6):
            new_weights[i, ] = pop[-2]['weights']
            for ii in range(3): 
                x = np.random.randint(WEIGHT_SHAPE)
                new_weights[i,x] += np.power(-np.random.rand(1), np.random.randint(2))[0] * lr 
                
        else: 
            new_weights[i, ] = np.random.rand(WEIGHT_SHAPE) * 5
    new_pop = []
    new_pop.append(pop[-1])
    new_pop.append(pop[-2])
    print(new_weights)
    return new_weights, new_pop




def initPopulation(count=1, scale=5):
    # count (int): size of population
    # scale (float): upper bound for population values
    # return value (numpy array, shape=[count, 9])
    return np.random.rand(count, WEIGHT_SHAPE) * scale

def key_func(e):
    print(e['distance'])
    return e['distance']

def main():
    population_size = 8
    num_generations = 5
    best_distance = 0
    pop = []
    weights = initPopulation(population_size)
    distance_simulation = Distance_dummy()
    for i in range(num_generations):
        act_generation = i;
        print("Starting generation {}".format(i))
        pop.extend(distance_simulation.test_population(weights))
        print(len(pop))
        pop.sort(key=key_func)
        if(len(pop)>0):
            if(best_distance < pop[-1]['distance']):
                np.save("bestweights.npy", pop[-1]['weights'])
                np.save("distance.npy", pop[-1]['distance'])
                best_distance = pop[-1]['distance']

        print(pop[0]['distance'])
        print(pop[-1]['distance'])
        weights, pop = mutate_population(pop)
        
class Distance_dummy():
    x, y, z = 0, 0, 0

    def __init__(self):
        self.x, self.y, self.z = axes3d.get_test_data(0.05)
        self.plot_result()
    def test_population(self, weights):
        population = []

        for i in range(weights.shape[0]):
            distance = None
            while distance is None:
                distance = self.test_weightbatch(weights[i])
                            
            population.append({
            'weights': weights[i],
            'distance': distance
            })
        return population
    
    def test_weightbatch(self, weightbatch):
        index_x, index_y = 0, 0
        lowest_distance_x, lowest_distance_y = 1000, 1000
        for index_row, value in enumerate(self.x):
            if value[index_row] - weightbatch[0] < lowest_distance_x:
                lowest_distance_x = value[index_row] - weightbatch[0]
                index_x = index_row
        for index_col, value in enumerate(self.y):
            if value[index_col] - weightbatch[1] < lowest_distance_y:
                lowest_distance_x = value[index_col] - weightbatch[0]
                index_y = index_col
        return self.z[index_x, index_y]

    def plot_result(self):
        fig = plt.figure()  
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_wireframe(self.x, self.y, self.z, rstride=1, cstride=1)
        plt.show()
        
    '''   
    def get_test_data(self, delta=0.05):
        from matplotlib.mlab import bivariate_normal
        x = y = np.arange(-5.0, 5.0, delta)
        X, Y = np.meshgrid(x,y)
        
        Z1 = bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
        Z2 = bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
        Z = Z2 - Z1
        
        X = X * 1
        Y = Y * 1
        Z = Z * 100
        return X, Y, Z
   '''	

if __name__ == '__main__':
    main()
