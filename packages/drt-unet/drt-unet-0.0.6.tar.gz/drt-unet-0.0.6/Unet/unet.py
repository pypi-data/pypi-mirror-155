import tensorflow as tf
import numpy as np

def double_conv(in_channels, out_channels):
    return tf.keras.Sequential(layers=(tf.keras.layers.Conv2D(out_channels, kernel_size=3, padding='SAME'),
                                       tf.keras.layers.BatchNormalization(),
                                       tf.keras.layers.ReLU(),
                                       tf.keras.layers.Conv2D(out_channels, kernel_size=3, padding='SAME'),
                                       tf.keras.layers.BatchNormalization(),
                                       tf.keras.layers.ReLU()
                                       ))

class Down(tf.keras.layers.Layer):
    def __init__(self, in_channels, out_channels):
        super(Down, self).__init__()
        self.conv = double_conv(in_channels, out_channels)
        self.pool = tf.keras.layers.MaxPool2D(2)

    def call(self, x):
        x = self.pool(x)
        return self.conv(x)


class Up(tf.keras.layers.Layer):
    def __init__(self, in_channels, out_channels):
        super(Up, self).__init__()
        self.conv = double_conv(in_channels, out_channels)
        self.upsample = tf.keras.layers.UpSampling2D(2, interpolation='bilinear')

    def call(self, x1, x2):
        x1 = self.upsample(x1)
        diffY = x2.shape[1] - x1.shape[1]
        diffX = x2.shape[2] - x1.shape[2]
        paddings = tf.constant([[0, 0], [diffY, 0], [diffX, 0], [0, 0]])
        x1 = tf.pad(x1, paddings)
        x = tf.concat((x2, x1), axis=-1)
        return self.conv(x)


class UNet(tf.keras.Model):
    def __init__(self, device = None):
        super(UNet, self).__init__()
        self.inc = double_conv(3, 4)  
        self.down1 = Down(4, 8)
        self.down2 = Down(8, 16)
        self.down3 = Down(16, 32)
        factor = 2
        self.down4 = Down(32, 64 // factor)
        self.up1 = Up(64, 32 // factor)
        self.up2 = Up(32, 16 // factor)
        self.up3 = Up(16, 8 // factor)
        self.up4 = Up(8, 4)
        self.outc = tf.keras.layers.Conv2D(filters=1, kernel_size=1)

    def call(self, x, training=False):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        logits = self.outc(x)
        return tf.sigmoid(logits)
