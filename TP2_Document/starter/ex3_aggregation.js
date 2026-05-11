/**
 * TP2 - Exercice 3 : Pipelines d'Agrégation
 * Use Case : Statistiques médicales HealthCare DZ
 */

use("medical_db");

// ─── 3.1 : Distribution des diagnostics par wilaya ────────────────────────────

print("=== 3.1 : Top diagnostics par wilaya ===");

const diagParWilaya = db.patients.aggregate([

  // Décomposer les consultations
  {
    $unwind: "$consultations"
  },

  // Grouper par wilaya + diagnostic
  {
    $group: {
      _id: {
        wilaya: "$adresse.wilaya",
        diagnostic: "$consultations.diagnostic"
      },

      total: {
        $sum: 1
      }
    }
  },

  // Trier par nombre décroissant
  {
    $sort: {
      total: -1
    }
  },

  // Limiter aux 20 premiers
  {
    $limit: 20
  }

]).toArray();

printjson(diagParWilaya);


// ─── 3.2 : Médicament le plus prescrit par spécialité ─────────────────────────

print("\n=== 3.2 : Top médicaments par spécialité ===");

const medsParSpecialite = db.patients.aggregate([

  // Décomposer consultations
  {
    $unwind: "$consultations"
  },

  // Décomposer médicaments
  {
    $unwind: "$consultations.medicaments"
  },

  // Grouper par spécialité + médicament
  {
    $group: {

      _id: {
        specialite: "$consultations.medecin.specialite",
        medicament: "$consultations.medicaments.nom"
      },

      total: {
        $sum: 1
      }
    }
  },

  // Trier
  {
    $sort: {
      total: -1
    }
  }

]).toArray();

printjson(medsParSpecialite);


// ─── 3.3 : Évolution mensuelle des consultations ──────────────────────────────

print("\n=== 3.3 : Consultations par mois (12 derniers mois) ===");

const evolutionMensuelle = db.patients.aggregate([

  {
    $unwind: "$consultations"
  },

  {
    $match: {
      "consultations.date": {
        $gte: new Date(
          new Date().setFullYear(
            new Date().getFullYear() - 1
          )
        )
      }
    }
  },

  // Grouper par année + mois
  {
    $group: {

      _id: {
        annee: {
          $year: "$consultations.date"
        },

        mois: {
          $month: "$consultations.date"
        }
      },

      totalConsultations: {
        $sum: 1
      }
    }
  },

  // Trier
  {
    $sort: {
      "_id.annee": 1,
      "_id.mois": 1
    }
  },

  // Formatter YYYY-MM
  {
    $project: {

      _id: 0,

      date: {
        $concat: [
          { $toString: "$_id.annee" },
          "-",
          {
            $cond: [
              { $lt: ["$_id.mois", 10] },
              { $concat: ["0", { $toString: "$_id.mois" }] },
              { $toString: "$_id.mois" }
            ]
          }
        ]
      },

      totalConsultations: 1
    }
  }

]).toArray();

printjson(evolutionMensuelle);


// ─── 3.4 : Patients à risque multiple ────────────────────────────────────────

print("\n=== 3.4 : Profil patients à risque élevé ===");

const patientsRisque = db.patients.aggregate([

  {
    $match: {

      antecedents: {
        $all: ["Diabète type 2", "HTA"]
      },

      $expr: {
        $gt: [

          {
            $dateDiff: {
              startDate: "$dateNaissance",
              endDate: new Date(),
              unit: "year"
            }
          },

          60
        ]
      }
    }
  },

  // Ajouter âge + nombre consultations
  {
    $addFields: {

      age: {
        $dateDiff: {
          startDate: "$dateNaissance",
          endDate: new Date(),
          unit: "year"
        }
      },

      nbConsultations: {
        $size: "$consultations"
      }
    }
  },

  // Statistiques globales
  {
    $group: {

      _id: null,

      totalPatients: {
        $sum: 1
      },

      ageMoyen: {
        $avg: "$age"
      },

      consultationsMoyennes: {
        $avg: "$nbConsultations"
      }
    }
  }

]).toArray();

printjson(patientsRisque);


// ─── 3.5 : Rapport médecins ───────────────────────────────────────────────────

print("\n=== 3.5 : Top 5 médecins & taux de ré-consultation ===");

const rapportMedecins = db.patients.aggregate([

  {
    $unwind: "$consultations"
  },

  // Grouper par médecin
  {
    $group: {

      _id: "$consultations.medecin.nom",

      patients_uniques: {
        $addToSet: "$_id"
      },

      total_consultations: {
        $sum: 1
      }
    }
  },

  // Calculer nombre patients uniques
  {
    $addFields: {

      nb_patients_uniques: {
        $size: "$patients_uniques"
      }
    }
  },

  // Calcul taux de ré-consultation
  {
    $addFields: {

      taux_reconsultation: {

        $multiply: [

          {
            $divide: [

              {
                $subtract: [
                  "$total_consultations",
                  "$nb_patients_uniques"
                ]
              },

              "$nb_patients_uniques"
            ]
          },

          100
        ]
      }
    }
  },

  // Trier
  {
    $sort: {
      total_consultations: -1
    }
  },

  // Top 5
  {
    $limit: 5
  }

]).toArray();

printjson(rapportMedecins);
