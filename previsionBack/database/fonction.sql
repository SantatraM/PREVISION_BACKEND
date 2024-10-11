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