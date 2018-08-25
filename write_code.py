from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import main

class write_input_box_process():
    def __init__(self, window, name, size, num_classes, data, learning_rate, training_epochs, batch_size):
        window.dock1.plaintext.append("\nlearning_rate = " + learning_rate + 
                                     "\ntraining_epochs = " + training_epochs +
                                     "\nbatch_size = " + batch_size)
        window.dock1.plaintext.append("from tensorflow.examples.tutorials.mnist import input_data")                    
        #window.dock1.plaintext.append("\ninput_data = input_data.read_data_sets(\""
        #                              + data + "\", one_hot = True)")
        window.dock1.plaintext.append("\ninput_data = input_data.read_data_sets(\"./mnist.data/\", one_hot = True)")
        window.dock1.plaintext.append("\nwith tf.name_scope('" + name + "') as scope:"
                                    + "\n\tX = tf.placeholder(tf.float32, [None, " + size + "])"
                                    + "\n\ty = tf.placeholder(tf.float32, [None, " + num_classes + "])")

class write_layer_process():
    def __init__(self, window, from_name, from_size, to_name, to_size, activation_function):
        window.dock1.plaintext.append("\nwith tf.variable_scope('" + to_name + "') as scope:"
                                    + "\n\t" + to_name + "_W = tf.Variable(tf.random_normal([" + str(from_size) + ", " + str(to_size) + "], stddev = 0.01))"
                                    + "\n\t" + to_name + "_b = tf.Variable(tf.random_normal([" + str(to_size) + "]))")
        if from_name == "input":
            window.dock1.plaintext.append("\t" + to_name + "_L = tf.nn." + activation_function + "(tf.add(tf.matmul(" + "X, " + to_name + "_W)," + to_name + "_b))")
        elif to_name == "output":
            window.dock1.plaintext.append("\tmodel = (tf.add(tf.matmul(" + from_name + "_L, " + to_name + "_W)," + to_name + "_b))")
        else:
            window.dock1.plaintext.append("\t" + to_name + "_L = tf.nn." + activation_function + "(tf.add(tf.matmul(" + from_name + "_L, " + to_name + "_W)," + to_name + "_b))")
            

class write_output_box_process():
    def __init__(self, window, name, size, loss_function, optimizer, display_step):
        window.dock1.plaintext.append("\nloss = tf.reduce_mean(tf.nn."+loss_function+"(logits=model, labels=y))") # need to generalize/expand
        window.dock1.plaintext.append("optimizer = tf.train."+optimizer+"(learning_rate=learning_rate).minimize(loss)")
        window.dock1.plaintext.append("display_step = " + str(display_step))

        window.dock1.plaintext.append("\n# initialize variables")
        window.dock1.plaintext.append("init = tf.global_variables_initializer()\n")

        window.dock1.plaintext.append("# run model")
        #window.dock1.plaintext.append("with tf.Session() as sess:\n\tsess.run(init)\n")
        window.dock1.plaintext.append("sess = tf.Session()\nsess.run(init)")
        window.dock1.plaintext.append("total_batch = int(input_data.train.num_examples/batch_size)") # need to generalize/expand

        window.dock1.plaintext.append("# training cycle")
        window.dock1.plaintext.append("for epoch in range(training_epochs):")
        window.dock1.plaintext.append("\tavg_cost = 0.")
        
        window.dock1.plaintext.append("\t# loop over all batches")
        window.dock1.plaintext.append("\tfor batch in range(total_batch):")
        window.dock1.plaintext.append("\t\tbatch_x, batch_y = input_data.train.next_batch(batch_size)")
        window.dock1.plaintext.append("\t\t# run optimization (backprop) and cost (to calculate loss)")
        window.dock1.plaintext.append("\t\t_, cost = sess.run([optimizer, loss], feed_dict={X: batch_x, y: batch_y})")
        window.dock1.plaintext.append("\t\t# compute average loss")
        window.dock1.plaintext.append("\t\tavg_cost += cost / total_batch")
        window.dock1.plaintext.append("\t# display logs per epoch step")
        window.dock1.plaintext.append("\tif epoch % display_step == 0:")
        window.dock1.plaintext.append("\t\tprint(\"epoch:\", '%04d' % (epoch+1), \"cost={:.9f}\".format(avg_cost))")
        window.dock1.plaintext.append("print(\"optimization finished!\")\n")
        window.dock1.plaintext.append("# test model")
        window.dock1.plaintext.append("prediction = tf.nn.softmax(model)") # apply softmax to model"
        window.dock1.plaintext.append("correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))")
        window.dock1.plaintext.append("# calculate accuracy")
        window.dock1.plaintext.append("accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))")
        window.dock1.plaintext.append("print(\"accuracy:\", sess.run(accuracy, feed_dict={X: input_data.test.images, y: input_data.test.labels}))")

        window.dock1.plaintext.append("\nlabels = sess.run(model, feed_dict={X:input_data.test.images,y:input_data.test.labels})")
        window.dock1.plaintext.append("fig = plt.figure()")
        window.dock1.plaintext.append("for i in range(10):"
                                    + "\n\tsubplot = fig.add_subplot(2, 5, i + 1)"
                                    + "\n\tsubplot.set_xticks([])"
                                    + "\n\tsubplot.set_yticks([])"
                                    + "\n\tsubplot.set_title('%d' % np.argmax(labels[i]))"
                                    + "\n\tsubplot.imshow(input_data.test.images[i].reshape((28, 28)), cmap = plt.cm.gray_r)")
        window.dock1.plaintext.append("plt.show()")

