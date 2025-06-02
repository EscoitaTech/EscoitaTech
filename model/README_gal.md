# 🧠 Modelo de Detección de Anomalías Acústicas

Este cartafol contén todos os arquivos necesarios para realizar **inferencias locais** nunha Raspberry Pi utilizando un **autoencoder convolucional condicionado polo ID da máquina**. O modelo foi adestrado para reconstruír espectrogramas acústicos e detectar anomalías medindo a diferenza entre os sons observados e os esperados de cada máquina.

## 🧩 Arquitectura do Modelo

O modelo é un **autoencoder convolucional condicional**, composto por:

- Un codificador que comprime espectrogramas de tamaño 128x128x1 xunto co ID da máquina.
- Un decodificador que reconstrúe o espectrograma orixinal.
- Unha capa final de embeddings con 32 dimensións.
- Un bloque de embedding para o ID da máquina (capa de embedding) con 8 dimensións.

Esta estrutura permite que o modelo aprenda os patróns acústicos específicos de cada máquina, mellorando o rendemento na detección de anomalías.

## 📁 Arquivos Incluídos

| Arquivo                     | Descrición                                                                      |
| --------------------------- | ------------------------------------------------------------------------------- |
| `encoder.tflite`            | Modelo TFLite do codificador para extraer embeddings na Raspberry Pi.           |
| `emb_train.npy`             | Embeddings do conxunto de adestramento (só datos normais).                      |
| `ids_train.npy`             | IDs numéricos das máquinas correspondentes aos embeddings de adestramento.      |
| `id_to_int.pkl`             | Dicionario para converter os nomes das máquinas en IDs numéricos internos.      |
| `thresholds_by_machine.pkl` | Umbrales óptimos de detección de anomalías (por máquina, baseados en F1-score). |

## 🧪 Fluxo de Inferencia

Durante a inferencia:

1. O audio de entrada convértese nun espectrograma de 128x128.
2. O modelo `encoder.tflite` extrae un embedding a partir do espectrograma e do ID da máquina.
3. O embedding compárase cos embeddings normais do adestramento (`emb_train.npy`) para calcular unha distancia.
4. A distancia compárase co umbral óptimo da máquina (`thresholds_by_machine.pkl`) para determinar se o son é **normal ou anómalo**.

## 🛠️ Requisitos para Raspberry Pi

- TensorFlow Lite Runtime
- NumPy
- Script de inferencia con acceso a estes arquivos do modelo

## 📌 Notas

O modelo foi adestrado utilizando espectrogramas preprocesados.
