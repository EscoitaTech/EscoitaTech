import time
import pickle
import tflite_runtime.interpreter as tflite
import paho.mqtt.client as mqtt
from datetime import datetime
import numpy as np
import sounddevice as sd
import librosa

# Parámetros generales del sistema
INPUT_SAMPLE_RATE = 48000       # Frecuencia de muestreo con la que se graba el audio
# Frecuencia a la que se convierte el audio para análisis
SAMPLE_RATE = 16000
SEGMENT_DURATION = 5            # Duración de cada fragmento de audio en segundos
DEVICE_INDEX = 1                # Índice del micrófono a usar
MACHINE_ID_STR = ""             # Identificador de la máquina (ej. "fan_00")
MQTT_BROKER = ""                # Dirección del servidor MQTT
MQTT_TOPIC = "logs/app"         # Tema MQTT donde se enviarán los resultados
# Umbral mínimo de ruido para ignorar fragmentos silenciosos
SILENCE_THRESHOLD = 0.0005

# Aplica un filtro para realzar sonidos agudos (igual que en entrenamiento)


def apply_pre_emphasis(signal, coeff=0.97):
    return np.append(signal[0], signal[1:] - coeff * signal[:-1])

# Normaliza los valores del espectrograma para que estén entre 0 y 1


def normalize_minmax(spectrogram):
    spec_min = spectrogram.min()
    spec_max = spectrogram.max()
    return (spectrogram - spec_min) / (spec_max - spec_min + 1e-8)

# Convierte un fragmento de audio en un espectrograma mel normalizado de tamaño 128x128


def convert_to_spectrogram(segment):
    segment = apply_pre_emphasis(segment)
    melspec = librosa.feature.melspectrogram(
        y=segment, sr=SAMPLE_RATE, n_fft=2048, hop_length=512,
        n_mels=128, fmax=2000  # fmax ajustado para micrófono de contacto
    )
    melspec_db = librosa.power_to_db(melspec)
    norm_spec = normalize_minmax(melspec_db)

    # Redimensiona el espectrograma para que sea exactamente de 128x128
    resized = np.zeros((128, 128))
    h, w = norm_spec.shape
    resized[:min(128, h), :min(128, w)] = norm_spec[:min(128, h), :min(128, w)]
    # Añade dimensiones necesarias para el modelo
    return resized[np.newaxis, ..., np.newaxis].astype(np.float32)

# Ejecuta el modelo en la Raspberry Pi con el espectrograma y el ID de la máquina


def run_inference(spec, machine_id):
    for input in input_details:
        shape = list(input['shape'])
        if shape == [1, 1]:  # Input del ID de la máquina
            interpreter.set_tensor(input['index'], np.array(
                [[machine_id]], dtype=np.float32))
        elif shape == [1, 128, 128, 1]:  # Input del espectrograma
            interpreter.set_tensor(input['index'], spec.astype(np.float32))
    interpreter.invoke()
    # Devuelve el embedding
    return interpreter.get_tensor(output_details[0]['index'])[0]

# Calcula la distancia mínima entre el embedding actual y todos los embeddings normales de entrenamiento


def compute_min_distance(embedding, reference_embeddings):
    return np.min(np.linalg.norm(reference_embeddings - embedding, axis=1))


# Carga el modelo entrenado en formato TFLite
interpreter = tflite.Interpreter(model_path="encoder.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Carga los embeddings normales y los IDs correspondientes del entrenamiento
emb_train = np.load("emb_train.npy")
ids_train = np.load("ids_train.npy")

# Carga el diccionario que traduce nombres de máquina a números internos
with open("id_to_int.pkl", "rb") as f:
    id_to_int = pickle.load(f)

# Selecciona los embeddings normales correspondientes a la máquina actual
machine_idx = id_to_int[MACHINE_ID_STR]
train_subset = emb_train[ids_train == machine_idx]

# Carga el umbral óptimo de detección de anomalías para esa máquina
with open("thresholds_by_machine.pkl", "rb") as f:
    thresholds_by_machine = pickle.load(f)

# Valor por defecto si no está definido
threshold = thresholds_by_machine.get(machine_idx, 0.8789)

# Configura y conecta el cliente MQTT para enviar resultados
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, 1883)
mqtt_client.loop_start()

# Selecciona el dispositivo de entrada de audio (micrófono)
sd.default.device = DEVICE_INDEX
print("Escuchando audio en tiempo real...")

# Bucle principal: analiza el sonido en tiempo real
while True:
    print("Grabando segmento...")

    # Graba un fragmento de audio
    audio = sd.rec(int(INPUT_SAMPLE_RATE * SEGMENT_DURATION),
                   samplerate=INPUT_SAMPLE_RATE,
                   channels=1)
    sd.wait()
    segment = audio.flatten()

    # Reconvierte el audio a la frecuencia esperada por el modelo
    segment = librosa.resample(
        segment, orig_sr=INPUT_SAMPLE_RATE, target_sr=SAMPLE_RATE)

    # Ignora segmentos con poco sonido (silencio)
    if np.mean(np.abs(segment)) < SILENCE_THRESHOLD:
        print("Segmento silencioso. Saltando.")
        time.sleep(1)
        continue

    try:
        # Prepara el audio y realiza la inferencia con el modelo
        spectrogram = convert_to_spectrogram(segment)
        embedding = run_inference(spectrogram, machine_idx)

        # Calcula la distancia entre el embedding y los sonidos normales
        distance = compute_min_distance(embedding, train_subset)

        # Clasifica el sonido como normal o anómalo
        state = "abnormal" if distance > threshold else "normal"
        timestamp = datetime.utcnow().isoformat()

        # Prepara los datos a enviar
        payload = {
            "timestamp": timestamp,
            "machine_id": MACHINE_ID_STR,
            "estado": state,
            "distancia": float(distance)
        }

        # Publica el resultado por MQTT
        mqtt_client.publish(MQTT_TOPIC, str(payload))
        print(f"Publicado en MQTT: {payload}")
        print(
            f"Distancia: {distance:.4f} - Umbral: {threshold:.4f} -> {state.upper()}")

    except Exception as e:
        print(f"Error durante la inferencia: {e}")

    time.sleep(1)  # Espera antes de grabar el siguiente segmento
