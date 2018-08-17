import tensorflow as tf
import numpy as np

with tf.name_scope('input')as scope:
    X = tf.placeholder(tf.float32, [None, 784])
    Y = tf.placeholder(tf.float32, [None, 10])

with tf.variable_scope('1')as scope:
    print("1")

with tf.variable_scope('2')as scope:
    print("2")

with tf.variable_scope('3')as scope:
    print("3")

with tf.variable_scope('4')as scope:
    print("4")
