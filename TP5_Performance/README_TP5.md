# 📘 TP5 — Performance & Optimisation NoSQL
## Benchmark Comparatif : Redis vs MongoDB vs Cassandra vs Neo4j

---

# 📖 Contexte

Dans ce projet, nous comparons 4 bases NoSQL majeures :

- 🟥 Redis (cache in-memory)
- 🟩 MongoDB (document store)
- 🟦 Cassandra (wide-column store)
- 🟪 Neo4j (graph database)

Objectif : déterminer la meilleure technologie selon les workloads.

---

# 🎯 Objectifs

- Mesurer performances réelles (write/read)
- Analyser latence (P50, P95, P99)
- Tester la scalabilité sous charge
- Identifier les cas d’usage optimaux

---

# ⚙️ 1. Benchmark Écriture

## 📌 Méthodologie

- 100 000 insertions par base
- mesure :
  - débit (req/sec)
  - latence moyenne
  - mémoire utilisée

---

## 📊 Résultats observés

| Base | Débit écriture | Latence | Observations |
|------|---------------|---------|--------------|
| Redis | 🔥 Très élevé | Très faible | In-memory |
| MongoDB | 🟢 Élevé | Moyen | Index + journaling |
| Cassandra | 🔥 Très élevé | Faible | write-optimized |
| Neo4j | 🟡 Moyen | Moyen | graphe coûteux |

---

## 📌 Analyse

- Redis et Cassandra dominent en écriture
- MongoDB est équilibré
- Neo4j est plus lent (relations complexes)

---

# 📖 2. Benchmark Lecture

## 📌 Types de requêtes

- Point lookup (clé unique)
- Range query (intervalle)
- Requête complexe (aggregation / traversal)

---

## 📊 Résultats

| Base | Lookup | Range | Complex |
|------|--------|-------|---------|
| Redis | ⚡ ultra rapide | ❌ limité | ❌ |
| MongoDB | 🟢 rapide | 🟢 bon | 🟢 très bon |
| Cassandra | 🟢 rapide | 🔥 excellent | ❌ limité |
| Neo4j | 🟢 bon | ❌ faible | 🔥 excellent |

---

## 📌 Analyse

- Redis = cache pur
- Cassandra = time-series / range queries
- MongoDB = polyvalent
- Neo4j = top pour relations complexes

---

# ⚡ 3. Test de charge concurrente

## 📌 Setup

- 50 clients simultanés
- 200 requêtes par client

---

## 📊 Résultats

| Base | Comportement sous charge |
|------|--------------------------|
| Redis | stable (in-memory) |
| MongoDB | légère dégradation |
| Cassandra | très stable |
| Neo4j | dégradation sur traversals |

---

## 📌 Analyse

- Cassandra = meilleure scalabilité horizontale
- Redis = très stable mais RAM limité
- MongoDB = sensible aux locks/IO
- Neo4j = CPU-bound sur graph traversal

---

# 📊 4. Tableau de décision final

| Critère | Redis | MongoDB | Cassandra | Neo4j |
|---------|------|--------|----------|------|
| Débit écriture | 🔥🔥🔥 | 🔥🔥 | 🔥🔥🔥 | 🔥 |
| Débit lecture | 🔥🔥🔥 | 🔥🔥 | 🔥🔥 | 🔥 |
| Requêtes complexes | ❌ | 🔥🔥 | ❌ | 🔥🔥🔥 |
| Scalabilité | 🔥🔥 | 🔥🔥 | 🔥🔥🔥 | 🔥 |
| Latence | ⚡ très faible | faible | faible | moyenne |

---

# 🧠 5. Analyse globale

## 🟥 Redis
✔ Cache ultra rapide  
✔ In-memory only  
❌ pas adapté persistance complexe  

👉 Use case : cache, session, leaderboard

---

## 🟩 MongoDB
✔ Flexible JSON  
✔ bon équilibre lecture/écriture  
✔ requêtes riches  

👉 Use case : applications web, APIs

---

## 🟦 Cassandra
✔ énorme scalabilité  
✔ write performance exceptionnelle  
✔ time-series optimal  

👉 Use case : IoT, logs, big data

---

## 🟪 Neo4j
✔ meilleur pour graphes  
✔ recommandations puissantes  
✔ traversals rapides  

👉 Use case : réseaux sociaux, recommandations

---

# 🏁 Conclusion

Chaque base a un rôle spécifique :

- Redis → cache ultra rapide
- MongoDB → polyvalent généraliste
- Cassandra → données massives + IoT
- Neo4j → relations complexes

---

# 🚀 Recommandation finale

👉 Il n’existe pas une meilleure base unique  
👉 Le choix dépend du workload :

- Cache → Redis
- Web App → MongoDB
- IoT / logs → Cassandra
- Graph / AI social → Neo4j

---

# 📌 Résultat du TP

Ce benchmark montre que :

✔ performance dépend du modèle de données  
✔ NoSQL ≠ remplacement SQL mais spécialisation  
✔ architecture moderne = multi-database (polyglot persistence)
