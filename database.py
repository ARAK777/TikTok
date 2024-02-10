import sqlite3


def database_initialization():
    conn_languages = sqlite3.connect('database/lang.db')
    cursor_languages = conn_languages.cursor()
    cursor_languages.execute('''CREATE TABLE IF NOT EXISTS languages
                               (user_id INTEGER PRIMARY KEY, language TEXT)''')
    conn_languages.commit()
    conn_languages.close()

    conn_database = sqlite3.connect('database/db.db')
    cursor_database = conn_database.cursor()
    try:
        cursor_database.execute('SELECT * FROM users')
    except:
        cursor_database.execute('CREATE TABLE users(user_id INT)')
    try:
        cursor_database.execute('SELECT * FROM stats')
    except:
        cursor_database.execute('CREATE TABLE stats(download_count INT)')
        cursor_database.execute('INSERT INTO stats VALUES(0)')
    conn_database.commit()
    conn_database.close()


def get_user_language(user_id):
    conn_languages = sqlite3.connect('database/lang.db')
    cursor_languages = conn_languages.cursor()
    cursor_languages.execute("SELECT language FROM languages WHERE user_id = ?", (user_id,))
    result = cursor_languages.fetchone()
    conn_languages.close()
    if result:
        return result[0]
    return None


def set_user_language(user_id, language):
    conn_languages = sqlite3.connect('database/lang.db')
    cursor_languages = conn_languages.cursor()
    cursor_languages.execute("INSERT OR REPLACE INTO languages (user_id, language) VALUES (?, ?)", (user_id, language))
    conn_languages.commit()
    conn_languages.close()


def new_user(user_id):
    conn_database = sqlite3.connect('database/db.db')
    cursor_database = conn_database.cursor()
    user = cursor_database.execute(f'SELECT * FROM users WHERE user_id={user_id}').fetchall()
    if len(user) == 0:
        cursor_database.execute(f'INSERT INTO users VALUES({user_id})')
        conn_database.commit()
    conn_database.close()


def get_users_count():
    conn_database = sqlite3.connect('database/db.db')
    cursor_database = conn_database.cursor()
    result = cursor_database.execute('SELECT * FROM users').fetchall()
    conn_database.close()
    return result


def get_users():
    conn_database = sqlite3.connect('database/db.db')
    cursor_database = conn_database.cursor()
    result = [user[0] for user in cursor_database.execute('SELECT * FROM users').fetchall()]
    conn_database.close()
    return result


def add_new_download():
    conn_database = sqlite3.connect('database/db.db')
    cursor_database = conn_database.cursor()
    new = int(cursor_database.execute('SELECT * FROM stats').fetchone()[0]) + 1
    cursor_database.execute(f'UPDATE stats SET download_count={new}')
    conn_database.commit()
    conn_database.close()


def get_downloads():
    conn_database = sqlite3.connect('database/db.db')
    cursor_database = conn_database.cursor()
    result = int(cursor_database.execute('SELECT * FROM stats').fetchone()[0])
    conn_database.close()
    return result
