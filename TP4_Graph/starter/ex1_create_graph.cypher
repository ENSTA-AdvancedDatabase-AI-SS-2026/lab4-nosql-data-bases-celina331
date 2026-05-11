////////////////////////////////////////////////////////////
// TP4 - Exercice 1 : Création du graphe UniConnect DZ
////////////////////////////////////////////////////////////

// ─── Nettoyage base ──────────────────────────────────────
MATCH (n) DETACH DELETE n;


// ─── 1.1 : Contraintes d’unicité ──────────────────────────
CREATE CONSTRAINT etudiant_id IF NOT EXISTS
FOR (e:Etudiant)
REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT cours_code IF NOT EXISTS
FOR (c:Cours)
REQUIRE c.code IS UNIQUE;

CREATE CONSTRAINT competence_nom IF NOT EXISTS
FOR (c:Competence)
REQUIRE c.nom IS UNIQUE;


// ─── 1.2 : Compétences ────────────────────────────────────
UNWIND [
  {nom: "Python", categorie: "Programmation"},
  {nom: "Java", categorie: "Programmation"},
  {nom: "SQL", categorie: "Bases de Données"},
  {nom: "NoSQL", categorie: "Bases de Données"},
  {nom: "Machine Learning", categorie: "IA"},
  {nom: "Deep Learning", categorie: "IA"},
  {nom: "React", categorie: "Web"},
  {nom: "Docker", categorie: "DevOps"},
  {nom: "Linux", categorie: "Systèmes"},
  {nom: "Réseaux", categorie: "Infrastructure"}
] AS comp
MERGE (:Competence {nom: comp.nom, categorie: comp.categorie});


// ─── 1.3 : Cours ──────────────────────────────────────────
UNWIND [
  {code: "INFO401", intitule: "Bases de Données Avancées", credits: 6, dept: "Informatique"},
  {code: "INFO402", intitule: "Intelligence Artificielle", credits: 6, dept: "Informatique"},
  {code: "INFO403", intitule: "Développement Web", credits: 4, dept: "Informatique"},
  {code: "INFO404", intitule: "Systèmes Distribués", credits: 5, dept: "Informatique"},
  {code: "INFO405", intitule: "Cloud Computing", credits: 4, dept: "Informatique"}
] AS cours
MERGE (c:Cours {code: cours.code})
SET c += cours;


// ─── 1.4 : Étudiants (50 étudiants) ───────────────────────
UNWIND [
  {id:"E001", prenom:"Ahmed", nom:"Bensalem", universite:"USTHB", filiere:"Informatique", annee:3, ville:"Alger"},
  {id:"E002", prenom:"Fatima", nom:"Ouali", universite:"USTHB", filiere:"Informatique", annee:3, ville:"Alger"},
  {id:"E003", prenom:"Yasmina", nom:"Kaci", universite:"UMBB", filiere:"GL", annee:2, ville:"Boumerdes"},
  {id:"E004", prenom:"Karim", nom:"Meziane", universite:"USTO", filiere:"Informatique", annee:4, ville:"Oran"},
  {id:"E005", prenom:"Sara", nom:"Bouchareb", universite:"UMC", filiere:"Telecoms", annee:3, ville:"Constantine"}

  // 👉 tu peux compléter jusqu’à E050
] AS data
MERGE (e:Etudiant {id: data.id})
SET e += data;


// ─── 1.5 : Relations CONNAIT ─────────────────────────────
// Création de connexions sociales simples

MATCH (a:Etudiant {id:"E001"}), (b:Etudiant {id:"E002"})
MERGE (a)-[:CONNAIT {depuis:2023}]->(b);

MATCH (a:Etudiant {id:"E002"}), (b:Etudiant {id:"E003"})
MERGE (a)-[:CONNAIT {depuis:2022}]->(b);

MATCH (a:Etudiant {id:"E003"}), (b:Etudiant {id:"E004"})
MERGE (a)-[:CONNAIT {depuis:2024}]->(b);


// ─── 1.6 : Relations SUIT (cours) ─────────────────────────
MATCH (e:Etudiant), (c:Cours)
WHERE e.annee >= 2 AND c.code IN ["INFO401","INFO402"]
MERGE (e)-[:SUIT {semestre: 1, note: 10 + rand()*10}]->(c);


// ─── 1.7 : Relations MAITRISE ─────────────────────────────
MATCH (e:Etudiant)
WHERE e.filiere = "Informatique"
MATCH (c:Competence)
WHERE c.nom IN ["Python", "SQL", "Linux"]
MERGE (e)-[:MAITRISE {niveau: "intermédiaire"}]->(c);


// ─── Vérification finale ──────────────────────────────────
MATCH (n)
RETURN labels(n)[0] AS type, count(*) AS total
ORDER BY total DESC;

MATCH ()-[r]->()
RETURN type(r) AS relation, count(*) AS total
ORDER BY total DESC;
