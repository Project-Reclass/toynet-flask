/*
INSERT INTO users(id, password_hash, first_name) VALUES(################, "password_hash", "first_name");
INSERT INTO usernames(username, toynet_userid) VALUES("username/email", ################);

NOTE: the plaintext passwords here are for development login only - do NOT store production passwords in the code base!
*/

-- password: 'tayispusheen'
INSERT INTO users(id, password_hash, first_name) VALUES(20000000000000000000, "$argon2id$v=19$m=102400,t=2,p=8$Gb99iGZpk780wPblkFzxgg$8Bnv/63zkQWkblyy/wAB+A", "Tay");
INSERT INTO usernames(username, toynet_userid) VALUES("tay@projectreclass.org", 20000000000000000000);
