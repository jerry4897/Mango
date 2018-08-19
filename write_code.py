from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import main

class write_input_box_process():
    def __init__(self, window, names, sizes, num_classes, data, learning_rate, training_epochs, batch_size):
        if(names == "input"):
            window.dock1.plaintext.append("# store layers' weights and biases")
            window.dock1.plaintext.append("weights = []; biases = []")
            for layer in range(len(names)):
                window.dock1.plaintext.append("weights.append("+"tf.Variable(tf.random_normal(["+sizes[layer]+", "+ str(num_classes) +"])))")
                window.dock1.plaintext.append("biases.append(tf.Variable(tf.random_normal(["+ str(num_classes) +"])))\n")
        
            window.dock1.plaintext.append("# create model")
            window.dock1.plaintext.append("def general_model(input):")
            window.dock1.plaintext.append("\t"+names[0]+" = tf.add(tf.matmul(input, weights[0]), biases[0])\n")

        else:
            for layer in range(1, len(names)-1):
                window.dock1.plaintext.append("\t"+names[layer]+" = tf.add(tf.matmul(" + names[layer-1] + ", weights[" + str(layer) +  "]), biases[" + str(layer) + "])")
                window.dock1.plaintext.append("\t" + names[len(names)-1] + " = tf.matmul(" + names[layer-1] +", weights[" + str(layer) + "]) + biases[" + str(layer) + "]")
                window.dock1.plaintext.append("\t" + "return names[len(names)-1]\n")

class write_to_dock_code():
    def __init__(self, window, names, sizes, data, learning_rate, training_epochs, batch_size, loss, optimizer, display_step):
        window.dock1.plaintext.append("# construct model")
        window.dock1.plaintext.append("model = general_model(X)\n")
        window.dock1.plaintext.append("# store layers' weights and biases")
        window.dock1.plaintext.append("weights = []; biases = []")
        for layer in range(len(names)-1):
	        window.dock1.plaintext.append("weights.append("+"tf.Variable(tf.random_normal(["+sizes[layer]+", "+sizes[layer+1]+"])))")
	        window.dock1.plaintext.append("biases.append(tf.Variable(tf.random_normal(["+sizes[layer+1]+"])))")

        window.dock1.plaintext.append("# create model")
        window.dock1.plaintext.append("def general_model(input):")
        window.dock1.plaintext.append("\t"+names[0]+" = tf.add(tf.matmul(input, weights[0]), biases[0])")

        for layer in range(1, len(names)-1):
	        window.dock1.plaintext.append("\t"+names[layer]+" = tf.add(tf.matmul("+names[layer-1]+", weights["+ str(layer) +"]), biases["+ str(layer) +"])")
        window.dock1.plaintext.append("\t" + names[len(names)-1] + " = tf.matmul(" + names[layer-1] +", weights["+ str(layer) +"]) + biases["+ str(layer) +"]")
        window.dock1.plaintext.append("\t" + "return names[len(names)-1]\n")

        window.dock1.plaintext.append("# construct model")
        window.dock1.plaintext.append("model = general_model(X)\n")

        window.dock1.plaintext.append("# define loss and optimizer")
        window.dock1.plaintext.append("loss = tf.reduce_mean(tf.nn."+loss+"(logits=model, labels=Y))") # need to generalize/expand
        window.dock1.plaintext.append("optimizer = tf.train."+optimizer+"(learning_rate=learning_rate)")
        window.dock1.plaintext.append("train = optimizer.minimize(loss)\n")

        window.dock1.plaintext.append("# initialize variables")
        window.dock1.plaintext.append("init = tf.global_variables_initializer()\n")

        window.dock1.plaintext.append("# run model")
        window.dock1.plaintext.append("with tf.Session() as sess:\n\tsess.run(init)\n")
        window.dock1.plaintext.append("\tdata = input_data.read_data_sets(\"" + data + "\", one_hot=True)")
        window.dock1.plaintext.append("\t# training cycle")
        window.dock1.plaintext.append("\tfor epoch in range(training_epochs):")
        window.dock1.plaintext.append("\t\tavg_cost = 0.")
        window.dock1.plaintext.append("\t\ttotal_batch = int(data.train.num_examples/batch_size)") # need to generalize/expand
        window.dock1.plaintext.append("\t\t# loop over all batches")
        window.dock1.plaintext.append("\t\tfor batch in range(total_batch):")
        window.dock1.plaintext.append("\t\t\tbatch_x, batch_y = data.train.next_batch(batch_size)")
        window.dock1.plaintext.append("\t\t\t# run optimization (backprop) and cost (to calculate loss)")
        window.dock1.plaintext.append("\t\t\t_, cost = sess.run([train, loss], feed_dict={X: batch_x, Y: batch_y})")
        window.dock1.plaintext.append("\t\t\t# compute average loss")
        window.dock1.plaintext.append("\t\t\tavg_cost += cost / total_batch")
        window.dock1.plaintext.append("\t\t# display logs per epoch step")
        window.dock1.plaintext.append("\t\tif epoch % display_step == 0:")
        window.dock1.plaintext.append("\t\t\tprint(\"epoch:\", '%04d' % (epoch+1), \"cost={:.9f}\".format(avg_cost))")
        window.dock1.plaintext.append("\tprint(\"optimization finished!\")\n")
        window.dock1.plaintext.append("\t# test model")
        window.dock1.plaintext.append("\tprediction = tf.nn.softmax(model) # apply softmax to model")
        window.dock1.plaintext.append("\tcorrect_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))")
        window.dock1.plaintext.append("\t# calculate accuracy")
        window.dock1.plaintext.append("\taccuracy = tf.reduce_mean(tf.cast(correct_prediction, \"float\"))")
        window.dock1.plaintext.append("\tprint(\"accuracy:\", accuracy.eval({X: data.test.images, Y: data.test.labels}))")