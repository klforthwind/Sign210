CREATE TABLE CONFIG (
    evar varchar(128) NOT NULL,
    val varchar(2048) NOT NULL,
    PRIMARY KEY (evar, val)
);
