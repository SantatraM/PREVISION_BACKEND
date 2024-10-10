create or replace view v_station as 
select s.* , sb.sousbassin , m.mesure
from station s
join sousbassin sb on sb.idsousbassin = s.idsousbassin
join mesure m on m.idmesure = s.idmesure