# 🧠 Modelo de Detección de Anomalías Acústicas

Esta carpeta contiene todos los archivos necesarios para realizar **inferencia local** en una Raspberry Pi utilizando un **autoencoder convolucional condicionado por el ID de la máquina**. El modelo fue entrenado para reconstruir espectrogramas acústicos y detectar anomalías midiendo la diferencia entre los sonidos observados y los esperados de cada máquina.

## 🧩 Arquitectura del Modelo

El modelo es un **autoencoder convolucional condicional**, compuesto por:

- Un codificador que comprime espectrogramas de tamaño 128x128x1 junto con el ID de la máquina.
- Un decodificador que reconstruye el espectrograma original.
- Una capa final de embeddings con 32 dimensiones.
- Un bloque de embedding del ID de máquina (capa de embedding) con 8 dimensiones.

Esta estructura permite al modelo aprender patrones acústicos específicos de cada máquina, mejorando el rendimiento en la detección de anomalías.

## 📁 Archivos Incluidos

| Archivo                     | Descripción                                                                       |
| --------------------------- | --------------------------------------------------------------------------------- |
| `encoder.tflite`            | Modelo TFLite del codificador para extraer embeddings en la Raspberry Pi.         |
| `emb_train.npy`             | Embeddings del conjunto de entrenamiento (solo datos normales).                   |
| `ids_train.npy`             | IDs numéricos de las máquinas correspondientes a los embeddings de entrenamiento. |
| `id_to_int.pkl`             | Diccionario para convertir los nombres de las máquinas en IDs numéricos internos. |
| `thresholds_by_machine.pkl` | Umbrales óptimos de detección de anomalías (por máquina, basados en F1-score).    |

## 🧪 Flujo de Inferencia

Durante la inferencia:

1. El audio de entrada se convierte en un espectrograma de 128x128.
2. El modelo `encoder.tflite` extrae un embedding a partir del espectrograma y el ID de la máquina.
3. El embedding se compara con los embeddings normales del entrenamiento (`emb_train.npy`) para calcular una distancia.
4. La distancia se compara con el umbral óptimo de la máquina (`thresholds_by_machine.pkl`) para determinar si el sonido es **normal o anómalo**.

## 🛠️ Requisitos para Raspberry Pi

- TensorFlow Lite Runtime
- NumPy
- Script de inferencia con acceso a estos archivos de modelo

## 📌 Notas

El modelo fue entrenado utilizando espectrogramas preprocesados.
