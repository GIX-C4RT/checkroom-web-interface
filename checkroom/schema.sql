DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS item;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    admin BOOLEAN NOT NULL
);

CREATE TABLE item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    image BLOB NOT NULL,
    borrower INTEGER,
    FOREIGN KEY (borrower) REFERENCES user (id)
);