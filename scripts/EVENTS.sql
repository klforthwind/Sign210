CREATE TABLE EVENTS (
    id int NOT NULL AUTO_INCREMENT,
    ev_type varchar(128) NOT NULL,
    ev_cmd varchar(256),
    ev_msg varchar(256),
    ev_extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE TWITCH_COMMAND (
    id int NOT NULL AUTO_INCREMENT,
    user varchar(256),
    cmd varchar(256),
    msg varchar(256),
    flags varchar(512), 
    extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE TWITCH_CHAT (
    id int NOT NULL AUTO_INCREMENT,
    user varchar(256),
    msg varchar(256),
    flags varchar(512),
    extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE TWITCH_RAID (
    id int NOT NULL AUTO_INCREMENT,
    user varchar(256),
    viewers varchar(256),
    extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE TWITCH_CHEER (
    id int NOT NULL AUTO_INCREMENT,
    user varchar(256),
    msg varchar(256),
    bits varchar(256),
    flags varchar(512), 
    extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE TWITCH_SUB (
    id int NOT NULL AUTO_INCREMENT,
    user varchar(256),
    msg varchar(256),
    subTierInfo varchar(256), 
    extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE TWITCH_RESUB (
    id int NOT NULL AUTO_INCREMENT,
    user varchar(256),
    msg varchar(256),
    streamMonths varchar(64),
    cumulativeMonths varchar(64),
    subTierInfo varchar(256), 
    extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE TWITCH_GIFTSUB (
    id int NOT NULL AUTO_INCREMENT,
    gifterUser varchar(256),
    streakMonths varchar(64),
    recipientUser varchar(256),
    senderCount varchar(64),
    subTierInfo varchar(256), 
    extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE TWITCH_MYSTERYSUB (
    id int NOT NULL AUTO_INCREMENT,
    gifterUser varchar(256),
    numOfSubs varchar(64),
    senderCount varchar(64),
    subTierInfo varchar(256), 
    extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE TWITCH_CONTINUESUB (
    id int NOT NULL AUTO_INCREMENT,
    user varchar(256),
    sender varchar(256),
    extra varchar(2048) NOT NULL,
    PRIMARY KEY (id)
);
