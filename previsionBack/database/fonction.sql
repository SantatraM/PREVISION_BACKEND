CREATE OR REPLACE FUNCTION dispatchHauteur()
RETURNS VOID AS $$
BEGIN

    INSERT INTO hauteurDebitCrues(idstation,dateCrues,hauteur,debit)
    SELECT DISTINCT hdi.station,hdi.datecrues::timestamp,hdi.hauteur::float,debit::float
    from hauteurDebitImport hdi
    where not EXISTS (
        select 1 from hauteurDebitCrues hdc
        where hdc.datecrues = hdi.datecrues::timestamp
        and hdc.idstation = hdi.station
    );

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION dispatchPluie()
RETURNS VOID AS $$
BEGIN

    INSERT INTO pluiecrues(idstation,dateCrues,pluie)
    SELECT DISTINCT pi.station,pi.dateCrues::timestamp,pi.pluie::float
    from PluieImport pi 
    where not EXISTS (
        select 1 from pluiecrues pc
        where pc.datecrues = pi.datecrues::timestamp
        and pc.idstation = pi.station
    );

END;
$$ LANGUAGE plpgsql;