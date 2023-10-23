import sqlite3


conn = sqlite3.connect(r"C:\Users\Admin\PycharmProjects\AccounterBot\expences.db")
cursor = conn.cursor()

def _init_db():
    with open(".\db\create_db.sql", "r") as f:
        query_str = f.read()
    cursor.executescript(query_str)
    conn.commit()

def is_db_exist():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expense'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

is_db_exist()

# здесь будут обращения к бд
def insert(table: str, columns: dict[str, str]):
    column_keys = ', '.join(columns.keys())
    values = tuple(columns.values())
    placeholders = ", ".join("?" * len(columns.keys()))
    cursor.execute(f"INSERT INTO {table} ({column_keys}) VALUES ({placeholders})", values)
    conn.commit()
    
def today_stat() -> str:
    cursor.execute("SELECT SUM(amount) FROM expense WHERE DATE(created)=DATE('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "Сегодня еще не было трат"
    all_today_expenses = result[0]
    return (f"Всего расходов за день: {all_today_expenses} €\nТраты за месяц /month")
    
def month_stat(first_day_month: str) -> str:
    cursor.execute(f"SELECT SUM(amount) FROM expense WHERE DATE(created) > DATE('{first_day_month}')")
    result = cursor.fetchone()
    if not result[0]:
        return "В этом месяце еще не было трат"
    return f"Всего расходов в этом месяце: {result[0]} €"

def fetchall(table: str, columns: list[str]) -> list[dict]:
    joined_columns = ', '.join(columns)
    cursor.execute(f"SELECT {joined_columns} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result

def delete(category_name, amount):
    cursor.execute(f"SELECT * FROM expense WHERE DATE(created)=DATE('now', 'localtime') AND category_codename='{category_name}' AND amount='{amount}'")
    result = cursor.fetchone()
    if result:
        cursor.execute(f"DELETE FROM expense WHERE DATE(created) = DATE('now', 'localtime') AND category_codename='{category_name}' AND amount='{amount}'")
        conn.commit()
    return result

def get_today_expenses_list():
    cursor.execute("SELECT * FROM expense WHERE DATE(created) = DATE('now', 'localtime')")
    result = cursor.fetchall()
    return result
