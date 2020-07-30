from __future__ import print_function

import tensorflow as tf
import os, pathlib

from eval import eval
from data import BalanceCovidDataset

def train_tf(epochs, lr, bs, weightspath, 
                metaname, ckptname, trainfile, testfile, name, 
                datadir, covid_weight, covid_percent, input_size, 
                top_percent, in_tensorname, out_tensorname, 
                logit_tensorname, label_tensorname, weights_tensorname,
                input_data_dir, output_data_dir):
    # Parameters
    learning_rate = lr
    batch_size = bs
    display_step = 1

    # output path
    outputPath = output_data_dir
    runID = name + '-lr' + str(learning_rate)
    runPath = outputPath + runID
    pathlib.Path(runPath).mkdir(parents=True, exist_ok=True)
    print('Output: ' + runPath)

    with open(trainfile) as f:
        trainfiles = f.readlines()
    with open(testfile) as f:
        testfiles = f.readlines()

    generator = BalanceCovidDataset(data_dir=datadir,
                                    csv_file=trainfile,
                                    batch_size=batch_size,
                                    input_shape=(input_size, input_size),
                                    covid_percent=covid_percent,
                                    class_weights=[1., 1., covid_weight],
                                    top_percent=top_percent)

    with tf.Session() as sess:
        tf.get_default_graph()
        saver = tf.train.import_meta_graph(os.path.join(weightspath, metaname))

        graph = tf.get_default_graph()

        image_tensor = graph.get_tensor_by_name(in_tensorname)
        labels_tensor = graph.get_tensor_by_name(label_tensorname)
        sample_weights = graph.get_tensor_by_name(weights_tensorname)
        pred_tensor = graph.get_tensor_by_name(logit_tensorname)
        # loss expects unscaled logits since it performs a softmax on logits internally for efficiency

        # Define loss and optimizer
        loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(
            logits=pred_tensor, labels=labels_tensor)*sample_weights)
        optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
        train_op = optimizer.minimize(loss_op)

        # Initialize the variables
        init = tf.global_variables_initializer()

        # Run the initializer
        sess.run(init)

        # load weights
        saver.restore(sess, os.path.join(weightspath, ckptname))
        #saver.restore(sess, tf.train.latest_checkpoint(weightspath))

        # save base model
        saver.save(sess, os.path.join(runPath, 'model'))
        print('Saved baseline checkpoint')
        print('Baseline eval:')
        eval(sess, graph, testfiles, os.path.join(datadir,'test'),
             in_tensorname, out_tensorname, input_size)

        # Training cycle
        print('Training started')
        total_batch = len(generator)
        progbar = tf.keras.utils.Progbar(total_batch)
        for epoch in range(epochs):
            for i in range(total_batch):
                # Run optimization
                batch_x, batch_y, weights = next(generator)
                sess.run(train_op, feed_dict={image_tensor: batch_x,
                                              labels_tensor: batch_y,
                                              sample_weights: weights})
                progbar.update(i+1)

            if epoch % display_step == 0:
                pred = sess.run(pred_tensor, feed_dict={image_tensor:batch_x})
                loss = sess.run(loss_op, feed_dict={pred_tensor: pred,
                                                    labels_tensor: batch_y,
                                                    sample_weights: weights})
                print("Epoch:", '%04d' % (epoch + 1), "Minibatch loss=", "{:.9f}".format(loss))
                eval(sess, graph, testfiles, os.path.join(datadir,'test'),
                     in_tensorname, out_tensorname, input_size)
                saver.save(sess, os.path.join(runPath, 'model'), global_step=epoch+1, write_meta_graph=False)
                print('Saving checkpoint at epoch {}'.format(epoch + 1))


    print("Optimization Finished!")
