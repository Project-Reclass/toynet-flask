-- This file is part of Toynet-Flask.
-- 
-- Toynet-Flask is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
-- 
-- Toynet-Flask is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
-- 
-- You should have received a copy of the GNU General Public License
-- along with Toynet-Flask.  If not, see <https://www.gnu.org/licenses/>.

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
