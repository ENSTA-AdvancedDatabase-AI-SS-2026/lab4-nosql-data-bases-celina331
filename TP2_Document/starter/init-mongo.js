// MongoDB initialization script

db = db.getSiblingDB('medical_db');


// Créer utilisateur MongoDB

try {

  db.createUser({
    user: 'medical_user',
    pwd: 'medical123',

    roles: [
      {
        role: 'readWrite',
        db: 'medical_db'
      }
    ]
  });

  print('✅ Utilisateur créé');

} catch (e) {

  print('⚠️ Utilisateur existe déjà');
}


// Créer collections

db.createCollection('patients');

db.createCollection('analyses');


print('✅ medical_db initialized successfully');
