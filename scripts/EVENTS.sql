CREATE TABLE EVENTS (
    id int NOT NULL AUTO_INCREMENT,
    ev_type varchar(128) NOT NULL,
    ev_extra varchar(512) NOT NULL,
    PRIMARY KEY (id)
);
