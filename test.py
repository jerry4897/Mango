import tensorflow as tf
import numpy as np

# construct model
model = general_model(X)

# store layers' weights and biases
weights = []; biases = []
weights.append(tf.Variable(tf.random_normal([784, 128])))
biases.append(tf.Variable(tf.random_normal([128])))
weights.append(tf.Variable(tf.random_normal([128, 10])))
biases.append(tf.Variable(tf.random_normal([10])))
# create model
def general_model(input):
	input = tf.add(tf.matmul(input, weights[0]), biases[0])
	layer_1 = tf.add(tf.matmul(input, weights[1]), biases[1])
	output = tf.matmul(input, weights[1]) + biases[1]
	return names[len(names)-1]

# construct model
model = general_model(X)

# define loss and optimizer
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train = optimizer.minimize(loss)

# initialize variables
init = tf.global_variables_initializer()

# run model
with tf.Session() as sess:
	sess.run(init)
    
    data = input_data.read_data_sets("C:\Users\김석환\MNIST_data", one_hot=True)
	# training cycle
	for epoch in range(training_epochs):
		avg_cost = 0.
		total_batch = int(data.train.num_examples/batch_size)
		# loop over all batches
		for batch in range(total_batch):
			batch_x, batch_y = data.train.next_batch(batch_size)
			# run optimization (backprop) and cost (to calculate loss)
			_, cost = sess.run([train, loss], feed_dict={X: batch_x, Y: batch_y})
			# compute average loss
			avg_cost += cost / total_batch
		# display logs per epoch step
		if epoch % display_step == 0:
			print("epoch:", '%04d' % (epoch+1), "cost={:.9f}".format(avg_cost))
	print("optimization finished!")

	# test model
	prediction = tf.nn.softmax(model) # apply softmax to model
	correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
	# calculate accuracy
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
	print("accuracy:", accuracy.eval({X: data.test.images, Y: data.test.labels}))