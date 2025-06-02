# 🧠 Acoustic Anomaly Detection Model

This folder contains all the necessary files for **local inference** on a Raspberry Pi using a **convolutional autoencoder conditioned on machine ID**. The model was trained to reconstruct acoustic spectrograms and detect anomalies by measuring the difference between the observed and expected sounds of each machine.

## 🧩 Model Architecture

The model is a **conditional convolutional autoencoder**, consisting of:

- An encoder that compresses 128x128x1 spectrograms together with a machine ID.
- A decoder that reconstructs the original spectrogram.
- A final embedding layer with 32 dimensions.
- A machine ID embedding block (embedding layer) with 8 dimensions.

This structure allows the model to learn machine-specific acoustic patterns, improving anomaly detection performance.

## 📁 Included Files

| File                        | Description                                                            |
| --------------------------- | ---------------------------------------------------------------------- |
| `encoder.tflite`            | TFLite encoder model for extracting embeddings on Raspberry Pi.        |
| `emb_train.npy`             | Training set embeddings (normal data only).                            |
| `ids_train.npy`             | Numeric machine IDs corresponding to the training embeddings.          |
| `id_to_int.pkl`             | Dictionary for converting machine names to internal numeric IDs.       |
| `thresholds_by_machine.pkl` | Optimal anomaly detection thresholds (per machine, based on F1-score). |

## 🧪 Inference Workflow

During inference:

1. The input audio is converted into a 128x128 spectrogram.
2. The `encoder.tflite` model extracts an embedding from the spectrogram and machine ID.
3. The embedding is compared to the corresponding normal training embeddings (`emb_train.npy`) to compute a distance.
4. The distance is compared against the machine's optimal threshold (`thresholds_by_machine.pkl`) to determine whether the sound is **normal or anomalous**.

## 🛠️ Raspberry Pi Requirements

- TensorFlow Lite Runtime
- NumPy
- Inference script with access to these model files

## 📌 Notes

The model was trained using preprocessed spectrograms.

---
