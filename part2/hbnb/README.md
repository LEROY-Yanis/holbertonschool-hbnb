# 🏠 HBnB - API REST pour Plateforme de Location

## 📖 Description

HBnB est une API REST développée avec Flask pour gérer une plateforme de location de logements (type Airbnb). L'application permet de gérer des utilisateurs, des lieux, des équipements (amenities) et des avis (reviews).

## 🏗️ Architecture

Le projet suit une architecture en couches basée sur les design patterns suivants :

```
┌─────────────────────────────────────────┐
│         CLIENT (Postman, curl)          │
└────────────────┬────────────────────────┘
                 │ HTTP Request
                 ↓
┌─────────────────────────────────────────┐
│    API Layer (Flask-RESTX Routes)       │
│  users.py, amenities.py, places.py      │
│              reviews.py                 │
└────────────────┬────────────────────────┘
                 │ Appelle méthodes
                 ↓
┌─────────────────────────────────────────┐
│    Business Logic Layer (Facade)        │
│         HBnBFacade (facade.py)          │
│    Validations + Logique métier         │
└────────────────┬────────────────────────┘
                 │ Manipule objets
                 ↓
┌─────────────────────────────────────────┐
│      Model Layer (Entités)              │
│  User, Place, Review, Amenity           │
│          BaseModel                      │
└────────────────┬────────────────────────┘
                 │ Persisté via
                 ↓
┌─────────────────────────────────────────┐
│   Persistence Layer (Repository)        │
│      InMemoryRepository                 │
│         _storage (dict)                 │
└─────────────────────────────────────────┘
```

### Design Patterns utilisés

- **Pattern Facade** : Simplifie l'accès aux différents repositories
- **Pattern Repository** : Abstraction de la couche de persistance
- **Pattern MVC adapté** : Séparation claire entre modèles, vues (API) et logique métier

## 📁 Structure du Projet

```
hbnb/
├── run.py                      # Point d'entrée de l'application
├── config.py                   # Configuration de l'application
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
└── app/
    ├── __init__.py            # Initialisation Flask et enregistrement des routes
    ├── models/                # Modèles de données
    │   ├── __init__.py
    │   ├── basemodel.py       # Classe de base pour tous les modèles
    │   ├── user.py            # Modèle Utilisateur
    │   ├── amenity.py         # Modèle Équipement
    │   ├── place.py           # Modèle Lieu
    │   └── review.py          # Modèle Avis
    ├── persistence/           # Couche de persistance
    │   ├── __init__.py
    │   └── repository.py      # Repository abstrait et implémentation en mémoire
    ├── services/              # Logique métier
    │   ├── __init__.py
    │   └── facade.py          # Facade centralisant les opérations
    └── api/                   # Endpoints de l'API REST
        ├── __init__.py
        └── v1/                # Version 1 de l'API
            ├── __init__.py
            ├── users.py       # Endpoints utilisateurs
            ├── amenities.py   # Endpoints équipements
            ├── places.py      # Endpoints lieux
            └── reviews.py     # Endpoints avis
```

## 🚀 Installation

### Prérequis

- Python 3.8+
- pip

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/LEROY-Yanis/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2/hbnb
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
python3 run.py
```

L'API sera accessible sur `http://127.0.0.1:5000`

## 📚 Documentation de l'API

### Documentation Swagger

Une fois l'application lancée, accédez à la documentation interactive Swagger :
```
http://127.0.0.1:5000/api/v1/docs
```

### Endpoints disponibles

#### 👤 Utilisateurs (`/api/v1/users`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/api/v1/users/` | Créer un nouvel utilisateur |
| `GET` | `/api/v1/users/<user_id>` | Récupérer un utilisateur par ID |

**Exemple de requête POST** :
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

#### 🎯 Équipements (`/api/v1/amenities`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/api/v1/amenities/` | Créer un nouvel équipement |
| `GET` | `/api/v1/amenities/` | Lister tous les équipements |
| `GET` | `/api/v1/amenities/<amenity_id>` | Récupérer un équipement par ID |
| `PUT` | `/api/v1/amenities/<amenity_id>` | Mettre à jour un équipement |

**Exemple de requête POST** :
```json
{
  "name": "WiFi"
}
```

#### 🏠 Lieux (`/api/v1/places`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/api/v1/places/` | Créer un nouveau lieu |
| `GET` | `/api/v1/places/` | Lister tous les lieux |
| `GET` | `/api/v1/places/<place_id>` | Récupérer un lieu par ID |

**Exemple de requête POST** :
```json
{
  "title": "Cozy Apartment",
  "description": "Beautiful apartment in city center",
  "price": 100.0,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner_id": "uuid-of-owner",
  "amenities": ["uuid-amenity-1", "uuid-amenity-2"]
}
```

#### ⭐ Avis (`/api/v1/reviews`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/api/v1/reviews/` | Créer un nouvel avis |
| `GET` | `/api/v1/reviews/` | Lister tous les avis |
| `GET` | `/api/v1/reviews/<review_id>` | Récupérer un avis par ID |
| `PUT` | `/api/v1/reviews/<review_id>` | Mettre à jour un avis |
| `DELETE` | `/api/v1/reviews/<review_id>` | Supprimer un avis |

