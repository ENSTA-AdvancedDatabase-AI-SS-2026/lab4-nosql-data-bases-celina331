////////////////////////////////////////////////////////////
// TP4 - Exercice 3 : Algorithmes de Graphe (GDS)
////////////////////////////////////////////////////////////


// ─── 3.1 : Plus court chemin ─────────────────────────────
MATCH p = shortestPath(
  (a:Etudiant {prenom: "Ahmed"})-[:CONNAIT*..10]-(b:Etudiant {prenom: "Yasmina"})
)
RETURN
[
  n IN nodes(p) |
  n.prenom + " (" + n.universite + ")"
] AS chemin,
length(p) AS distance;


// ─── 3.2 : Centralité de degré ───────────────────────────

// Création du graphe projeté
CALL gds.graph.project(
  'reseau_social',
  'Etudiant',
  'CONNAIT'
);

// Calcul degré (top connectés)
CALL gds.degree.stream('reseau_social')
YIELD nodeId, score
RETURN
gds.util.asNode(nodeId).prenom AS etudiant,
gds.util.asNode(nodeId).universite AS universite,
score AS nb_connexions
ORDER BY nb_connexions DESC
LIMIT 10;


// ─── 3.3 : Détection de communautés (Louvain) ────────────

CALL gds.louvain.stream('reseau_social')
YIELD nodeId, communityId
WITH communityId, collect(gds.util.asNode(nodeId).prenom) AS membres
RETURN
communityId,
size(membres) AS taille_communaute,
membres[0..5] AS exemples
ORDER BY taille_communaute DESC;


// ─── 3.4 : Recommandation de contacts ─────────────────────

MATCH (moi:Etudiant {prenom: "Ahmed"})-[:CONNAIT]-(ami:Etudiant)
WITH moi, collect(DISTINCT ami) AS amis

MATCH (suggestion:Etudiant)
WHERE suggestion <> moi
AND NOT (moi)-[:CONNAIT]-(suggestion)

// amis en commun
OPTIONAL MATCH (moi)-[:CONNAIT]-(a1:Etudiant)-[:CONNAIT]-(suggestion)
WITH moi, suggestion, count(a1) AS amis_communs

// même filière bonus
WITH moi, suggestion, amis_communs,
CASE WHEN moi.filiere = suggestion.filiere THEN 1 ELSE 0 END AS meme_filiere

// score final
WITH suggestion,
(amis_communs * 3 + meme_filiere) AS score

RETURN
suggestion.prenom AS suggestion,
suggestion.universite AS universite,
score
ORDER BY score DESC
LIMIT 5;


// ─── 3.5 : Chemin de compétences ─────────────────────────

MATCH path = (c:Cours)-[:REQUIERT*]->(comp:Competence {nom: "Machine Learning"})
RETURN
[
  n IN nodes(path) |
  CASE
    WHEN n:Cours THEN n.intitule
    ELSE n.nom
  END
] AS parcours_apprentissage;


// ─── Nettoyage graphe projeté ────────────────────────────
CALL gds.graph.drop('reseau_social');
