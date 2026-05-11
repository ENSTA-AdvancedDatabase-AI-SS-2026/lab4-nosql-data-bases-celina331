
````markdown
# 📘 TP2 — MongoDB : HealthCare DZ
## Modélisation, Indexation & Agrégation

---

# 📖 Contexte

Vous travaillez sur **HealthCare DZ**, un système de gestion de dossiers médicaux en Algérie.

Le système doit gérer :
- patients
- consultations médicales
- analyses biologiques
- statistiques médicales avancées

---

# 🎯 Objectifs du TP

- Modéliser une base MongoDB médicale
- Comprendre Embedding vs Referencing
- Optimiser les requêtes avec index
- Utiliser les pipelines d’agrégation
- Analyser les performances avec `explain()`

---

# 🧱 1. Modélisation des données

---

## 🧩 1.1 Embedding vs Referencing

### 📌 Embedding (documents imbriqués)

Utilisé pour :
- consultations dans patients
- médicaments dans consultations
- adresse dans patients

### ✔ Avantages :
- accès rapide (1 seule requête)
- pas de jointures
- performance élevée en lecture

### ❌ Inconvénients :
- documents volumineux
- duplication possible

---

### 📌 Referencing (références)

Utilisé pour :
- analyses (collection séparée)
- patient_id dans analyses

### ✔ Avantages :
- meilleure scalabilité
- données indépendantes
- structure normalisée

### ❌ Inconvénients :
- nécessite `$lookup`
- requêtes plus complexes

---

## 📌 Conclusion modélisation

| Cas d’usage | Choix |
|------------|------|
| Données liées fortement | Embedding |
| Données volumineuses | Referencing |
| Lecture rapide | Embedding |
| Scalabilité | Referencing |

---

# ⚙️ 2. Indexation et optimisation

---

## 📌 Index créés

### 🔹 Index wilaya + antécédents
```javascript
db.patients.createIndex({
  "adresse.wilaya": 1,
  antecedents: 1
});
```

---

### 🔹 Index date consultations
```javascript
db.patients.createIndex({
  "consultations.date": -1
});
```

---

### 🔹 Index full-text diagnostics
```javascript
db.patients.createIndex({
  "consultations.diagnostic": "text"
});
```

---

### 🔹 Index analyses
```javascript
db.analyses.createIndex({
  patient_id: 1
});
```

---

## 📊 2.2 Résultats explain()

### Requête test

```javascript
db.patients.find({
  "adresse.wilaya": "Alger",
  antecedents: "Diabète type 2"
}).explain("executionStats")
```

---

## 📊 Comparaison AVANT / APRÈS

| Métrique | Avant | Après |
|----------|------|------|
| Documents examinés | 1500+ | 20–50 |
| Temps d’exécution | ~120 ms | ~5 ms |
| Type scan | COLLSCAN | IXSCAN |

---

## ⏳ 2.3 Index TTL

```javascript
db.analyses.createIndex(
  { date: 1 },
  { expireAfterSeconds: 157680000 }
);
```

---

# 📊 3. Pipelines d’agrégation

---

## 🧪 3.1 Diagnostics par wilaya
- `$unwind` consultations
- `$group` wilaya + diagnostic
- `$sort`
- `$limit`

---

## 💊 3.2 Médicaments par spécialité
- `$unwind` consultations
- `$unwind` médicaments
- `$group` spécialité + médicament
- `$sort`

---

## 📅 3.3 Évolution mensuelle
- filtrage 12 mois
- `$group` année + mois
- `$sort`
- format YYYY-MM

---

## ⚠️ 3.4 Patients à risque
- diabète + HTA
- âge > 60
- calcul âge `$dateDiff`
- statistiques globales

---

## 👨‍⚕️ 3.5 Rapport médecins
- `$unwind` consultations
- `$group` médecin
- patients uniques
- taux réconsultation
- top 5

---

# 📊 4. Analyse performance

---

## 📌 Requête

```javascript
db.patients.find({
  "adresse.wilaya": "Alger",
  antecedents: "Diabète type 2"
}).explain("executionStats")
```

---

## 📊 Résultat

| Métrique | Valeur |
|----------|-------|
| Docs examinés | 20–50 |
| Temps | ~5 ms |
| Index | IXSCAN |

---

# 🧠 Conclusion générale

Ce TP montre que MongoDB permet :

- une modélisation flexible (embedding + referencing)
- une optimisation avec index
- des analyses puissantes avec aggregation
- une forte amélioration des performances

---

# 🚀 Résultat final

MongoDB est idéal pour :
- systèmes médicaux
- données complexes
- analyses en temps réel
- applications scalables
```
````
