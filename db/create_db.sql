CREATE TABLE IF NOT EXISTS budget(
    codename VARCHAR(255) PRIMARY KEY,
    daily_limit INTEGER);

CREATE TABLE IF NOT EXISTS category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense BOOLEAN,
    aliases text);

CREATE TABLE IF NOT EXISTS expense(
    id integer primary key,
    amount decimal(6, 2),
    created varchar(255),
    category_codename varchar(255),
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename));

INSERT INTO category (codename, name, is_base_expense, aliases) VALUES
    ("products", "products", true, "food products"),
    ("rent", "rent", true, "rent"),
    ("mobile", "mobile", true, "mobile"),
    ("transport", "transport", true, "metro bolt"),
    ("fitness", "fitness", true, "gym fitness"),
    ("cafe", "cafe", false, "cafe"),
    ("clothes", "clothes", false, "clothes shoes"),
    ("travel", "travel", false, "travel tickets"),
    ("alco", "alcohol", false, "wine beer alco"),
    ("other", "other", false, "");
