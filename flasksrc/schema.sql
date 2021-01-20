DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS toynet_values;
DROP TABLE IF EXISTS toynet_value_inspirations;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

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
