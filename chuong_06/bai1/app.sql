CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);
INSERT INTO users (name, email) VALUES ('Nguyen Van A', 'a@gmail.com');
INSERT INTO users (name,email) VALUES ('Nguyen Dang Phat' , 'phat@gmail.com');