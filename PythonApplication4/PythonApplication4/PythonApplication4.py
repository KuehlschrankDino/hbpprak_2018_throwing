import time
import numpy as np
import os
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


WEIGHT_SHAPE = 2	
decay = 0.000
scale = 30

def mutate_population(pop, actual_generation, keep=3, lr=0.5):
    new_weights = np.empty((len(pop), WEIGHT_SHAPE))
    lr -= actual_generation * decay
    print("actual learning rate: {}".format(lr))
    for i, p in enumerate(pop):
        new_weights[i, ] = pop[-1]['weights']
        if(i < 4):
            for ii in range(3): 
                x = np.random.randint(WEIGHT_SHAPE)
                new_weights[i,x] += np.random.rand(1) * np.power(-1, np.random.randint(2)) * lr
        elif (i < 6):
            new_weights[i, ] = pop[-2]['weights']
            for ii in range(3): 
                x = np.random.randint(WEIGHT_SHAPE)
                new_weights[i,x] += np.random.rand(1) * np.power(-1, np.random.randint(2)) * lr 
        elif (i < 7): 
            new_weights[i, ] = np.random.rand(WEIGHT_SHAPE) * np.power(-1, np.random.randint(2)) * scale
    new_pop = []
    new_pop.append(pop[-1])
    new_pop.append(pop[-2])
    return new_weights, new_pop




def initPopulation(count=1, scale=30):
    # count (int): size of population
    # scale (float): upper bound for population values
    # return value (numpy array, shape=[count, 9])
    return np.random.rand(count, WEIGHT_SHAPE) * np.power(-1, np.random.randint(2)) * scale

def key_func(e):
    return e['distance']

def main():
    population_size = 8
    num_generations = 50
    best_distance = 0
    pop = []
    weights = initPopulation(population_size)
    distance_simulation = Distance_dummy()
    for i in range(num_generations):
        print("Starting generation {}".format(i))
        pop.extend(distance_simulation.test_population(weights))
        pop.sort(key=key_func)
        for single_pop in pop:
            print(single_pop['distance'])
        if(len(pop)>0):
            if(best_distance < pop[-1]['distance']):
                best_distance = pop[-1]['distance']
        print("top weights{}".format(pop[-1]['weights']))
        print("top distance{}".format(pop[-1]['distance']))
        weights, pop = mutate_population(pop, i)
        distance_simulation.set_best_weights(pop[-1])
    distance_simulation.plot_result()

class Distance_dummy():
    x, y, z = 0, 0, 0
    x_best_indices, y_best_indices, z_best_indices = [], [], []
    best_distances = []
    def __init__(self):
        self.x, self.y, self.z = axes3d.get_test_data(0.05)
        print("Maximum distance reachable for this simulation{}".format(np.max(self.z)))

    def test_population(self, weights):
        population = []
        for i in range(weights.shape[0]):
            distance = self.test_weightbatch(weights[i])
            population.append({
            'weights': weights[i],
            'distance': distance
            })
        return population
    
    def test_weightbatch(self, weightbatch):
        index_x, index_y, index_z = self.get_indices(weightbatch)
        return self.z[index_x, index_y]

    def get_indices(self, weightbatch):
        index_x, index_y, index_z = 0, 0, 0
        index_x = self.get_index(weightbatch, self.x, 0)
        index_y = self.get_index(weightbatch, self.y, 1)
        index_z = self.get_z_index(index_x, index_y)
        return index_x, index_y, index_z

    def get_index(self, weightbatch, array, column):
        index = 0
        lowest_distance = 1000
        for index_row, value in enumerate(array):
            if abs(value[index_row] - weightbatch[column]) < lowest_distance:
                lowest_distance = abs(value[index_row] - weightbatch[0])
                index = index_row
        return index

    def get_z_index(self, index_x, index_y):
        index_z = 0
        lowest_distance_x = 1000
        x_value = - 30 + index_x / 2
        for index, value_x  in enumerate(self.x[index_y]):
            if abs(value_x - x_value) < lowest_distance_x:
                index_z = index
                lowest_distance_x = abs(value_x - x_value)
        return index_z 

    def set_best_weights(self, best_pop):
        best_index_x, best_index_y, best_index_z= self.get_indices(best_pop['weights'])
        self.x_best_indices.append(best_index_x)
        self.y_best_indices.append(best_index_y)
        self.z_best_indices.append(best_index_z)
        self.best_distances.append(self.z[best_index_x, best_index_y])

    def plot_result(self):
        fig = plt.figure()  
        ax = fig.add_subplot(111, projection='3d')
        plt.plot(np.array(self.x[self.y_best_indices, self.z_best_indices]),
                np.array(self.y[self.x_best_indices, self.z_best_indices]),
                np.array(self.best_distances), 
                c = 'r', marker = 'o')
        ax.plot_wireframe(self.x, self.y, self.z, rstride=1, cstride=1)
        plt.show()
        
if __name__ == '__main__':
    main()
    
    
