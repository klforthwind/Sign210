CREATE TABLE EVENTS (
    id int NOT NULL AUTO_INCREMENT,
    ev_type varchar(128) NOT NULL,
    ev_extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);
