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