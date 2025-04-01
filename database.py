import sqlite3


conn = sqlite3.connect("trains.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS train_routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_number TEXT NOT NULL,
        departure TEXT NOT NULL,
        destination TEXT NOT NULL,
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS train_cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_number TEXT NOT NULL,
        car_type TEXT NOT NULL,
        seat_count INTEGER,
        FOREIGN KEY (train_number) REFERENCES train_routes (train_number)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS train_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_number TEXT NOT NULL,
        car_id INTEGER NOT NULL,
        passenger_name TEXT NOT NULL,
        seat_number INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (train_number) REFERENCES train_routes (train_number),
        FOREIGN KEY (car_id) REFERENCES train_cars (id)
    )
''')

cursor.executemany('''
    INSERT INTO train_routes (train_number, departure, destination, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)
''', [
    ("IC125", "Київ", "Львів", "08:00", "14:30"),
    ("RE256", "Львів", "Одеса", "10:15", "22:45"),
    ("NV341", "Харків", "Дніпро", "07:30", "10:00"),
    ("IC789", "Одеса", "Київ", "16:00", "23:15"),
    ("RE654", "Дніпро", "Львів", "12:45", "23:30")
])

cursor.executemany('''
    INSERT INTO train_cars (train_number, car_type, seat_count) VALUES (?, ?, ?)
''', [
    ("IC125", "Плацкарт", 54),
    ("IC125", "Купе", 36),
    ("RE256", "СВ", 18),
    ("NV341", "Плацкарт", 54),
    ("IC789", "Купе", 36)
])

cursor.executemany('''
    INSERT INTO train_tickets (train_number, car_id, passenger_name, seat_number, price) VALUES (?, ?, ?, ?, ?)
''', [
    ("IC125", 1, "Іван Петренко", 12, 450.00),
    ("IC125", 2, "Марія Іваненко", 8, 600.00),
    ("RE256", 3, "Олег Коваленко", 5, 1200.00),
    ("NV341", 4, "Анна Савченко", 27, 350.00),
    ("IC789", 5, "Петро Бондар", 14, 700.00)
])

conn.commit()

print("\n" + "=" * 50)
print("=== СПИСОК НОМЕРІВ ПОТЯГІВ ===")
print("=" * 50)
cursor.execute("SELECT DISTINCT train_number FROM train_routes ORDER BY train_number")
train_numbers = cursor.fetchall()
for i, train in enumerate(train_numbers, 1):
    print(f"{i}. {train[0]}")

print("\n\n" + "=" * 80)
print("=== ТАБЛИЦЯ МАРШРУТІВ ПОЇЗДІВ ===")
print("=" * 80)
print("ID | Номер поїзда | Відправлення | Призначення | Час відправлення | Час прибуття")
print("-" * 80)
cursor.execute("SELECT * FROM train_routes")
routes = cursor.fetchall()
for route in routes:
    print(f"{route[0]} | {route[1]} | {route[2]} | {route[3]} | {route[4]} | {route[5]}")

print("\n\n" + "=" * 80)
print("=== ТАБЛИЦЯ ВАГОНІВ ===")
print("=" * 80)
print("ID | Номер поїзда | Тип вагону | Кількість місць")
print("-" * 50)
cursor.execute("SELECT * FROM train_cars")
cars = cursor.fetchall()
for car in cars:
    print(f"{car[0]} | {car[1]} | {car[2]} | {car[3]}")

print("\n\n" + "=" * 80)
print("=== ТАБЛИЦЯ КВИТКІВ ===")
print("ID | Номер поїзда | ID вагону | Пасажир | Номер місця | Ціна")
cursor.execute("SELECT * FROM train_tickets")
tickets = cursor.fetchall()
for ticket in tickets:
    print(f"{ticket[0]} | {ticket[1]} | {ticket[2]} | {ticket[3]} | {ticket[4]} | {ticket[5]}")

print("\n\n" + "=" * 80)
print("=== НЕОБРОБЛЕНІ ДАНІ ВАГОНІВ ===")


cursor.execute("SELECT * FROM train_cars")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()