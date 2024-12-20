create or replace view v_station as 
    select s.* , sb.sousbassin , m.mesure
    from station s
    join sousbassin sb on sb.idsousbassin = s.idsousbassin
    join mesure m on m.idmesure = s.idmesure

create or replace view v_formule as
    select fd.* , s.site as station
    from formuledebit fd 
    join station s on s.idStation = fd.idStation;

create or replace view v_formule_variable AS
    SELECT fd.id AS idformule,fd.idStation,fd.condition,fd.formule,s.site as station,
        STRING_AGG(vf.variable || ' = ' || vf.valeur, ', ') AS variables_valeurs,
        fd.formule as formuleFinal
    FROM formuleDebit fd
    left JOIN variableFormule vf ON fd.id = vf.idFormule
    join station s on s.idStation = fd.idStation
    GROUP BY fd.id, fd.idStation, fd.condition, fd.formule,s.site;

create or replace view v_seuil as
    select s.* , st.site as station
    from seuil s
    join station st on st.idStation = s.idStation;

create or replace view v_station_sans_seuil as station
    SELECT st.*
    FROM station st
    WHERE NOT EXISTS (
        SELECT 1 FROM seuil s WHERE st.idStation = s.idStation
    );

create or replace view v_crues as
    SELECT COALESCE(h.idStation, p.idStation) AS idStation,COALESCE(h.dateCrues, p.dateCrues) AS dateCrues,h.hauteur,h.debit,p.pluie,s.rouge,s.jaune
    FROM 
        hauteurDebitCrues h
    FULL OUTER JOIN 
        pluieCrues p ON h.idStation = p.idStation AND h.dateCrues = p.dateCrues
    LEFT OUTER JOIN seuil s ON COALESCE(h.idStation, p.idStation) = s.idStation
    ORDER BY idStation, dateCrues;

create or replace view v_commune_Analamanga as
    select * from commune 
    where nom_region = 'ANALAMANGA';

CREATE OR REPLACE VIEW v_vigilence_commune AS
    SELECT cs.id AS idCommuneStation,cs.idStation,c.id,c.nom_commun AS nomCommune,ST_AsGeoJSON(c.geom) as geom ,c.pop_ensemb,c. pop_hommes, c.pop_femmes,c.nom_distri,
        CASE 
            WHEN latest.hauteur >= COALESCE(latest.rouge, 0) THEN 'red' --rouge
            WHEN latest.hauteur >= COALESCE(latest.jaune, 0) THEN 'yellow' --jaune
            ELSE 'grey' --aucune
        END AS couleur
    FROM v_commune_Analamanga c
    LEFT JOIN communeStation cs ON cs.idCommune = c.id
    LEFT JOIN 
        ( 
            SELECT v.idStation, v.hauteur, v.debit, v.pluie, v.rouge, v.jaune, v.dateCrues
            FROM v_crues v
            WHERE (v.idStation, v.dateCrues) IN (
                SELECT idStation, MAX(dateCrues)
                FROM v_crues
                GROUP BY idStation
            )
        ) latest ON cs.idStation = latest.idStation
    ORDER BY cs.idCommune, latest.hauteur;

CREATE OR REPLACE VIEW v_nombre_commune_sous_vigilence AS
    SELECT COUNT(DISTINCT idCommuneStation) AS total
    FROM v_vigilence_commune
    WHERE couleur != 'grey';

CREATE OR REPLACE VIEW v_nombre_population_vigilence AS
    SELECT
        COUNT(CASE WHEN couleur = 'red' THEN 1 ELSE NULL END) AS population_rouge,
        COUNT(CASE WHEN couleur = 'yellow' THEN 1 ELSE NULL END) AS population_jaune
    FROM
        v_vigilence_commune;

CREATE OR REPLACE VIEW v_pourcentage_communes_alertes AS
    WITH couleur_possible AS (
        SELECT 'red' AS couleur
        UNION ALL
        SELECT 'yellow'
        UNION ALL
        SELECT 'grey'
    )
    SELECT
        cp.couleur,
        COALESCE(COUNT(vvc.id), 0) AS nombres_communes,
        COALESCE(ROUND((COUNT(vvc.id) * 100.0 / (SELECT COUNT(*) FROM v_vigilence_commune)), 2), 0) AS pourcentage
    FROM
        couleur_possible cp
    LEFT JOIN
        v_vigilence_commune vvc ON vvc.couleur = cp.couleur
    GROUP BY
        cp.couleur;

CREATE OR REPLACE VIEW v_previsionParRivieres AS
SELECT ppr.*,r.nom as riviere, s1.site AS nomStationDeDonnee,s2.site AS nomStationAPrevoir
FROM previsionParRivieres ppr
JOIN station s1 ON s1.idStation = ppr.stationDeDonnee
JOIN station s2 ON s2.idStation = ppr.stationAPrevoir
JOIN riviere r ON r.id = ppr.idriviere;

CREATE VIEW v_prevision_par_rivieres AS
SELECT p.id,p.idriviere,r.nom AS nom_riviere,  p.stationDeDonnee,s1.site AS station_de_donnee,  p.stationAPrevoir,s2.site AS station_a_prevoir  
FROM previsionParRivieres p
JOIN riviere r ON p.idriviere = r.id
JOIN station s1 ON p.stationDeDonnee = s1.idStation
JOIN station s2 ON p.stationAPrevoir = s2.idStation;

create or replace view v_riviere_non_prise as
select r.*
from riviere r 
where not EXISTS (
    select 1 from previsionparrivieres ppr where ppr.idriviere = r.id
);


CREATE OR REPLACE VIEW v_commune_station AS
SELECT 
    c.idstation,
    s.site AS station,
    json_agg(
        jsonb_build_object(
            'commune', cm.nom_commun,
            'idcommune', cm.id
        )
    ) AS communes_info
FROM station s
JOIN communeStation c ON s.idstation = c.idstation
JOIN commune cm ON cm.id = c.idcommune
GROUP BY c.idstation, s.site;
station
