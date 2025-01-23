CREATE TABLE IF NOT EXISTS savings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal TEXT NOT NULL,
    amount REAL NOT NULL,
    saved REAL NOT NULL DEFAULT 0,
    start_date TEXT,
    end_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
