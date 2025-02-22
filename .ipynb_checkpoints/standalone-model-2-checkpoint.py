# modified from https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html
# and from wandb class


from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K

import wandb
from wandb.keras import WandbCallback


run = wandb.init()
config = run.config

# dimensions of our images.
config.img_width, config.img_height = 150, 150

train_data_dir = '../dogcat-data/train'
validation_data_dir = '../dogcat-data/validation'
nb_train_samples = 2000
nb_validation_samples = 2000
config.epochs = 50
config.batch_size = 32

input_shape = (config.img_width, config.img_height, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.summary()
#exit()
model.compile(loss='binary_crossentropy', optimizer='sgd',
              metrics=['accuracy'])

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
    )

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(config.img_width, config.img_height),
    batch_size=config.batch_size,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(config.img_width, config.img_height),
    batch_size=config.batch_size,
    class_mode='binary')


model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // config.batch_size,
    epochs=config.epochs,
    callbacks=[WandbCallback()],
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // config.batch_size)
