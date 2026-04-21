# 02 - Analyse Fonctionnelle

## 🛠️ Fonctionnalités par Profil

### 🔒 Authentification et Profils
- **Inscription & Connexion** : Inscription d'utilisateurs avec rôles (`ADMIN`, `COACH`, `ABONNE`).
- **Protection JWT** : Sécurisation de toutes les routes de l'API via OAuth2 et JWT.

### 🏋️ Gestion des Entités (Admin)
- **Coachs** : Création, modification et suppression des profils de coachs avec leurs spécialités.
- **Abonnés** : Gestion des inscriptions d'abonnés et de leurs types d'abonnement (MENSUEL, TRIMESTRIEL, ANNUEL).
- **Activités** : Définition des séances de fitness avec code, nom, durée et capacité maximale (`placesMax`).

### 📅 Système de Réservation (Cœur du projet)
- **Réservation de séances** : Un abonné peut s'inscrire à une séance supervisée par un coach.
- **Règles Métier (Validations)** :
    1. **Disponibilité du Coach** : Un coach ne peut pas avoir deux réservations sur le même créneau horaire.
    2. **Capacité de l'Activité** : On ne peut pas dépasser le nombre de places maximum (`placesMax`) pour une séance donnée.
    3. **Unicité de l'Abonné** : Un abonné ne peut pas réserver deux fois la même activité sur le même créneau.
    4. **Contrôle Temporel** : Les réservations ne sont autorisées que pour des dates futures.

## 👥 Cas d'Utilisation (Use Cases)
- **En tant qu'Admin** : Je veux créer une nouvelle activité "Yoga" pour diversifier le studio.
- **En tant qu'Abonné** : Je veux réserver ma place pour la séance de "Musculation" de demain à 10h.
- **En tant que Coach** : Je veux voir la liste des abonnés inscrits à ma séance de ce soir.

---
[Précédent : Introduction](./01-introduction.md) | [Suivant : Architecture Logicielle](./03-architecture-logicielle.md)
