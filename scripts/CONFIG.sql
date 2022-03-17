CREATE TABLE CONFIG (
    evar varchar(128) NOT NULL,
    val varchar(500) NOT NULL,
    PRIMARY KEY (evar, val)
);