'''
        window.dock1.plaintext.append("import matplotlib as mp\n%matplotlib inline\nimport matplotlib.pyplot as plt\nimport math")
        window.dock1.plaintext.append("def getActivations(layer,stimuli):")
        window.dock1.plaintext.append("\tunits = sess.run(layer,feed_dict={x:np.reshape(stimuli,[1,784],order='F'),keep_prob:1.0})")
        window.dock1.plaintext.append("\tplotNNFilter(units)")

        window.dock1.plaintext.append("def plotNNFilter(units):"
                                    + "\n\tfilters = units.shape[3]"
                                    + "\n\tplt.figure(1, figsize=(20,20))"
                                    + "\n\tn_columns = 6"
                                    + "\n\tn_rows = math.ceil(filters / n_columns) + 1"
                                    + "\n\tfor i in range(filters):"
                                    + "\n\t\tplt.subplot(n_rows, n_columns, i+1)"
                                    + "\n\t\tplt.title('Filter ' + str(i))"
                                    + "\n\t\tplt.imshow(units[0,:,:,i], interpolation=\"nearest\", cmap=\"gray\")")

        window.dock1.plaintext.append("getActivations(layer_1_L,imageToUse)") 
'''

class cnn_process():
    def __init__(self, window):
        window.dock1.plaintext.append("import math\nimport tensorflow.contrib.slim as slim\n")
        window.dock1.plaintext.append("from tensorflow.examples.tutorials.mnist import input_data")                    
        window.dock1.plaintext.append("\ninput_data = input_data.read_data_sets(\"./mnist.data/\", one_hot = True)")
        
        window.dock1.plaintext.append("tf.reset_default_graph()\n"
                                     + "x = tf.placeholder(tf.float32, [None, 784],name=\"x-in\")\n"
                                     + "true_y = tf.placeholder(tf.float32, [None, 10],name=\"y-in\")\n"
                                     + "keep_prob = tf.placeholder(\"float\")\n"

                                     + "\nx_image = tf.reshape(x,[-1,28,28,1])\n"
                                     + "hidden_1 = slim.conv2d(x_image,5,[5,5])\n"
                                     + "pool_1 = slim.max_pool2d(hidden_1,[2,2])\n"
                                     + "hidden_2 = slim.conv2d(pool_1,5,[5,5])\n"
                                     + "pool_2 = slim.max_pool2d(hidden_2,[2,2])\n"
                                     + "hidden_3 = slim.conv2d(pool_2,20,[5,5])\n"
                                     + "hidden_3 = slim.dropout(hidden_3,keep_prob)\n"
                                     + "out_y = slim.fully_connected(slim.flatten(hidden_3),10,activation_fn=tf.nn.softmax)\n"

                                     + "\ncross_entropy = -tf.reduce_sum(true_y*tf.log(out_y))\n"
                                     + "correct_prediction = tf.equal(tf.argmax(out_y,1), tf.argmax(true_y,1))\n"
                                     + "accuracy = tf.reduce_mean(tf.cast(correct_prediction, \"float\"))\n"
                                     + "train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)\n\n")
        
        window.dock1.plaintext.append("batchSize = 50\n"
                                    + "sess = tf.Session()\n"
                                    + "init = tf.global_variables_initializer()\n"
                                    + "sess.run(init)\n"
                                    + "for i in range(1001):\n"
                                    + "\tbatch = input_data.train.next_batch(batchSize)\n"
                                    + "\tsess.run(train_step, feed_dict={x:batch[0],true_y:batch[1], keep_prob:0.5})\n"
                                    + "\tif i % 100 == 0 and i != 0:\n"
                                    + "\t\ttrainAccuracy = sess.run(accuracy, feed_dict={x:batch[0],true_y:batch[1], keep_prob:1.0})\n"
                                    + "\t\tprint(\"step %d, training accuracy %g\"%(i, trainAccuracy))\n")

        window.dock1.plaintext.append("testAccuracy = sess.run(accuracy, feed_dict={x:input_data.test.images,true_y:input_data.test.labels, keep_prob:1.0})"
                                    + "\nprint(\"test accuracy %g\"%(testAccuracy))")
        
        window.dock1.plaintext.append("def getActivations(layer,stimuli):\n"
                                    + "\tunits = sess.run(layer,feed_dict={x:np.reshape(stimuli,[1,784],order='F'),keep_prob:1.0})\n"
                                    + "\tplotNNFilter(units)\n")
        window.dock1.plaintext.append("def plotNNFilter(units):\n"
                                    + "\tfilters = units.shape[3]\n"
                                    + "\tplt.figure(1, figsize=(20,20))\n"
                                    + "\tn_columns = 6\n"
                                    + "\tn_rows = math.ceil(filters / n_columns) + 1\n"
                                    + "\tfor i in range(filters):\n"
                                    + "\t\tplt.subplot(n_rows, n_columns, i+1)\n"
                                    + "\t\tplt.title('Filter ' + str(i))\n"
                                    + "\t\tplt.imshow(units[0,:,:,i], interpolation=\"nearest\", cmap=\"gray\")\n")

        window.dock1.plaintext.append("imageToUse = input_data.test.images[0]\n"
                                    + "plt.imshow(np.reshape(imageToUse,[28,28]), interpolation=\"nearest\", cmap=\"gray\")\n")
                        