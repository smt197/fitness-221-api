# 06 - Manuel d'Utilisation et Développement

## 💻 Guide du Développeur (Local)
1. **Cloner le projet** : `git clone <repo-url>`
2. **Environnement Virtuel** :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Linux/Mac
    # ou venv\Scripts\activate sous Windows
    ```
3. **Installer les dépendances** : `pip install -r requirements.txt`
4. **Configurer l'environnement** : Créer un fichier `.env` si nécessaire avec les variables requises (Base de données, JWT).
5. **Démarrer les conteneurs (si utilisation de Docker-Compose)** :
    ```bash
    docker-compose up --build -d
    ```
6. **Lancer le serveur en local (sans Docker)** :
    ```bash
    uvicorn api:app --reload
    ```

---

## 🚀 Guide du Déploiement (Production)
1. **Hébergement** : Déployer le repository sur **Render** ou plateforme similaire.
2. **Docker** : L'application lira directement le `Dockerfile` à la racine.
3. **Environnement** : Saisir les variables clés comme `DATABASE_URL` dans les secrets de déploiement.
4. **Logs** : Surveiller les logs Uvicorn pour confirmer que le port bind correctement (généralement `0.0.0.0:8000` ou dynamique avec `$PORT`).

---

## 📚 Documentation de l'API (Swagger embarqué par FastAPI)
FastAPI génère automatiquement l'interface Swagger pour tester les endpoints :
- **Adresse** : `http://localhost:8000/docs` (ou l'URL de votre serveur `/docs`)
- **Authentification** : 
    1. Cliquez sur le bouton "Authorize" en haut à droite.
    2. Saisissez les identifiants d'un utilisateur existant (via l'endpoint login).
    3. Le Token sera automatiquement injecté pour toutes vos prochaines requêtes dans l'interface Swagger.

---
[Précédent : Infrastructure et Déploiement](./05-infrastructure-deploiement.md)
