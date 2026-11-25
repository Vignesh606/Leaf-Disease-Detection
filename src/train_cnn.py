"""
AgroVision Phase-I Baseline 4-Block CNN Training Script (TensorFlow/Keras).

Architecture:
  4x [Conv2D(3x3) -> BatchNormalization -> ReLU -> MaxPooling2D(2x2)]
  Filters: 32 -> 64 -> 128 -> 256
  Head: GlobalAveragePooling2D -> Dense(256, ReLU) -> Dropout(0.5) -> Dense(num_classes, Softmax)
"""

import argparse
from pathlib import Path


def build_agrovision_cnn(num_classes: int, input_shape=(224, 224, 3)):
    """Build and compile the AgroVision 4-block CNN classifier."""
    import tensorflow as tf
    from tensorflow.keras import layers, models

    inputs = layers.Input(shape=input_shape)
    x = inputs

    for filters in (32, 64, 128, 256):
        x = layers.Conv2D(filters, (3, 3), padding="same", use_bias=False)(x)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
        x = layers.MaxPooling2D(pool_size=(2, 2))(x)

    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="AgroVision_Baseline_CNN")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train(data_dir: str, epochs: int = 20, batch_size: int = 32, output_path: str = "agrovision_cnn.keras"):
    """Train the AgroVision CNN on a directory structured as <data_dir>/<class_name>/*.jpg."""
    import tensorflow as tf

    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset directory not found: {data_path}")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_path,
        validation_split=0.30,
        subset="training",
        seed=42,
        image_size=(224, 224),
        batch_size=batch_size,
        label_mode="categorical",
    )
    val_test_ds = tf.keras.utils.image_dataset_from_directory(
        data_path,
        validation_split=0.30,
        subset="validation",
        seed=42,
        image_size=(224, 224),
        batch_size=batch_size,
        label_mode="categorical",
    )

    class_names = train_ds.class_names
    aug_layer = tf.keras.Sequential([
        layers.Rescaling(1.0 / 255.0),
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.07),
        layers.RandomBrightness(0.2),
        layers.RandomContrast(0.2),
    ])
    rescale_layer = tf.keras.layers.Rescaling(1.0 / 255.0)

    train_ds = train_ds.map(lambda img, lbl: (aug_layer(img, training=True), lbl)).prefetch(tf.data.AUTOTUNE)
    val_ds = val_test_ds.map(lambda img, lbl: (rescale_layer(img), lbl)).prefetch(tf.data.AUTOTUNE)

    model = build_agrovision_cnn(num_classes=len(class_names))
    model.summary()
    model.fit(train_ds, validation_data=val_ds, epochs=epochs)
    model.save(output_path)
    print(f"Saved trained AgroVision model to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train AgroVision Baseline CNN")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to unified dataset root")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--output", type=str, default="agrovision_cnn.keras")
    args = parser.parse_args()
    train(args.data_dir, args.epochs, args.batch_size, args.output)
