CREATE TABLE TOKENS(
ID TEXT PRIMARY KEY NOT NULL,
TOKEN TEXT NOT NULL
);

CREATE TABLE POKES(
POKEID INTEGER PRIMARY KEY NOT NULL,
UID TEXT NOT NULL,
RID TEXT NOT NULL,
RNAME TEXT NOT NULL,
TEXTD TEXT,
ODATA TEXT,
PTIME TEXT
);
