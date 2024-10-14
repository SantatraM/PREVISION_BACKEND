create database stage;
\c stage;

create sequence seqSousBassin;
create table sousBassin(
    idSousBassin varchar default concat('SBS' || nextval('seqSousBassin')) primary key,
    sousBassin varchar
);

create sequence seqMesure;
create table mesure(
    idMesure varchar default concat('MES' || nextval('seqMesure')) primary key,
    mesure varchar
);

create sequence seqStation;
create table station(
    idStation varchar default concat('STAT' || nextval('seqStation')) primary key,
    site varchar(50),
    idSousBassin varchar references sousBassin(idSousBassin),
    longitude float,
    latitude float,
    idMesure varchar references mesure(idMesure),
    code varchar
);

create table stationImport(
    site varchar,
    sousBassin varchar,
    longitude varchar,
    latitude varchar,
    mesure varchar
);

create table hauteurDebitImport(
    station varchar,
    dateCrues varchar,
    hauteur varchar,
    debit varchar
);

create table PluieImport(
    station varchar,
    dateCrues varchar,
    pluie varchar
);

create sequence seqHauteur;
create table hauteurDebitCrues(
    id varchar default concat('HAU' || nextval('seqHauteur')) primary key,
    idStation varchar references station(idStation),
    dateCrues timestamp , 
    hauteur float,
    debit float
);

create sequence seqPluie;
create table pluieCrues(
    id varchar default concat('PLU' || nextval('seqPluie')) primary key,
    idStation varchar references station(idStation),
    dateCrues timestamp,
    pluie float
);

create sequence seqFormule;
create table formuleDebit(
    id varchar default concat('FOR' || nextval('seqFormule')) primary key,
    idStation varchar references station(idStation),
    condition float ,
    formule varchar
);

create sequence seqVariable;
create table variableFormule(
    id varchar default concat('VAR' || nextval('seqVariable')) primary key,
    idFormule varchar references formuleDebit(id),
    variable varchar(5),
    valeur float
);

create sequence seqSeuil;
create table seuil(
    idSeuil varchar default concat('SEU' || nextval('seqSeuil')) primary key,
    idStation varchar references station(idStation),
    rouge float,
    jaune float
);


