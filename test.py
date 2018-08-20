import tensorflow as tf
import numpy as np

learning_rate = 0.001
training_epochs = 15
batch_size = 100

input_data = input_data.read_data_sets("C:\Users\�輮ȯ\Documents\Mango\su.jpg", one_hot = True)

with tf.name_scope('input') as scope:
	X = tf.placeholder(tf.float32, [None, 784])
	y = tf.placeholder(tf.float32, [None, 10])

with tf.variable_scope('layer_1') as scope:
	layer_1_W = tf.Variable(tf.random_normal([784, 256], stddev = 0.01))
	layer_1_b = tf.Variable(tf.random_normal([256]))

	layer_1_L = tf.nn.relu(tf.add(tf.matmul(X, layer_1_W),layer_1_b))

with tf.variable_scope('input') as scope:
	input_W = tf.Variable(tf.random_normal([784, 784], stddev = 0.01))
	input_b = tf.Variable(tf.random_normal([784]))

	input_L = tf.nn.relu(tf.add(tf.matmul(X, input_W),input_b))