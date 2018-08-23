import cv2
import numpy as np
import tensorflow as tf
from scipy.stats import bernoulli
import cython # optional (for speed)
from tensorflow.examples.tutorials.mnist import input_data

#%%cython -a # optional (for speed)

def intensity2spike_train(dataset, stimulus_epoch):
    image = cv2.imread(filename.decode(), cv2.IMREAD_GRAYSCALE)
    height, width = image.shape[0], image.shape[1]
    spike_train = np.zeros((height, width, stimulus_epoch))

    for y in range(0, height):
        for x in range(0, width):
            spike_train[y][x] = bernoulli.rvs((image[height, width]/255)*np.ones((stimulus_epoch)))

    return spike_train

input_data = input_data.read_data_sets("./mnist.data/", one_hot = True)
input_data = input_data.map(tf.py_func(map_func=intensity2spike_train))
def simulate(self, input_data, duration=1.0, max_rate=200, dt=0.001, threshold=0.5):
        # Reset layer arrays
    for l in range(len(self.weights)):
        self.potential[l] = np.zeros(self.weights[l].shape[1])
        self.spikes[l] = np.zeros((self.weights[l].shape[0]), dtype=bool)
        self.spike_stats[l] = np.zeros((self.weights[l].shape[0]), dtype=int)
    self.spikes[-1] = np.zeros((self.weights[-1].shape[1]), dtype=bool)
    self.spike_stats[-1] = np.zeros((self.weights[-1].shape[1]), dtype=int)
        
    for t in range(int(duration/dt)):
            
        # Create poisson distributed spikes from input
        rescale_fac = 1/(dt*max_rate)
        spike_snapshot = np.random.uniform(size=input_data.shape) * rescale_fac
        input_spikes = spike_snapshot <= input_data
        self.spikes[0] = input_spikes
        self.spike_stats[0] += input_spikes
            
        for l in range(len(self.weights)):
            # Get input impulse from incoming spikes
            impulse = np.dot(self.weights[l].T, self.spikes[l])
            # Add bias impulse
            if self.bias[l] is not None:
                impulse += self.bias[l]/rescale_fac
            # Add input to membrane potential
            self.potential[l] += impulse
            self.potential[l] *= self.potential[l] > 0
            # Check for spiking
            self.spikes[l+1] = self.potential[l] >= threshold
            self.spike_stats[l+1] += self.spikes[l+1]
            # Reset
            self.potential[l][self.spikes[l+1]] = 0
        
    return self.spike_stats