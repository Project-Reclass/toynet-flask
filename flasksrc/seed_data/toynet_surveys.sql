INSERT INTO toynet_survey_types(type_id, type) VALUES(0, "TEXT");
INSERT INTO toynet_survey_types(type_id, type) VALUES(1, "CHOICE");
INSERT INTO toynet_survey_types(type_id, type) VALUES(2, "LONGTEXT");
INSERT INTO toynet_survey_types(type_id, type) VALUES(3, "SCALE");



INSERT INTO toynet_surveys(survey_id) VALUES(6001);

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6001, 0, 0, "What is your first name?", NULL);

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6001, 1, 1, "Are you interested in a career in the technology industry?", NULL);
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 1, 0, "As of now, I don't plan on it.");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 1, 1, "Not sure...");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 1, 2, "I'm open to it. :)");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 1, 3, "Absolutely!");

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6001, 2, 2, "What do you hope to get out of this course?", NULL);

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6001, 3, 3, "How familiar would you say you are with computer networking concepts?", NULL);
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 3, 0, "Not at all");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 3, 1, "Some familiarity");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 3, 2, "Quite a bit");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 3, 3, "Very familiar");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 3, 4, "Professional Experience");

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6001, 4, 2, "How did you get involved with our program?", NULL);

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6001, 5, 1, "Have you ever worked with computer networks during you time in service?", NULL);
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 5, 0, "Yes");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6001, 5, 1, "No");

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6001, 6, 0, "How many months do you plan to dedicate to this program?", "months");



INSERT INTO toynet_surveys(survey_id) VALUES(6002);

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6002, 0, 1, "Do you feel more knowledgable about computer networking than before you took this module?", NULL);
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 0, 0, "Yes");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 0, 1, "About the same");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 0, 2, "No");

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6002, 1, 3, "How helpful were the diagrams in understanding protocols?", NULL);
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 1, 0, "Not at all");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 1, 1, "A little");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 1, 2, "Not very");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 1, 3, "Super helpful");

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6002, 2, 3, "How helpful was the example of chain of command in understanding OSI layers?", NULL);
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 2, 0, "Not at all");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 2, 1, "A little");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 2, 2, "Not very");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 2, 3, "Super helpful");

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6002, 3, 0, "How difficult as the material to master?", NULL);

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6002, 4, 2, "Please list any questions you still have about the content.", NULL);

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6002, 5, 1, "Do you feel more knowledgable about computer networking than before you took this module?", NULL);
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 5, 0, "Yes");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 5, 1, "About the same");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 5, 2, "No");

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6002, 6, 3, "How helpful were the diagrams in understanding protocols?", NULL);
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 6, 0, "Not at all");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 6, 1, "A little");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 6, 2, "Not very");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 6, 3, "Super helpful");

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6002, 7, 3, "How helpful was the example of chain of command in understanding OSI layers?", NULL);
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 7, 0, "Not at all");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 7, 1, "A little");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 7, 2, "Helpful");
INSERT INTO toynet_survey_options(survey_id, question_id, option_id, option) VALUES(6002, 7, 3, "Super helpful");

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6002, 8, 0, "How difficult as the material to master?", NULL);

INSERT INTO toynet_survey_questions(survey_id, question_id, type_id, question, unit) VALUES(6002, 9, 2, "Please list any questions you still have about the content.", NULL);
