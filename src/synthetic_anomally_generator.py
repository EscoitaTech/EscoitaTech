import librosa
import soundfile as sf
import scipy.signal as sg
import numpy as np
import pathlib
import random

# Configuración general
INPUT_ROOT = ""       # Carpeta con archivos de audio normales
OUTPUT_ROOT = ""    # Carpeta donde se guardarán los archivos anómalos generados
# Tipo de anomalía: "rub", "block", "unbal", "noise" o "mix" (mezcla)
ANOMALY_TYPE = "mix"
COPIES = 1                  # Número de versiones anómalas a generar por cada audio
SEVERITY = 0.6              # Intensidad del fallo (0 = leve, 1 = fuerte)
SEED = 42                   # Semilla aleatoria para obtener resultados reproducibles

# Establece la semilla aleatoria para que los resultados sean consistentes
random.seed(SEED)
np.random.seed(SEED)


# Función que simula un fallo de tipo "rozamiento de aspas"
def blade_rub(signal, sr, severity=0.7, n_bursts=8):
    output = signal.copy()
    burst_len = int(0.02 * sr)  # Duración de cada "rozamiento"
    # Filtro para generar el ruido agudo típico del rozamiento
    sos = sg.butter(4, 3000 / (sr / 2), btype="highpass", output="sos")
    for _ in range(n_bursts):
        start = random.randint(0, len(signal) - burst_len - 1)
        burst = np.random.randn(burst_len) * severity * 0.3
        burst = sg.sosfilt(sos, burst)
        output[start:start + burst_len] += burst
    return np.clip(output, -1, 1)


# Función que simula un fallo de tipo "bloqueo parcial del flujo"
def partial_blockage(signal, sr, severity=0.5):
    low = random.uniform(500, 1500)
    high = low + random.uniform(300, 800)
    sos = sg.butter(4, [low / (sr / 2), high / (sr / 2)],
                    btype="bandstop", output="sos")
    filtered = sg.sosfilt(sos, signal)
    return np.clip((1 - severity) * signal + severity * filtered, -1, 1)


# Función que simula un fallo por desequilibrio mecánico
def unbalance_modulation(signal, sr, severity=0.5):
    freq = random.uniform(4, 12)
    t = np.arange(len(signal)) / sr
    modulation = 1 + severity * 0.3 * np.sin(2 * np.pi * freq * t)
    return np.clip(signal * modulation, -1, 1)


# Función que añade ruidos impulsivos como pequeñas explosiones
def noise_burst(signal, sr, severity=0.5, n_bursts=3):
    output = signal.copy()
    burst_len = int(0.05 * sr)
    for _ in range(n_bursts):
        start = random.randint(0, len(signal) - burst_len - 1)
        burst = np.random.randn(burst_len) * severity * 0.2
        output[start:start + burst_len] += burst
    return np.clip(output, -1, 1)


# Diccionario que relaciona el tipo de anomalía con su función correspondiente
ANOMALY_FUNCTIONS = {
    "rub": blade_rub,
    "block": partial_blockage,
    "unbal": unbalance_modulation,
    "noise": noise_burst,
}


# Función principal que aplica una o varias anomalías al audio original
def generate_anomaly(signal, sr, anomaly_type, severity=0.6):
    if anomaly_type == "mix":
        # Selecciona aleatoriamente dos tipos de anomalía
        selected = random.sample(list(ANOMALY_FUNCTIONS.keys()), k=2)
        output = signal.copy()
        for name in selected:
            output = ANOMALY_FUNCTIONS[name](output, sr, severity)
        return output

    if anomaly_type not in ANOMALY_FUNCTIONS:
        raise ValueError("Tipo de anomalía no reconocido: " + anomaly_type)

    return ANOMALY_FUNCTIONS[anomaly_type](signal, sr, severity)


# Busca todos los archivos .wav en la carpeta de entrada y sus subcarpetas
def collect_wav_files(root_path):
    path = pathlib.Path(root_path)
    return list(path.rglob("*.wav"))


# Construye la ruta de destino para guardar el archivo modificado
def build_output_path(source_path, output_root, copy_index=0):
    source_path = pathlib.Path(source_path)
    relative = source_path.relative_to(INPUT_ROOT)
    parts = list(relative.parts)

    if COPIES > 1:
        # Si se generan varias copias, se crea una subcarpeta para cada copia
        parts.insert(-1, f"copy{copy_index}")

    return pathlib.Path(output_root, *parts)


# Procesa todos los archivos .wav encontrados, aplicando las anomalías
def process_all_files():
    source_files = collect_wav_files(INPUT_ROOT)

    if not source_files:
        raise RuntimeError(
            f"No se encontraron archivos .wav en la carpeta '{INPUT_ROOT}'.")

    print(
        f"Generando archivos con anomalía '{ANOMALY_TYPE}' (intensidad={SEVERITY})")
    print(
        f"Número de archivos: {len(source_files)} × {COPIES} copia(s) cada uno")

    for source in source_files:
        signal, sr = librosa.load(source, sr=None)

        for c in range(COPIES):
            modified = generate_anomaly(signal, sr, ANOMALY_TYPE, SEVERITY)
            destination = build_output_path(source, OUTPUT_ROOT, c)
            destination.parent.mkdir(parents=True, exist_ok=True)
            sf.write(destination, modified, sr)

    print("Proceso finalizado. Los archivos anómalos se han guardado en:")
    print(pathlib.Path(OUTPUT_ROOT).resolve())


# Punto de entrada del script: ejecuta el procesamiento completo si se llama desde terminal
if __name__ == "__main__":
    process_all_files()
