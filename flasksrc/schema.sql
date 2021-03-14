DROP TABLE IF EXISTS usernames;
DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS toynet_values;
DROP TABLE IF EXISTS toynet_value_inspirations;

DROP TABLE IF EXISTS toynet_quizzes;
DROP TABLE IF EXISTS toynet_quiz_options;

DROP TABLE IF EXISTS toynet_surveys;
DROP TABLE IF EXISTS toynet_survey_questions;
DROP TABLE IF EXISTS toynet_survey_options;
DROP TABLE IF EXISTS toynet_survey_types;

-- user data

CREATE TABLE usernames (
  username TEXT PRIMARY KEY,
  toynet_userid INTEGER NOT NULL,
  UNIQUE (toynet_userid),
  FOREIGN KEY (toynet_userid) REFERENCES users (id)
);

CREATE TABLE users (
  id TEXT PRIMARY KEY,
  password_hash TEXT NOT NULL,
  first_name TEXT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- values submodule

CREATE TABLE toynet_values (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE toynet_value_inspirations (
  value_id INTEGER NOT NULL,
  organization TEXT NOT NULL,
  quote TEXT NOT NULL,
  FOREIGN KEY (value_id) REFERENCES toynet_value (id)
);


-- quizzes submodule

CREATE TABLE toynet_quizzes (
  quiz_id INTEGER NOT NULL,
  question_id  INTEGER NOT NULL,
  question TEXT NOT NULL,
  answer INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (quiz_id, question_id)
);

CREATE TABLE toynet_quiz_options (
  quiz_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  option_id INTEGER NOT NULL,
  option TEXT NOT NULL,
  PRIMARY KEY (quiz_id, question_id, option_id)
  FOREIGN KEY (quiz_id, question_id) REFERENCES toynet_quizzes (quiz_id, question_id)
);


-- surveys submodule

CREATE TABLE toynet_surveys (
  survey_id INTEGER PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE toynet_survey_questions (
  survey_id INTEGER NOT NULL,
  question_id  INTEGER NOT NULL,
  type_id INTEGER NOT NULL,
  question TEXT NOT NULL,
  unit TEXT,
  PRIMARY KEY (survey_id, question_id, type_id)
  FOREIGN KEY (survey_id) REFERENCES toynet_surveys (survey_id)
);

CREATE TABLE toynet_survey_options (
  survey_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  option_id INTEGER NOT NULL,
  option TEXT NOT NULL,
  PRIMARY KEY (survey_id, question_id, option_id)
  FOREIGN KEY (survey_id, question_id) REFERENCES toynet_survey_questions (survey_id, question_id)
);

CREATE TABLE toynet_survey_types (
  type_id INTEGER NOT NULL,
  type TEXT NOT NULL,
  PRIMARY KEY (type_id)
  FOREIGN KEY (type_id) REFERENCES toynet_survey_questions (type_id)
);
