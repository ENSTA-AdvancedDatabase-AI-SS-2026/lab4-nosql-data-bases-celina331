
````markdown
# 📘 TP3 — Cassandra : SmartGrid DZ
## IoT Électrique & Traitement des données temps réel

---

# 📖 Contexte du projet

SmartGrid DZ est un système IoT de gestion de réseau électrique basé sur Cassandra.

Le système gère :
- 10 000 capteurs électriques
- mesures toutes les minutes
- alertes temps réel
- agrégations pour dashboard

Objectif : stocker et analyser des données massives en temps réel.

---

# 🎯 Objectifs du TP

- Concevoir un schéma Cassandra optimisé
- Gérer les séries temporelles IoT
- Éviter les hot partitions
- Comprendre ALLOW FILTERING
- Comparer les stratégies de compaction

---

# 🧱 1. Modélisation des données

---

## ⚡ 1.1 Table mesures_par_capteur

### PRIMARY KEY :
```sql
PRIMARY KEY ((capteur_id, date_jour), timestamp)
```

---

### 📌 Justification

#### Partition Key :
```text
(capteur_id, date_jour)
```

✔ Permet :
- distribution des données
- séparation journalière
- évite les hot partitions

---

### ⚠️ Problème évité

Sans `date_jour` :
- un capteur actif devient une **hot partition**
- surcharge disque et CPU
- lenteur des lectures

---

### ✔ Solution adoptée

Ajout de :
- capteur_id
- date_jour

👉 permet de découper les données par jour

---

## ⚡ 1.2 Table alertes_par_wilaya

### PRIMARY KEY :
```sql
PRIMARY KEY ((wilaya, date_jour), timestamp, capteur_id)
```

---

### 📌 Justification

✔ Partition par :
- wilaya
- jour

✔ Avantages :
- requêtes rapides par région
- séparation temporelle

---

### ⚠️ Sans date_jour :
- toutes les alertes dans une seule partition
- saturation rapide

---

## ⚡ 1.3 Table agregats_horaires

### PRIMARY KEY :
```sql
PRIMARY KEY (wilaya, date_heure)
```

---

✔ Usage :
- dashboard temps réel
- lecture rapide des stats

---

# ⚠️ 2. ALLOW FILTERING

---

## 📌 Définition

Force Cassandra à scanner toutes les partitions.

---

## ❌ Pourquoi c’est dangereux ?

### ⚠️ 1. Performance faible
- full scan cluster

### ⚠️ 2. Non scalable
- ralentissement avec volume

### ⚠️ 3. Perte de performance Cassandra
- contourne le modèle clé-valeur

### ⚠️ 4. CPU élevé
- surcharge nodes

---

## ✔ Conclusion

👉 ALLOW FILTERING = interdit en production  
👉 seulement pour tests

---

# ⚙️ 3. Stratégies de compaction

---

## 🧩 3.1 STCS

✔ Avantages :
- rapide en écriture

❌ Inconvénients :
- lecture lente

👉 utilisé pour batch write

---

## ⏳ 3.2 TWCS

✔ Avantages :
- parfait pour données temporelles
- suppression automatique ancienne data

👉 BEST CHOICE IoT (SmartGrid DZ)

---

## 📦 3.3 LCS

✔ Avantages :
- lecture très rapide

❌ Inconvénients :
- écriture coûteuse

👉 utilisé pour OLTP

---

## 📊 Comparaison

| Type | Lecture | Écriture | Usage |
|------|--------|----------|------|
| STCS | ❌ faible | ✔ excellent | batch |
| TWCS | ✔ bon | ✔ bon | IoT |
| LCS | ✔ excellent | ❌ coûteux | OLTP |

---

# 🚀 4. Ingestion IoT (TP2 script)

Le système permet :
- ingestion de 10 000 capteurs
- simulation de données réalistes
- batch processing Cassandra
- débit élevé (mesures/sec)

---

# 🧠 Conclusion générale

Ce projet montre que Cassandra est adapté pour :

- IoT massifs
- données temps réel
- haute disponibilité
- scalabilité horizontale

---

# 📌 Recommandations finales

✔ Utiliser TWCS pour séries temporelles  
✔ Toujours inclure une partition temporelle  
✔ Éviter ALLOW FILTERING  
✔ Batch UNLOGGED pour ingestion rapide  
✔ Préparer les requêtes avant le design (query-driven design)

---

# 🏁 Résultat final

SmartGrid DZ permet :

- stockage distribué massif
- traitement temps réel IoT
- performance stable même à grande échelle
````
