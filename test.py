import tensorflow as tf
import numpy as np

with tf.name_scope('input')as scope:
    X = tf.placeholder(tf.float32, [None, 784])
    Y = tf.placeholder(tf.float32, [None, 10])

with tf.variable_scope('layer1')as scope:
    print("layer1")

with tf.variable_scope('layer2')as scope:
    print("layer2")

with tf.variable_scope('layer3')as scope:
    print("layer3")

with tf.variable_scope('layer4')as scope:
    print("layer4")
