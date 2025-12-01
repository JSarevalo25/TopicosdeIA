from ultralytics import YOLO
from paddleocr import PaddleOCR
import cv2
import json
import os
import re
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# función para extraer la placa del texto OCR
def extraer_placa(textos):
    patrones = [
        r"^[A-Z]{2}-\d{2}-\d{3}$",   # UK-33-333
        r"^[A-Z]{3}-\d{3}-[A-Z]{1}$",  # SSS-123-S
        r"^[A-Z]{3}-\d{2}-\d{2}$",   # UKF-33-33
    ]
    for texto in textos:
        print("ocr texto:", texto )
        texto = texto.upper().replace(" ", "")
        for patron in patrones:
            match = re.search(patron, texto)
            if match:
                return match.group(0).replace("-", "")
    return ""


# Cargar modelo y OCR

modelo = YOLO("best.pt")
ocr = PaddleOCR(use_angle_cls=True, lang='en')

carpeta = "./images/"
etiquetas = json.load(open("test_images.json"))

y_true = []
y_pred = []

# Procesar imágenes
for nombre_img in os.listdir(carpeta):
    real = etiquetas[nombre_img]
    img = cv2.imread(os.path.join(carpeta, nombre_img))

    detecciones = modelo(img)
    placa_predicha = ""

    for r in detecciones:
        index_placas = (r[0].boxes.cls == 1).nonzero(as_tuple=True)[0]

        for idx in index_placas:
            conf = r.boxes.conf[idx].item()
            if conf < 0.5:
                continue

            x1, y1, x2, y2 = map(int, r.boxes.xyxy[idx])
            plate = img[y1:y2, x1:x2]

            ocr_res = ocr.predict(cv2.cvtColor(plate, cv2.COLOR_BGR2RGB))
            textos = ocr_res[0]['rec_texts']

            placa_predicha = extraer_placa(textos)

    y_true.append(real)
    y_pred.append(placa_predicha)


# Evaluar resultados usando matriz de confusión y reporte de clasificación
etiquetas_ordenadas = sorted(list(set(y_true)))
# Calcular matriz de confusión
mc = confusion_matrix(y_true, y_pred, labels=etiquetas_ordenadas)
# Crear DataFrame para mejor visualización
df_mc = pd.DataFrame(mc, index=etiquetas_ordenadas, columns=etiquetas_ordenadas)

print("MATRIZ DE CONFUSIÓN \n")
print(df_mc)

# En el reporte de clasiicacion, muestra precision, recall, f1-score y support 
# En donde precision es la capacidad del clasificador para no etiquetar como positivo un ejemplo negativo.
# el recall es la capacidad del clasificador para encontrar todos los ejemplos positivos.
# El f1-score es la media armonica entre precision y recall.
# El support es el numero de ocurrencias de cada clase en y_true que significa el numero de veces que aparece cada etiqueta en 
# los datos reales.
print("REPORTE DE CLASIFICACIÓN \n")
print(classification_report(y_true, y_pred, zero_division=0))

# Visualizar matriz de confusión
# Guardamos la figura 
plt.figure(figsize=(10, 7))
sns.heatmap(df_mc, annot=True, cmap="Blues", fmt="d")
plt.title("Matriz de Confusión - Detector de Placas")
plt.xlabel("Predicción")
plt.ylabel("Real")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()
