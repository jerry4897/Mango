import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

learning_rate = 0.001
training_epochs = 30
batch_size = 100
from tensorflow.examples.tutorials.mnist import input_data

input_data = input_data.read_data_sets("./mnist.data/", one_hot = True)

with tf.name_scope('input') as scope:
	X = tf.placeholder(tf.float32, [None, 784])
	y = tf.placeholder(tf.float32, [None, 10])

with tf.variable_scope('layer_1') as scope:
	layer_1_W = tf.Variable(tf.random_normal([784, 256], stddev = 0.01))
	layer_1_b = tf.Variable(tf.random_normal([256]))
	layer_1_L = tf.nn.relu(tf.add(tf.matmul(X, layer_1_W),layer_1_b))

with tf.variable_scope('layer_2') as scope:
	layer_2_W = tf.Variable(tf.random_normal([256, 128], stddev = 0.01))
	layer_2_b = tf.Variable(tf.random_normal([128]))
	layer_2_L = tf.nn.relu(tf.add(tf.matmul(layer_1_L, layer_2_W),layer_2_b))

with tf.variable_scope('output') as scope:
	output_W = tf.Variable(tf.random_normal([128, 10], stddev = 0.01))
	output_b = tf.Variable(tf.random_normal([10]))
	model = (tf.add(tf.matmul(layer_2_L, output_W),output_b))

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)
display_step = 3

# initialize variables
init = tf.global_variables_initializer()

# run model
sess = tf.Session()
sess.run(init)
total_batch = int(input_data.train.num_examples/batch_size)
# training cycle
for epoch in range(training_epochs):
	avg_cost = 0.
	# loop over all batches
	for batch in range(total_batch):
		batch_x, batch_y = input_data.train.next_batch(batch_size)
		# run optimization (backprop) and cost (to calculate loss)
		_, cost = sess.run([optimizer, loss], feed_dict={X: batch_x, y: batch_y})
		# compute average loss
		avg_cost += cost / total_batch
	# display logs per epoch step
	if epoch % display_step == 0:
		print("epoch:", '%04d' % (epoch+1), "cost={:.9f}".format(avg_cost))
print("optimization finished!")

# test model
prediction = tf.nn.softmax(model)
correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
# calculate accuracy
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print("accuracy:", sess.run(accuracy, feed_dict={X: input_data.test.images, y: input_data.test.labels}))

labels = sess.run(model, feed_dict={X:input_data.test.images,y:input_data.test.labels})
fig = plt.figure()
for i in range(10):
	subplot = fig.add_subplot(2, 5, i + 1)
	subplot.set_xticks([])
	subplot.set_yticks([])
	subplot.set_title('%d' % np.argmax(labels[i]))
	subplot.imshow(input_data.test.images[i].reshape((28, 28)), cmap = plt.cm.gray_r)
plt.show()