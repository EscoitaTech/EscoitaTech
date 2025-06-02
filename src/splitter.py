# Librería que permite cargar y cortar archivos de audio
from pydub import AudioSegment
import os                       # Para crear carpetas y manejar rutas de archivos
# Para buscar archivos con un patrón específico (por ejemplo, *.wav)
import glob


def split_audio(input_path, output_dir, chunk_duration_sec=10, start_index=0):
    """
    Esta función corta un archivo de audio en partes más pequeñas (fragmentos).
    Guarda cada fragmento como un archivo .wav separado en una carpeta indicada.

    Parámetros:
    - input_path: ruta del archivo de audio original que se quiere cortar
    - output_dir: carpeta donde se guardarán los fragmentos resultantes
    - chunk_duration_sec: duración de cada fragmento en segundos (por defecto 10)
    - start_index: número desde el que se empieza a nombrar los fragmentos
    """

    # Crea la carpeta de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Intenta cargar el archivo de audio
    try:
        audio = AudioSegment.from_file(input_path)
    except Exception as e:
        print(f"Error cargando {input_path}: {e}")
        return start_index  # Si falla, simplemente devuelve el índice actual

    # Calcula la duración total del audio en milisegundos
    duration_ms = len(audio)

    # Convierte la duración deseada de fragmento de segundos a milisegundos
    chunk_duration_ms = chunk_duration_sec * 1000

    # Empezamos a contar los fragmentos desde el índice indicado
    counter = start_index

    # Recorre el audio de principio a fin en bloques del tamaño deseado
    for i in range(0, duration_ms, chunk_duration_ms):
        chunk = audio[i:i + chunk_duration_ms]  # Extrae un fragmento de audio

        # Genera un nombre como "00000001.wav", "00000002.wav", etc.
        chunk_name = f"{counter:08d}.wav"
        chunk_path = os.path.join(output_dir, chunk_name)

        # Intenta guardar el fragmento como archivo .wav
        try:
            chunk.export(chunk_path, format="wav")
            print(f"Guardado: {chunk_path}")
        except Exception as e:
            print(f"No se pudo guardar {chunk_path}: {e}")

        counter += 1  # Aumenta el número para el siguiente archivo

    return counter  # Devuelve el nuevo índice para continuar con otros archivos


# Variable que se usa para llevar la cuenta de los nombres de los archivos generados
index = 0

# Busca todos los archivos .wav dentro de la carpeta "limpio"
for file_path in sorted(glob.glob(os.path.join(input_dir, "*.wav"))):
    # Aplica la función a cada archivo y actualiza el índice
    index = split_audio(file_path, output_dir,
                        chunk_duration, start_index=index)


def main():
    index = 0
    audio_files = sorted(glob.glob(os.path.join(input_dir, "*.wav")))

    if not audio_files:
        print(
            f"No se han encontrado archivos de audio en el directorio {input_dir}")
        return

    for file_path in audio_files:
        index = split_audio(file_path, output_dir,
                            chunk_duration, start_index=index)


input_dir = ""       # Carpeta que contiene los archivos originales largos
output_dir = ""      # Carpeta donde se guardarán los fragmentos
chunk_duration = 10        # Duración de cada fragmento en segundos

if __name__ == "__main__":
    main()
