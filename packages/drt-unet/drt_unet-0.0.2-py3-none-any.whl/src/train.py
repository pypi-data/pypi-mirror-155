import os
import numpy as np

import tensorflow as tf
from PIL import Image
from unet import UNet

from utils import load_data, plot_acc_loss

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

gpu_available = tf.test.is_gpu_available(cuda_only=True)

if gpu_available:
    print('GPU found')
    device = 'gpu'
else:
    print("No GPU found")
    device = 'cpu'


PATH = os.getcwd()
BATCH_SIZE = 16
EPOCHS_NUMBER = 2000
LOSS = 'bce'
SAVING_NAME = 'model{}_e{}_b{}'.format(LOSS, EPOCHS_NUMBER, BATCH_SIZE)

print("Start load train images.")
train_images = load_data('train_images') 
train_masks = load_data('train_masks')
print("Start load test images.")
test_images = load_data('test_images') 
test_masks = load_data('test_masks') 
print("End load.")

model = UNet()

trained = False
model_path = os.path.join(os.getcwd(), "src", "models")
# проверку переделать
if len(os.listdir(model_path)) != 0:
    latest = tf.train.latest_checkpoint(model_path)
    model.load_weights(latest)
    trained = True
 
if not trained:
    
    model.compile(optimizer='adam',
                loss=[LOSS],
                metrics=['bce', 'accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])

    # Train the model
    print("Start train!")

    dataset = tf.data.Dataset.from_tensors((train_images, train_masks))
    test_dataset = tf.data.Dataset.from_tensors((test_images, test_masks))

    print(dataset)

    fit = model.fit(dataset, batch_size=BATCH_SIZE, epochs=EPOCHS_NUMBER, shuffle=True, validation_data=test_dataset)
    
    test_loss, _, test_acc, _, _   = model.evaluate(test_dataset)

    # save model
    
    model.save_weights('src/models/{}model'.format(SAVING_NAME))

    print("Train complete. Model saved.")

test_images_tensor = tf.data.Dataset.from_tensors(test_images)
# # Predict and save masks for the test set
predicted_masks = model.predict(test_images_tensor, batch_size=BATCH_SIZE)

for i in range(10):
    pred_mask = np.squeeze(predicted_masks[i])
    true_mask = test_masks[i]
    tmp = np.ceil(pred_mask * 255.).astype(np.uint8)
    im = Image.fromarray(tmp)
    im.save('src/results/test{}{}.{}.png'.format(EPOCHS_NUMBER, BATCH_SIZE, i))

# results_file = open('models/{}test_loss{}test_accuracy.txt'.format(test_loss, test_acc), 'w')
# results_file.write(SAVING_NAME)
# results_file.close()

# plot_acc_loss(fit.history['accuracy'], fit.history['loss'], SAVING_NAME)
