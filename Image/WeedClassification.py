import tensorflow as tf
import sklearn
import numpy as np
from PIL import Image

class WeedClassifier:

    def __init__(self):
        pass

    @staticmethod
    def resize_img(name, width, height):
        img = Image.open(name)
        if img.size[0] < width:
            print('Image too small to be processed without risk.')
            return None
        elif img.size[1] < height:
            print('Image too small to be processed without risk.')
            return None
        img = img.resize((width, height), Image.ANTIALIAS)  # image resize filter
        return img

    def train(self, imgs, labels):
        x = 100
        y = 100
        mode = tf.estimator.ModeKeys.TRAIN

        print(imgs[0].shape)
        # Input Layer
        input_layer = [tf.reshape(img, [-1, x, y, 3]) for img in imgs]
        # -1 is for dynamic calculation based on batch size

        # Convolutional Layer #1
        conv1 = tf.layers.conv2d(
            inputs=input_layer,
            filters=32,
            kernel_size=[5, 5],  # dimensions of filters
            padding="same",
            activation=tf.nn.relu)

        # Pooling Layer #1
        pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

        # Convolutional Layer #2 and Pooling Layer #2
        conv2 = tf.layers.conv2d(
            inputs=pool1,
            filters=64,
            kernel_size=[5, 5],
            padding="same",
            activation=tf.nn.relu)
        pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

        # Dense Layer
        pool2_flat = tf.reshape(pool2, [-1, x/4 * y/4 * 64])
        dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
        dropout = tf.layers.dropout(
            inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

        # Logits Layer
        logits = tf.layers.dense(inputs=dropout, units=2)

        # Calculate Loss
        loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
        
        # Configure the Training Op (for TRAIN mode)
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())

        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)
        
import os
from sklearn.model_selection import train_test_split

# weed folder and plant folder
wFolder = 'Weed-Broadleaf_Plantain_small'
pFolder = 'Plant-Lettuce_small'

# rename for full relative path
weeds = os.listdir(wFolder)
weeds = [os.path.join(wFolder, name) for name in weeds]
weedLabels = [1 for _ in range(len(weeds))]
plants = os.listdir(pFolder)
plants = [os.path.join(pFolder, name) for name in plants]
plantLabels = [0 for _ in range(len(plants))]

# put together the two different lists
objects = weeds + plants
labels = weedLabels + plantLabels

# objects -> imgs
imgs = [np.asarray(Image.open(name).convert('L')) for name in objects]

# split the data
X_train, y_train, X_test, y_test = train_test_split(imgs, labels, test_size=0.2)
print(len(X_train), len(y_train))
print(len(X_test), len(y_test))

# weed classifier
wc = WeedClassifier()
wc.train(X_train, y_train)
