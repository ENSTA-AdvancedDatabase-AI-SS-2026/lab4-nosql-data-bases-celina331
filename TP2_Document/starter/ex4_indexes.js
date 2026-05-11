/**
 * TP2 - Exercice 4 : Index et Optimisation
 */

use("medical_db");

// ─── 4.1 : Créer les index appropriés ────────────────────────────────────────


// ✅ Index 1 : Recherche fréquente par wilaya + antécédents

db.patients.createIndex({
  "adresse.wilaya": 1,
  antecedents: 1
});


// ✅ Index 2 : Recherche par date de consultation

db.patients.createIndex({
  "consultations.date": -1
});


// ✅ Index 3 : Recherche Full-Text sur les diagnostics

db.patients.createIndex({
  "consultations.diagnostic": "text"
});


// ✅ Index 4 : Analyses par patient (lookup)

db.analyses.createIndex({
  patient_id: 1
});


// ─── 4.2 : Comparer avec explain() ────────────────────────────────────────────


// Requête de test

const requeteTest = {

  "adresse.wilaya": "Alger",

  antecedents: "Diabète type 2"
};


print("=== EXPLAIN AVEC INDEX ===");

const explainResult = db.patients.find(requeteTest)
  .explain("executionStats");


// Affichage des statistiques importantes

print("Documents retournés :", explainResult.executionStats.nReturned);

print("Documents examinés :", explainResult.executionStats.totalDocsExamined);

print("Temps d'exécution (ms) :",
  explainResult.executionStats.executionTimeMillis);

print("Index utilisé :");

printjson(
  explainResult.queryPlanner.winningPlan
);


// ─── 4.3 : Recherche Full-Text ────────────────────────────────────────────────

print("\n=== Recherche Full-Text ===");

const rechercheTexte = db.patients.find({

  $text: {
    $search: "Hypertension"
  }

}).toArray();

printjson(rechercheTexte);


// ─── 4.4 : Index TTL pour archivage ───────────────────────────────────────────


// 5 ans = 5 × 365 × 24 × 60 × 60

db.analyses.createIndex(

  { date: 1 },

  {
    expireAfterSeconds: 157680000
  }

);


print("\n✅ Tous les index ont été créés.");
