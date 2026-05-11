# 📘 RAPPORT.md — TP4 Neo4j
## UniConnect DZ — Réseau Social Universitaire

---

# 📖 1. Schéma du graphe

Le graphe modélise un réseau social universitaire composé de :

## 🧩 Nœuds (Nodes)

- **Etudiant**
  - id
  - prenom
  - nom
  - universite
  - filiere
  - annee
  - ville

- **Cours**
  - code
  - intitule
  - credits
  - departement

- **Competence**
  - nom
  - categorie

- **Club**
  - nom
  - universite
  - domaine

- **Entreprise**
  - nom
  - secteur
  - ville

---

## 🔗 Relations

- (Etudiant)-[:CONNAIT]->(Etudiant)
- (Etudiant)-[:SUIT]->(Cours)
- (Etudiant)-[:MEMBRE_DE]->(Club)
- (Etudiant)-[:MAITRISE]->(Competence)
- (Cours)-[:REQUIERT]->(Competence)
- (Etudiant)-[:A_STAGE_CHEZ]->(Entreprise)

---

## 🖼️ Représentation logique (diagramme)

```
Etudiant ── CONNAIT ──> Etudiant
    │
    ├── SUIT ────────> Cours ─── REQUIERT ───> Competence
    │
    ├── MAITRISE ────> Competence
    │
    ├── MEMBRE_DE ───> Club
    │
    └── A_STAGE_CHEZ ─> Entreprise
```

---

# 👥 2. Résultats de l’algorithme de communautés (Louvain)

## ⚙️ Algorithme utilisé :
- Louvain Community Detection (Neo4j GDS)

---

## 📊 Résultats observés :

L’algorithme a détecté plusieurs communautés principales :

### 🟦 Communauté 1 — Informatique / USTHB
- Ahmed
- Fatima
- étudiants USTHB
- forte connexion sur cours INFO401 / INFO402

👉 Interprétation :
Groupe centré sur la filière Informatique avec forte interaction académique.

---

### 🟩 Communauté 2 — Université UMBB
- étudiants de Boumerdes
- forte densité de relations CONNAIT internes

👉 Interprétation :
Communauté géographique + universitaire.

---

### 🟨 Communauté 3 — Université USTO
- étudiants Oran
- connexions autour de projets et clubs

---

### 🟥 Communauté 4 — Compétences IA
- étudiants maîtrisant Machine Learning
- Deep Learning
- forte corrélation avec cours INFO402

---

## 📌 Conclusion communautés

- Les communautés sont formées principalement par :
  - université
  - filière
  - compétences communes
- L’algorithme Louvain est efficace pour détecter :
  - groupes sociaux naturels
  - clusters académiques

---

# ⚖️ 3. Comparaison SQL vs Cypher

## 🔍 Cas : "Trouver les amis d’Ahmed et ses amis d’amis"

---

## 🧾 Version SQL

```sql
SELECT e2.*
FROM Etudiant e1
JOIN CONNAIT c1 ON e1.id = c1.id_etudiant1
JOIN Etudiant e2 ON c1.id_etudiant2 = e2.id

LEFT JOIN CONNAIT c2 ON e2.id = c2.id_etudiant1
LEFT JOIN Etudiant e3 ON c2.id_etudiant2 = e3.id

WHERE e1.prenom = 'Ahmed';
```

---

## ❌ Problèmes SQL

- ❌ beaucoup de JOINs
- ❌ complexité élevée (O(n²))
- ❌ difficile à maintenir
- ❌ performances faibles sur grands volumes
- ❌ pas naturel pour relations profondes

---

## 📊 Version Cypher

```cypher
MATCH (a:Etudiant {prenom: "Ahmed"})-[:CONNAIT*2]-(b)
RETURN b;
```

---

## ✅ Avantages Cypher

- ✔ syntaxe simple
- ✔ très lisible
- ✔ expressif (graph traversal naturel)
- ✔ performant sur relations profondes
- ✔ pas de JOIN complexe

---

## 📌 Comparaison finale

| Critère        | SQL ❌ | Cypher ✅ |
|----------------|--------|----------|
| Lisibilité     | Faible | Très élevée |
| Complexité     | Élevée | Faible |
| Performance graphe | Mauvaise | Optimisée |
| Requêtes multi-hop | Difficile | Naturel |

---

# 🏁 Conclusion générale

Neo4j est particulièrement adapté pour :

- réseaux sociaux
- recommandations
- analyse de communautés
- relations complexes multi-niveaux

---

## 🚀 Résultat final du TP

Le système UniConnect DZ permet :

- détection automatique de communautés
- recommandation d’étudiants
- analyse des parcours académiques
- exploration rapide des relations

---

# 📌 Bonus appris

- Cypher est plus intuitif que SQL pour les graphes
- GDS permet des analyses avancées (Louvain, PageRank)
- les graphes modélisent naturellement les relations humaines
