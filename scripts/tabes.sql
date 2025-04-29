-- don't execute this file

CREATE TABLE users (
        id INTEGER NOT NULL AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL,
        hashed_password VARCHAR(100) NOT NULL,
        created_at DATETIME DEFAULT (now()),
        updated_at DATETIME,
        PRIMARY KEY (id),
        UNIQUE (username),
        UNIQUE (email)
)