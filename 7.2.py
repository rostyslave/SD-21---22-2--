import sqlite3
from datetime import datetime


def initialize_db(db_name='articles.db'):
    """
    Ініціалізує базу даних і створює таблицю статей, якщо вона не існує.

    Args:
        db_name (str): Ім'я файлу бази даних

    Returns:
        None
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Articles (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author TEXT,
        created_date TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

    print(f"Базу даних '{db_name}' успішно ініціалізовано.")


def create_article(title, content, author=None, db_name='articles.db'):
    """
    Створює нову статтю в базі даних.

    Args:
        title (str): Заголовок статті
        content (str): Текстовий вміст статті
        author (str, optional): Автор статті
        db_name (str): Ім'я файлу бази даних

    Returns:
        int: ID створеної статті
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
    INSERT INTO Articles (title, content, author, created_date)
    VALUES (?, ?, ?, ?)
    ''', (title, content, author, created_date))

    article_id = cursor.lastrowid

    conn.commit()
    conn.close()

    print(f"Статтю '{title}' успішно створено з ID: {article_id}")
    return article_id


def delete_article(article_id, db_name='articles.db'):
    """
    Видаляє статтю за її ID.

    Args:
        article_id (int): ID статті, яку потрібно видалити
        db_name (str): Ім'я файлу бази даних

    Returns:
        bool: True якщо статтю видалено, False якщо статтю не знайдено
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM Articles WHERE id = ?', (article_id,))
    if not cursor.fetchone():
        conn.close()
        print(f"Статтю з ID {article_id} не знайдено.")
        return False

    cursor.execute('DELETE FROM Articles WHERE id = ?', (article_id,))

    conn.commit()
    conn.close()

    print(f"Статтю з ID {article_id} успішно видалено.")
    return True


def view_article(article_id, db_name='articles.db'):
    """
    Переглядає вміст статті за її ID.

    Args:
        article_id (int): ID статті, вміст якої потрібно переглянути
        db_name (str): Ім'я файлу бази даних

    Returns:
        dict або None: Словник з інформацією про статтю або None, якщо статтю не знайдено
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, title, content, author, created_date 
    FROM Articles 
    WHERE id = ?
    ''', (article_id,))

    article = cursor.fetchone()
    conn.close()

    if not article:
        print(f"Статтю з ID {article_id} не знайдено.")
        return None

    article_info = {
        'id': article[0],
        'title': article[1],
        'content': article[2],
        'author': article[3],
        'created_date': article[4]
    }

    print(f"Знайдено статтю: '{article_info['title']}' від {article_info['created_date']}")
    return article_info


def list_all_articles(db_name='articles.db'):
    """
    Отримує список всіх статей з бази даних.

    Args:
        db_name (str): Ім'я файлу бази даних

    Returns:
        list: Список словників з інформацією про кожну статтю
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT id, title, author, created_date FROM Articles ORDER BY created_date DESC')

    articles = cursor.fetchall()
    conn.close()

    result = []
    for article in articles:
        result.append({
            'id': article[0],
            'title': article[1],
            'author': article[2],
            'created_date': article[3]
        })

    print(f"Знайдено {len(result)} статей.")
    return result


def update_article(article_id, title=None, content=None, author=None, db_name='articles.db'):
    """
    Оновлює інформацію про статтю.

    Args:
        article_id (int): ID статті для оновлення
        title (str, optional): Новий заголовок статті
        content (str, optional): Новий текстовий вміст статті
        author (str, optional): Новий автор статті
        db_name (str): Ім'я файлу бази даних

    Returns:
        bool: True якщо статтю оновлено, False якщо статтю не знайдено
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM Articles WHERE id = ?', (article_id,))
    if not cursor.fetchone():
        conn.close()
        print(f"Статтю з ID {article_id} не знайдено.")
        return False

    update_fields = []
    values = []

    if title is not None:
        update_fields.append('title = ?')
        values.append(title)

    if content is not None:
        update_fields.append('content = ?')
        values.append(content)

    if author is not None:
        update_fields.append('author = ?')
        values.append(author)

    if not update_fields:
        conn.close()
        print("Не вказано поля для оновлення.")
        return False

    query = f"UPDATE Articles SET {', '.join(update_fields)} WHERE id = ?"
    values.append(article_id)

    cursor.execute(query, values)

    conn.commit()
    conn.close()

    print(f"Статтю з ID {article_id} успішно оновлено.")
    return True


def search_articles(keyword, db_name='articles.db'):
    """
    Пошук статей за ключовим словом у заголовку або вмісті.

    Args:
        keyword (str): Ключове слово для пошуку
        db_name (str): Ім'я файлу бази даних

    Returns:
        list: Список словників з інформацією про знайдені статті
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, title, author, created_date 
    FROM Articles 
    WHERE title LIKE ? OR content LIKE ?
    ORDER BY created_date DESC
    ''', (f'%{keyword}%', f'%{keyword}%'))

    articles = cursor.fetchall()
    conn.close()

    result = []
    for article in articles:
        result.append({
            'id': article[0],
            'title': article[1],
            'author': article[2],
            'created_date': article[3]
        })

    print(f"Знайдено {len(result)} статей за запитом '{keyword}'.")
    return result

initialize_db()

article_id = create_article("Моя перша стаття", "Це вміст моєї першої статті.", "Іван Петренко")
if article_id > 0:
    article = view_article(article_id)
    if article:
        print(f"Вміст статті: {article['content']}")

    update_article(article_id, content="Оновлений вміст статті.")

    delete_article(article_id)