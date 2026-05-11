/**
 * TP2 - Exercice 1 : Modélisation MongoDB
 * Use Case : HealthCare DZ - Dossiers Médicaux
 */

// Se connecter à la base médicale
use("medical_db");

// ─── 1.1 : Créer la collection avec validation ────────────────────────────────

db.createCollection("patients", {
  validator: {
    $jsonSchema: {
      bsonType: "object",

      required: [
        "cin",
        "nom",
        "prenom",
        "dateNaissance",
        "sexe"
      ],

      properties: {

        cin: {
          bsonType: "string",
          description: "CIN obligatoire"
        },

        nom: {
          bsonType: "string",
          description: "Nom obligatoire"
        },

        prenom: {
          bsonType: "string",
          description: "Prénom obligatoire"
        },

        dateNaissance: {
          bsonType: "date",
          description: "Date de naissance obligatoire"
        },

        sexe: {
          enum: ["M", "F"],
          description: "Sexe doit être M ou F"
        },

        adresse: {
          bsonType: "object",
          properties: {

            wilaya: {
              bsonType: "string"
            },

            commune: {
              bsonType: "string"
            }
          }
        },

        groupeSanguin: {
          bsonType: "string"
        },

        antecedents: {
          bsonType: "array",
          items: {
            bsonType: "string"
          }
        },

        allergies: {
          bsonType: "array",
          items: {
            bsonType: "string"
          }
        },

        consultations: {
          bsonType: "array",

          items: {
            bsonType: "object",

            required: [
              "date",
              "medecin",
              "diagnostic"
            ],

            properties: {

              date: {
                bsonType: "date"
              },

              medecin: {
                bsonType: "object",

                properties: {

                  nom: {
                    bsonType: "string"
                  },

                  specialite: {
                    bsonType: "string"
                  }
                }
              },

              diagnostic: {
                bsonType: "string"
              },

              tension: {
                bsonType: "object",

                properties: {

                  systolique: {
                    bsonType: "int"
                  },

                  diastolique: {
                    bsonType: "int"
                  }
                }
              },

              medicaments: {
                bsonType: "array",

                items: {
                  bsonType: "object",

                  properties: {

                    nom: {
                      bsonType: "string"
                    },

                    dosage: {
                      bsonType: "string"
                    },

                    duree: {
                      bsonType: "string"
                    }
                  }
                }
              },

              notes: {
                bsonType: "string"
              }
            }
          }
        }
      }
    }
  }
});

// ─── 1.2 : Insérer des patients avec données algériennes ──────────────────────

const patients = [

  {
    cin: "198001012300",
    nom: "Bensalem",
    prenom: "Ahmed",
    dateNaissance: new Date("1980-01-01"),
    sexe: "M",

    adresse: {
      wilaya: "Alger",
      commune: "Bab Ezzouar"
    },

    groupeSanguin: "O+",

    antecedents: [
      "Diabète type 2",
      "HTA"
    ],

    allergies: [
      "Pénicilline"
    ],

    consultations: [

      {
        date: new Date("2024-01-15"),

        medecin: {
          nom: "Dr. Mansouri",
          specialite: "Cardiologie"
        },

        diagnostic: "Hypertension artérielle",

        tension: {
          systolique: 145,
          diastolique: 92
        },

        medicaments: [
          {
            nom: "Amlodipine",
            dosage: "5mg",
            duree: "30 jours"
          }
        ],

        notes: "Surveillance tensionnelle recommandée"
      },

      {
        date: new Date("2024-08-20"),

        medecin: {
          nom: "Dr. Benali",
          specialite: "Médecine générale"
        },

        diagnostic: "Diabète contrôlé",

        tension: {
          systolique: 130,
          diastolique: 85
        },

        medicaments: [
          {
            nom: "Metformine",
            dosage: "850mg",
            duree: "60 jours"
          }
        ],

        notes: "Continuer régime alimentaire"
      }
    ]
  },

  {
    cin: "199505101122",
    nom: "Kaci",
    prenom: "Sonia",
    dateNaissance: new Date("1995-05-10"),
    sexe: "F",

    adresse: {
      wilaya: "Oran",
      commune: "Es Senia"
    },

    groupeSanguin: "A+",

    antecedents: [
      "Asthme"
    ],

    allergies: [],

    consultations: [

      {
        date: new Date("2023-11-11"),

        medecin: {
          nom: "Dr. Rahmani",
          specialite: "Pneumologie"
        },

        diagnostic: "Crise d'asthme légère",

        medicaments: [
          {
            nom: "Ventoline",
            dosage: "2 bouffées",
            duree: "7 jours"
          }
        ],

        notes: "Éviter les allergènes"
      }
    ]
  },

  {
    cin: "197712250987",
    nom: "Meziane",
    prenom: "Karim",
    dateNaissance: new Date("1977-12-25"),
    sexe: "M",

    adresse: {
      wilaya: "Constantine",
      commune: "El Khroub"
    },

    groupeSanguin: "B+",

    antecedents: [
      "HTA"
    ],

    allergies: [
      "Aspirine"
    ],

    consultations: [

      {
        date: new Date("2024-02-18"),

        medecin: {
          nom: "Dr. Saidi",
          specialite: "Cardiologie"
        },

        diagnostic: "Tension élevée",

        tension: {
          systolique: 150,
          diastolique: 95
        },

        medicaments: [
          {
            nom: "Losartan",
            dosage: "50mg",
            duree: "30 jours"
          }
        ],

        notes: "Réduire le sel"
      }
    ]
  }

];

// Insertion des patients
db.patients.insertMany(patients);

// ─── 1.3 : Collection analyses (référencée) ───────────────────────────────────

const patientAhmed = db.patients.findOne({ cin: "198001012300" });
const patientSonia = db.patients.findOne({ cin: "199505101122" });

const analyses = [

  {
    patient_id: patientAhmed._id,

    type: "Glycémie",

    date: new Date("2024-01-20"),

    resultat: {
      valeur: 1.25,
      unite: "g/L"
    },

    laboratoire: "Laboratoire El Hikma"
  },

  {
    patient_id: patientAhmed._id,

    type: "ECG",

    date: new Date("2024-03-10"),

    resultat: {
      conclusion: "Normal"
    },

    laboratoire: "Clinique Cardio Alger"
  },

  {
    patient_id: patientSonia._id,

    type: "NFS",

    date: new Date("2024-05-01"),

    resultat: {
      hemoglobine: 13.2
    },

    laboratoire: "Laboratoire Ibn Sina"
  }

];

// Insertion des analyses
db.analyses.insertMany(analyses);

print("✅ Modélisation terminée");
print("✅ Patients insérés :", db.patients.countDocuments());
print("✅ Analyses insérées :", db.analyses.countDocuments());
