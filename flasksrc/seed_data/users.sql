/*
INSERT INTO users(id, password_hash, first_name) VALUES(################, "password_hash", "first_name");
INSERT INTO usernames(username, toynet_userid) VALUES("username/email", ################);

NOTE: the plaintext passwords here are for development login only - do NOT store production passwords in the code base!
*/

INSERT INTO user_groups(id) VALUES("DEFAULT");
INSERT INTO user_groups(id) VALUES("ALPHA");
INSERT INTO users(username, user_group_id, password_hash, first_name) VALUES("kunal@projectreclass.org", "ALPHA", "$argon2id$v=19$m=102400,t=2,p=8$Gb99iGZpk780wPblkFzxgg$8Bnv/63zkQWkblyy/wAB+A", "Kunal");
INSERT INTO users(username, user_group_id, password_hash, first_name) VALUES("tay@projectreclass.org", "ALPHA", "$argon2id$v=19$m=102400,t=2,p=8$Gb99iGZpk780wPblkFzxgg$8Bnv/63zkQWkblyy/wAB+A", "Tay");
INSERT INTO users(username, password_hash, first_name) VALUES("bot@projectreclass.org", "$argon2id$v=19$m=102400,t=2,p=8$Gb99iGZpk780wPblkFzxgg$8Bnv/63zkQWkblyy/wAB+A", "Buddy");