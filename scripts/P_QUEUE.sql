CREATE TABLE P_QUEUE (
    id int NOT NULL AUTO_INCREMENT,
    ev_type varchar(128) NOT NULL,
    ev_cmd varchar(256),
    ev_msg varchar(256),
    ev_extra varchar(2048) NOT NULL,
    importance int NOT NULL,
    PRIMARY KEY (id)
);
