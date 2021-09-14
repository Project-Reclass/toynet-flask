BEGIN TRANSACTION;

INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4001,"bot@projectreclass.org",3,5);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4001,"bot@projectreclass.org",4,4);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4001,"bot@projectreclass.org",2,6);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4001,"bot@projectreclass.org",6,2);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4001,"bot@projectreclass.org",7,1);

INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4002,"tay@projectreclass.org",2,8);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4002,"tay@projectreclass.org",6,4);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4002,"tay@projectreclass.org",5,5);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4002,"tay@projectreclass.org",8,2);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4002,"tay@projectreclass.org",10,0);

INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4003,"kunal@projectreclass.org",2,5);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4003,"kunal@projectreclass.org",0,7);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4003,"kunal@projectreclass.org",4,3);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4003,"kunal@projectreclass.org",6,1);
INSERT INTO toynet_quiz_scores(quiz_id,user_id,count_correct,count_wrong) VALUES (4003,"kunal@projectreclass.org",7,0);

END TRANSACTION;