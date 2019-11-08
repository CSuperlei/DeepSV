from keras import backend as K
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, BatchNormalization, LeakyReLU, Dropout, Flatten, Dense
from keras.optimizers import Adam
from keras.utils import multi_gpu_model
K.set_image_dim_ordering('tf')
K.set_image_data_format('channels_first')


def convlution_block(input_layer, n_filters, batch_normalization=True, kernel_size=(3,3), padding='same', strides=(1,1), alpha=0.1):
    layer = Conv2D(n_filters, kernel_size=kernel_size, padding=padding, strides=strides)(input_layer)
    if batch_normalization:
        layer = BatchNormalization(axis=1)(layer)

    layer = LeakyReLU(alpha=alpha)(layer)
    return layer


def maxpool_block(input_layer, pool_size=(2, 2), strides=(2,2), padding='same'):
    pool = MaxPooling2D(pool_size=pool_size, strides=strides, padding=padding)(input_layer)
    return pool


def cnn_model(input_shape=(3,255,255), n_base_filters=96, pool_size=(2,2), dropout_rate=0.3, n_labels=1, optimizer=Adam, initial_learning_rate=0.01, loss_function='categorical_crossentropy', activation_name='sigmoid', gpu_num=1, batch_normalization=True):
 
    inputs = Input(input_shape)
    current_layer = inputs

    
    conv1 = convlution_block(input_layer=current_layer, n_filters=n_base_filters, batch_normalization=batch_normalization)
    conv1 = convlution_block(input_layer=conv1, n_filters=n_base_filters, batch_normalization=batch_normalization)
    pool1 = maxpool_block(input_layer=conv1)

    conv2 = convlution_block(input_layer=pool1, n_filters=n_base_filters, batch_normalization=batch_normalization)
    conv2 = convlution_block(input_layer=conv2, n_filters=n_base_filters, batch_normalization=batch_normalization)
    pool2 = MaxPooling2D(pool_size)(conv2)

    conv3 = convlution_block(input_layer=pool2, n_filters=n_base_filters, batch_normalization=batch_normalization)
    conv3 = convlution_block(input_layer=conv3, n_filters=n_base_filters, batch_normalization=batch_normalization)
    pool3 = MaxPooling2D(pool_size)(conv3)

    conv4 = convlution_block(input_layer=pool3, n_filters=n_base_filters, batch_normalization=batch_normalization)
    conv4 = convlution_block(input_layer=conv4, n_filters=n_base_filters, batch_normalization=batch_normalization)
    pool4 = MaxPooling2D(pool_size)(conv4)


    conv5 = convlution_block(input_layer=pool4, n_filters=n_base_filters, batch_normalization=batch_normalization)
    conv5 = Dropout(dropout_rate)(conv5)
    
    conv6 = Flatten()(conv5)
    conv7 = Dense(256, activation='relu')(conv6)
    out_put = Dropout(dropout_rate)(conv7)

    model = Model(inputs=inputs, outputs=out_put)
    model.summary()

    if gpu_num>1:
        model = multi_gpu_model(model, gpus=gpu_num)
    model.compile(optimizer=optimizer(lr=initial_learning_rate), loss=loss_function)
    return model


if __name__=='__main__':
    model = cnn_model((3, 255, 255))
    for i, layer in enumerate(model.layers):
        print(i, layer.name, layer.output_shape)





