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
JOIN variableFormule vf ON fd.id = vf.idFormule
join station s on s.idStation = fd.idStation
GROUP BY fd.id, fd.idStation, fd.condition, fd.formule,s.site;