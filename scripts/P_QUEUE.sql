CREATE TABLE P_QUEUE (
    id int NOT NULL AUTO_INCREMENT,
    ev_type varchar(128) NOT NULL,
    ev_extra varchar(512) NOT NULL,
    importance int NOT NULL,
    PRIMARY KEY (id)
);
