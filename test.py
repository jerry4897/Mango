import tensorflow as tf
import numpy as np

with tf.name_scope('input')as scope:
    X = tf.placeholder(tf.float32, [None, 784])
    Y = tf.placeholder(tf.float32, [None, 10])
with tf.variable_scope('one')as scope:
    print("one")
with tf.variable_scope('two')as scope:
    print("two")
with tf.variable_scope('three')as scope:
    print("three")