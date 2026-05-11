````markdown id="l0vk7n"
# RAPPORT.md

# 📊 TP1 — Redis : Système de Cache E-commerce

## 👨‍💻 Projet : ShopFast Cache System

---

# 1️⃣ Comparaison de performance (Cache HIT vs Cache MISS)

## Cache MISS

Lorsqu’une donnée n’existe pas dans Redis :

1. L’application interroge PostgreSQL
2. La requête est lente (~2 secondes dans notre simulation)
3. La donnée est ensuite stockée dans Redis

### Résultat observé
- Temps moyen : ~2000 ms
- Forte latence
- Charge importante sur la base de données

---

## Cache HIT

Lorsque la donnée existe déjà dans Redis :

1. L’application lit directement depuis Redis
2. Aucun accès PostgreSQL n’est nécessaire

### Résultat observé
- Temps moyen : ~1 à 5 ms
- Réponse très rapide
- Réduction de la charge serveur

---

## Conclusion

Redis améliore fortement les performances du système.

Le pattern Cache-Aside permet :
- d’accélérer les accès fréquents,
- de réduire la charge PostgreSQL,
- d’améliorer l’expérience utilisateur.

---

# 2️⃣ Justification des choix de modélisation

---

## 🔹 String

Utilisé pour :
- cache simple,
- sessions utilisateur,
- compteurs.

### Pourquoi ?
Les Strings sont rapides, simples et optimisées pour les données courtes.

---

## 🔹 Hash

Utilisé pour :
- stockage des produits.

### Pourquoi ?
Les Hash permettent de stocker plusieurs champs dans une seule clé Redis.

Exemple :
```text
product:1
├── name
├── price
├── stock
```

Cela réduit le nombre de clés et facilite les mises à jour partielles.

---

## 🔹 List

Utilisé pour :
- historique de navigation.

### Pourquoi ?
Les Lists permettent :
- l’ajout rapide,
- l’ordre chronologique,
- la limitation de taille avec LTRIM.

---

## 🔹 Set

Utilisé pour :
- catégories produits,
- tags.

### Pourquoi ?
Les Sets évitent les doublons et permettent des opérations rapides comme :
- intersection,
- union,
- recherche.

---

## 🔹 Sorted Set

Utilisé pour :
- classement des meilleures ventes.

### Pourquoi ?
Les Sorted Sets permettent :
- le tri automatique,
- les classements temps réel,
- la récupération rapide du top N.

---

# 3️⃣ Réponses aux questions de réflexion

---

## ❓ Que se passe-t-il si Redis redémarre ?

Si Redis redémarre :

- les données en mémoire peuvent être perdues,
- sauf si la persistance est activée.

Dans ce TP :
- `appendonly yes`
- et les snapshots `save`

permettent de restaurer les données après redémarrage.

Cependant :
- certaines données récentes peuvent être perdues selon la configuration AOF/RDB.

---

## ❓ Comment gérer la cohérence cache/DB en cas d'accès concurrent ?

Plusieurs solutions existent :

### 1. Invalidation du cache
Après modification en base :
- supprimer la clé Redis,
- puis recharger au prochain accès.

### 2. Transactions Redis
Utiliser :
- MULTI
- EXEC

pour éviter les écritures concurrentes incohérentes.

### 3. TTL court
Permet d’éviter qu’une donnée obsolète reste trop longtemps dans le cache.

---

## ❓ Quand un TTL trop court est-il problématique ?

Un TTL trop court provoque :

- des expirations fréquentes,
- beaucoup de cache MISS,
- davantage de requêtes PostgreSQL.

Conséquences :
- surcharge base de données,
- augmentation de la latence,
- baisse des performances.

Exemple :
- TTL = 1 seconde
→ les données expirent presque immédiatement.

Il faut choisir un TTL équilibré selon :
- la fréquence des mises à jour,
- la criticité des données,
- le trafic utilisateur.

---

# ✅ Conclusion générale

Redis est très efficace pour :
- accélérer les applications,
- gérer les sessions,
- construire des systèmes temps réel.

Le TP a permis de manipuler :
- les principales structures Redis,
- le pattern Cache-Aside,
- les classements temps réel,
- les pipelines et transactions.
````
