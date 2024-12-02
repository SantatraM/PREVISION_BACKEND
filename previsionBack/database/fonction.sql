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

CREATE OR REPLACE FUNCTION variationDebit(station VARCHAR)
RETURNS float AS $$
DECLARE
    debit_now float;
    debit_6hours_ago float;
    last_date TIMESTAMP;
BEGIN
    -- Récupérer la dernière date pour la station
    SELECT MAX(datecrues) INTO last_date
    FROM v_crues
    WHERE idstation = station;

    -- Récupérer le débit à la dernière date
    SELECT debit INTO debit_now
    FROM v_crues
    WHERE idstation = station
    AND datecrues = last_date;

    -- Récupérer le débit 6 heures avant la dernière date
    SELECT debit INTO debit_6hours_ago
    FROM v_crues
    WHERE idstation = station
    AND datecrues = last_date - INTERVAL '6 hours';

    -- Retourner la différence des débits
    RETURN debit_now - debit_6hours_ago;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION dQPrev6hours(station VARCHAR)
RETURNS float AS $$
DECLARE
    dqprev float;
    debit_now float;
    debit_6hours_ago float;
    debit_12hours_ago float;
    debit_18hours_ago float;
    debit_24hours_ago float;
    last_date timestamp;
BEGIN 
    -- Récupérer la dernière date pour la station
    SELECT MAX(datecrues) INTO last_date
    FROM v_crues
    WHERE idstation = station;

    -- Récupérer tous les débits pour la station à différents moments
    SELECT 
        debit INTO debit_now
    FROM v_crues
    WHERE idstation = station
    AND datecrues = last_date;

    SELECT 
        debit INTO debit_6hours_ago
    FROM v_crues
    WHERE idstation = station
    AND datecrues = last_date - INTERVAL '6 hours';

    SELECT 
        debit INTO debit_12hours_ago
    FROM v_crues
    WHERE idstation = station
    AND datecrues = last_date - INTERVAL '12 hours';

    SELECT 
        debit INTO debit_18hours_ago
    FROM v_crues
    WHERE idstation = station
    AND datecrues = last_date - INTERVAL '18 hours';

    SELECT 
        debit INTO debit_24hours_ago
    FROM v_crues
    WHERE idstation = station
    AND datecrues = last_date - INTERVAL '24 hours';

    -- Calculer la variation du débit
    dqprev = (0.22 * debit_now) + (0.38 * debit_6hours_ago) + 
             (0.18 * debit_12hours_ago) + (0.12 * debit_18hours_ago) + 
             (0.10 * debit_24hours_ago);

    RETURN dqprev;
END;
$$ LANGUAGE plpgsql;