**Exemple de requête POST** :
```json
{
  "text": "Great place to stay!",
  "rating": 5,
  "user_id": "uuid-of-user",
  "place_id": "uuid-of-place"
}
```

## 🔍 Modèles de Données

### BaseModel
Classe de base pour tous les modèles, fournissant :
- `id` : Identifiant unique (UUID)
- `created_at` : Date de création (ISO format)
- `updated_at` : Date de dernière modification (ISO format)

### User (Utilisateur)
- `first_name` : Prénom (1-50 caractères)
- `last_name` : Nom (1-50 caractères)
- `email` : Email (format validé)
- `is_admin` : Statut administrateur (booléen, défaut: false)

### Amenity (Équipement)
- `name` : Nom de l'équipement (1-50 caractères)

### Place (Lieu)
- `title` : Titre du lieu (requis)
- `description` : Description du lieu
- `price` : Prix par nuit (> 0)
- `latitude` : Latitude (-90 à 90)
- `longitude` : Longitude (-180 à 180)
- `owner_id` : ID du propriétaire (référence User)
- `amenities` : Liste des IDs d'équipements
- `reviews` : Liste des IDs d'avis

### Review (Avis)
- `text` : Texte de l'avis (requis)
- `rating` : Note de 1 à 5 (entier requis)
- `user_id` : ID de l'utilisateur (référence User)
- `place_id` : ID du lieu (référence Place)

## 🔐 Validations

### Validations automatiques

- **User** :
  - Email unique dans le système
  - Format email valide (regex)
  - Nom et prénom entre 1 et 50 caractères

- **Amenity** :
  - Nom non vide et max 50 caractères

- **Place** :
  - Titre obligatoire
  - Prix strictement positif
  - Latitude entre -90 et 90
  - Longitude entre -180 et 180
  - Owner (propriétaire) doit exister
  - Tous les amenities doivent exister

- **Review** :
  - Texte obligatoire
  - Rating entre 1 et 5 (entier)
  - User doit exister
  - Place doit exister

## 🧪 Tests avec cURL

### Créer un utilisateur
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com"}'
```

### Créer un équipement
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name":"WiFi"}'
```

### Lister tous les équipements
```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/
```

### Créer un lieu
```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Cozy Studio",
    "description":"Nice place",
    "price":75.0,
    "latitude":48.8566,
    "longitude":2.3522,
    "owner_id":"<USER_ID>",
    "amenities":["<AMENITY_ID>"]
  }'
```

## 🛠️ Technologies Utilisées

- **Flask** : Framework web Python minimaliste
- **Flask-RESTX** : Extension Flask pour créer des APIs REST avec documentation Swagger automatique
- **Python 3** : Langage de programmation

## ⚙️ Configuration

Le fichier `config.py` contient les configurations de l'application :

```python
SECRET_KEY : Clé secrète pour les sessions
DEBUG : Mode debug (True en développement)
```

## 📝 Persistence des Données

Actuellement, le projet utilise un **InMemoryRepository** :
- Les données sont stockées en mémoire (dictionnaire Python)
- ✅ Avantage : Rapide, simple à utiliser
- ⚠️ Inconvénient : Les données sont perdues au redémarrage du serveur

### Évolution future
Le pattern Repository permet de facilement remplacer le stockage en mémoire par :
- Une base de données SQL (PostgreSQL, MySQL)
- Une base de données NoSQL (MongoDB)
- Des fichiers JSON persistants

## 🚦 Codes de Statut HTTP

| Code | Signification |
|------|---------------|
| `200` | OK - Requête réussie |
| `201` | Created - Ressource créée avec succès |
| `400` | Bad Request - Données invalides |
| `404` | Not Found - Ressource non trouvée |

## 🔄 Flux de Traitement d'une Requête

```
1. Client envoie une requête HTTP
   ↓
2. Flask route vers le bon endpoint (users.py, places.py, etc.)
   ↓
3. Flask-RESTX valide les données entrantes
   ↓
4. L'endpoint appelle une méthode du Facade
   ↓
5. Le Facade effectue les validations métier
   ↓
6. Le Facade manipule les modèles (User, Place, etc.)
   ↓
7. Les modèles sont persistés via le Repository
   ↓
8. Réponse JSON renvoyée au client avec code HTTP approprié
```

## 👨‍💻 Développement

### Ajouter un nouvel endpoint

1. Créer/modifier le fichier dans `app/api/v1/`
2. Définir le namespace et les modèles avec Flask-RESTX
3. Créer les classes Resource avec les méthodes HTTP
4. Ajouter les appels au Facade
5. Enregistrer le namespace dans `app/__init__.py`

### Ajouter un nouveau modèle

1. Créer le fichier dans `app/models/`
2. Hériter de `BaseModel`
3. Définir les attributs et validations dans `__init__`
4. Implémenter `to_dict()` et `update()` si nécessaire
5. Ajouter les méthodes correspondantes dans le Facade

## 📄 Licence

Ce projet a été développé dans le cadre du programme Holberton School.

## 👤 Auteur

**LEROY Yanis**
- GitHub: [@LEROY-Yanis](https://github.com/LEROY-Yanis)

## 🙏 Remerciements

- Holberton School pour le framework pédagogique
- La communauté Flask pour l'excellent framework
