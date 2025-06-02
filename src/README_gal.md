# 🧠 EscoitaTECH - Scripts de Procesamento e Inferencia (`src/`)

Este cartafol contén os scripts esenciais do sistema **EscoitaTECH**, deseñado para detectar anomalías acústicas en máquinas industriais mediante a análise de son. Os scripts cobren todo o proceso: desde a preparación de datos ata a inferencia en tempo real.

---

## 📁 Contido do cartafol `src/`

| Ficheiro                          | Descrición                                                                                                           |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `synthetic_anomally_generator.py` | Xera datos anómalos sintéticos a partir de gravacións normais, útiles para adestrar ou validar o sistema.            |
| `splitter.py`                     | Divide arquivos de son longos en segmentos de duración fixa para a súa análise.                                      |
| `calibrate_threshold.py`          | Grava segmentos normais e calcula automaticamente un limiar personalizado de detección para unha máquina específica. |
| `inference.py`                    | Executa a detección de anomalías en tempo real nunha Raspberry Pi usando entrada de audio e un modelo lixeiro.       |

---

## 🚀 Instalación de dependencias

Instala todas as dependencias necesarias con:

```bash
pip install -r requirements.txt
```
