DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS toynet_values;
DROP TABLE IF EXISTS toynet_value_inspirations;

DROP TABLE IF EXISTS toynet_quizzes;
DROP TABLE IF EXISTS toynet_quiz_questions;
DROP TABLE IF EXISTS toynet_quiz_options;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
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
  quiz_id INTEGER PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE toynet_quiz_questions (
  quiz_id INTEGER NOT NULL,
  question_id  INTEGER NOT NULL,
  question TEXT NOT NULL,
  answer INTEGER NOT NULL,
  PRIMARY KEY (quiz_id, question_id)
  FOREIGN KEY (quiz_id) REFERENCES toynet_quiz (quiz_id)
);

CREATE TABLE toynet_quiz_options (
  quiz_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  option_id INTEGER NOT NULL,
  option TEXT NOT NULL,
  PRIMARY KEY (quiz_id, question_id, option_id)
  FOREIGN KEY (quiz_id) REFERENCES toynet_quiz (quiz_id)
  FOREIGN KEY (question_id) REFERENCES toynet_quiz_questions (question_id)
);

