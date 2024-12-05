from tensorflow.keras.models import load_model
import tensorflow as tf

# Definisikan ulang kelas CustomCNN jika belum ada
class CustomCNN(tf.keras.Model):
    def __init__(self, num_classes):
        super(CustomCNN, self).__init__()
        self.conv1 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same')
        self.bn1 = tf.keras.layers.BatchNormalization()
        self.pool1 = tf.keras.layers.MaxPooling2D((2, 2))

        self.conv2 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same')
        self.bn2 = tf.keras.layers.BatchNormalization()
        self.pool2 = tf.keras.layers.MaxPooling2D((2, 2))

        self.conv3 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same')
        self.bn3 = tf.keras.layers.BatchNormalization()
        self.pool3 = tf.keras.layers.MaxPooling2D((2, 2))

        self.flatten = tf.keras.layers.Flatten()
        self.fc1 = tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))
        self.dropout = tf.keras.layers.Dropout(0.5)
        self.fc2 = tf.keras.layers.Dense(num_classes, activation='softmax')

    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.bn1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.pool2(x)
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.pool3(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.dropout(x)
        return self.fc2(x)
    
    def get_config(self):
        # Return the configuration for the CustomCNN model
        config = super(CustomCNN, self).get_config()
        config.update({
            'num_classes': self.num_classes
        })
        return config

    @classmethod
    def from_config(cls, config):
    # Get num_classes from the config or set a default value if not present
        num_classes = config.get('num_classes', 10)  # Default value is 10
    # Ensure num_classes is removed from the config before passing it to the class
        config.pop('num_classes', None)  # Remove 'num_classes' from the config if present
        config.pop('trainable', None)
        config.pop('dtype', None)
        return cls(num_classes=num_classes, **config)

# Muat model dari file .h5
model_path = 'cnn_model.h5'
model = load_model(model_path, custom_objects={'CustomCNN': CustomCNN})

# Pastikan model sudah ter-load dengan benar
print(model.summary())
