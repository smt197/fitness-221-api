# 05 - Infrastructure et Déploiement

## 🐳 Conteneurisation (Docker)
L'application est entièrement conteneurisée pour garantir un environnement de production identique au développement.
### Dockerfile
Nous utilisons une image légère **`python:3.10-slim`** pour assurer l'efficacité et la compatibilité.
- **Étape d'Installation** : Installation des dépendances définies dans `requirements.txt`.
- **Préparation** : Variables d'environnement pour assurer l'optimisation Python (`PYTHONDONTWRITEBYTECODE`, `PYTHONUNBUFFERED`).
- **Exécution** : Application servie via le serveur ASGI **Uvicorn**.

## 🚀 Déploiement sur Render
Le projet peut être déployé en continu sur une plateforme comme **Render**.
1.  **Web Service** : L'image Docker de la branche principale est construite automatiquement par Render.
2.  **Base de Données** : Utilisation d'une instance PostgreSQL de Render ou d'un fournisseur cloud connecté à l'application.

```mermaid
graph LR
    User[Utilisateurs Externes] -- HTTPS --> Render[Ingress / Load Balancer]
    
    subgraph "Infrastructure Cloud (Render)"
        subgraph "Docker Container"
            Render --> App["FastAPI & Uvicorn"]
            App --> SQLA[SQLAlchemy]
        end
        SQLA -- PostgreSQL Protocol --> DB[(Base de Données)]
    end
```

## 🌐 Configuration des Variables (Environment)
La sécurisation et le fonctionnement de l'API reposent sur les variables d'environnement telles que :
- `DATABASE_URL` : Chaîne de connexion PostgreSQL.
- `SECRET_KEY` : Clé de cryptage pour émettre les tokens JWT.

---
[Précédent : Conception des Données](./04-conception-donnees.md) | [Suivant : Manuel d'Utilisation](./06-manuel-utilisation.md)
