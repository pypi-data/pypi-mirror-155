import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow import keras

PATH = os.getcwd()

def load_data(folder_name):
    folder_path = os.path.join(os.getcwd(), "src", "data", folder_name)
    x_data = []
    for sample in sorted(os.listdir(folder_path)):
        tmp = tf.keras.preprocessing.image.load_img(os.path.join(folder_path, sample))
        tmp = tf.image.resize(tmp, [800, 600])
        x = tf.keras.preprocessing.image.img_to_array(tmp) / 255
        
        if(folder_name == "train_masks" or folder_name == "test_masks"):
            converted = tf.image.rgb_to_grayscale(x)
            x_data.append(converted)
        else:
           x_data.append(x) 
    return x_data

def plot_acc_loss(accuracy_values, loss_values, saving_name):
    # plot training ACCURACY VALUES
    fig = plt.figure()
    gs = fig.add_gridspec(ncols = 1,nrows = 2)
    plt.subplot(gs[0])
    plt.plot(accuracy_values)
    plt.ylabel('Accuracy')
    plt.legend(['Train data'], loc = 'upper left')

    # plot training LOSS VALUES
    plt.subplot(gs[1])
    plt.plot(loss_values)
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train data'], loc = 'upper left')
    plt.tight_layout()
    fig.savefig(os.path.join(PATH, 'results','') + '{}.png'.format(saving_name), dpi = fig.dpi)