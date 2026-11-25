# AgroVision: Advanced Leaf Disease Analytic Detection

**DSN3099 – Engineering Projects in Community Service (EPICS)**  
**VIT Bhopal University**

## Team Members
| Sl. No. | Register Number | Name |
| :--- | :--- | :--- |
| 1 | `24MEI10002` | Puli Sai Chaithanya Kumar |
| 2 | `24BEC10165` | Addepalli Sai Krishnam Raju |
| 3 | `24BCY10362` | Atla Dhatri Sai |
| 4 | `24BEC10071` | Pragada Sharmila |
| 5 | `24BCY10002` | Madineni Vignesh |
| 6 | `24MIM10243` | K Bala Yaswanth |

- **Supervisor:** Dr. Mostaid Ahmed  
- **Reviewer 1:** Ms. Mamta Patankar  
- **Reviewer 2:** Mr. Ajeet Singh  

## Project Structure
- `app.py` — Streamlit web application for leaf upload, `224×224` preprocessing, real-world augmentation preview, and disease screening.
- `src/preprocessing.py` — Image resizing, `[0, 1]` normalization, augmentation generator, and foliar color analytics.
- `src/train_cnn.py` — Phase-I 4-block CNN (`Conv2D + BatchNorm + ReLU + MaxPool + GAP + Dropout`) training script.
- `requirements.txt` — Python dependencies for Streamlit Cloud deployment.
- `assets/` — System architecture, preprocessing pipeline, CNN, Gantt chart, and evaluation figures.

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app** → Select repo `Vignesh606/Leaf-Disease-Detection`, branch `main`, main file `app.py`.
3. Click **Deploy**.

## Datasets & References
- `faysal05/plant-diseases-dataset` (Kaggle)
- `smokeyscraper/plant-diseases-dataset` (Kaggle)
- `nirmalsankalana/plant-diseases-training-dataset` (Kaggle)
- `vaibhavgovindwar/plant-diseases-dataset` (Kaggle)
- Reference implementations: `shukur-alom/leaf-diseases-detect`, `AkshayRP07/Plant-Desease-Detection`
