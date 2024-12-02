-- Insertion des données dans la table hauteurDebitCrues
INSERT INTO hauteurDebitCrues (idStation, dateCrues, hauteur, debit)
SELECT 
    'STAT1',  -- idStation
    gs.generate_series AS dateCrues,  -- date et heure générée
    random() * 10 AS hauteur,  -- Hauteur aléatoire entre 0 et 10
    random() * 300 AS debit  -- Débit aléatoire entre 0 et 300
FROM generate_series(
    '2024-11-29 00:00:00'::timestamp,  -- Date de départ
    now(),  -- Date actuelle
    '1 hour'::interval  -- Intervalle de 1 heure
) AS gs(generate_series);

-- Insertion des données dans la table pluieCrues
INSERT INTO pluieCrues (idStation, dateCrues, pluie)
SELECT 
    'STAT1',  -- idStation
    gs.generate_series AS dateCrues,  -- date et heure générée
    random() * 50 AS pluie  -- Pluie aléatoire entre 0 et 50 mm
FROM generate_series(
    '2024-11-29 00:00:00'::timestamp,  -- Date de départ
    now(),  -- Date actuelle
    '1 hour'::interval  -- Intervalle de 1 heure
) AS gs(generate_series);
