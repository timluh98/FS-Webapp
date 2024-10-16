CREATE TABLE todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complete BOOLEAN DEFAULT FALSE,
    description TEXT NOT NULL
);
CREATE TABLE list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
CREATE TABLE todo_list (
    todo_id INTEGER,
    list_id INTEGER,
    PRIMARY KEY (todo_id, list_id),
    FOREIGN KEY (todo_id) REFERENCES todo (id) ON DELETE CASCADE,
    FOREIGN KEY (list_id) REFERENCES list (id) ON DELETE CASCADE
);