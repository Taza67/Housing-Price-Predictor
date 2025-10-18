# France Housing Price Predictor

Algorithme de prédiction des prix immobiliers français.  
Cette application permet d'estimer le prix de logements en France à partir de différentes caractéristiques.

---

## 📂 Structure du projet

.

├── constants.py

├── data/

├── data-retrieval.ipynb

├── Dockerfile.streamlit

├── docker-compose.yml

├── housing-price-predictor.ipynb

├── logs/

├── main.py

├── models/

├── requirements.txt

├── transfomers.py

├── utilities.py

└── README.md

-   **`main.py`** : Point d’entrée Streamlit de l’application.
-   **`data/`** : Contient les jeux de données nécessaires.
-   **`models/`** : Contient les modèles entraînés.
-   **`logs/`** : Fichiers de logs.
-   **`Dockerfile.streamlit`** : Dockerfile pour lancer l’application Streamlit.
-   **`docker-compose.yml`** : Configuration Docker Compose.

---

## 🐳 Installation avec Docker

### Prérequis

-   [Docker](https://www.docker.com/get-started) installé.
-   [Docker Compose](https://docs.docker.com/compose/install/) installé.

### Construction et lancement

Depuis le répertoire racine du projet :

```bash
docker-compose up --build
```

-   L’application Streamlit sera exposée sur le port **8501**.
-   Accéder à l’application via : `http://localhost:8501`.

---

## 🚀 Lancer automatiquement dans le navigateur

Docker ne peut pas ouvrir directement le navigateur sur ton PC.
Mais tu peux le faire via un petit script côté hôte.

### Linux / Mac

```bash
#!/bin/bash
docker-compose up & sleep 5
xdg-open http://localhost:8501
```

### Windows (PowerShell)

```powershell
Start-Process "docker-compose" "up"
Start-Sleep -s 5
Start-Process "http://localhost:8501"
```

-   Le conteneur ne fait que servir l’application.
-   L’ouverture du navigateur se fait côté **hôte**, pas depuis Docker.

---

## 🔧 Configuration Streamlit

Dans le Dockerfile :

```dockerfile
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

-   `--server.address=0.0.0.0` : rend l’application accessible depuis l’hôte.

---

## 📚 Notes

-   Pour le développement local, tu peux éditer les fichiers sur ton hôte. Les changements ne seront visibles dans le conteneur que si tu reconstruis l’image Docker (`docker-compose build --no-cache`).

---

## 💡 Amélioration

-   Ce projet a été développé dans un **but d'apprentissage**.
-   Les **résultats des modèles ne sont pas parfaits** et peuvent être améliorés par des techniques de feature engineering, tuning des hyperparamètres et utilisation de datasets plus riches.
-   Il s’agit d’une **base pour expérimenter et apprendre** sur la prédiction de prix immobiliers.

---

## 📄 License

Ce projet est sous licence MIT.
