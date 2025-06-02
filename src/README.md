# 🧠 EscoitaTECH - Processing and Inference Scripts (`src/`)

This folder contains the core scripts of the **EscoitaTECH** system, designed to detect acoustic anomalies in industrial machines through sound analysis. The scripts cover the entire pipeline—from data preparation to real-time inference.

---

## 📁 Contents of the `src/` Folder

| File                              | Description                                                                                                             |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `synthetic_anomally_generator.py` | Generates synthetic anomalous data from normal recordings, useful for training or validating the system.                |
| `splitter.py`                     | Splits long audio recordings into fixed-duration segments (chunks) for analysis.                                        |
| `calibrate_threshold.py`          | Records normal sound segments and automatically calculates a custom anomaly detection threshold for a specific machine. |
| `inference.py`                    | Performs real-time anomaly detection on a Raspberry                                                                     |

## 🚀 Dependencies installation

```bash
pip install -r requirements.txt
```
