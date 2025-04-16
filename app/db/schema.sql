CREATE TABLE IF NOT EXISTS stories (
    id BIGINT PRIMARY KEY,
    title TEXT,
    score INTEGER,
    url TEXT,
    author TEXT,
    time BIGINT,
    descendants INTEGER,
    type TEXT
);
