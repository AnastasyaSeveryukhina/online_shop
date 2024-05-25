import sqlite3


def create_table():
    """Create the Product table in the SQLite database."""
    conn = sqlite3.connect('instance/shop.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT NOT NULL,
            image BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def insert_test_data():
    """Insert test data into the Product table."""
    conn = sqlite3.connect('instance/shop.db')
    cursor = conn.cursor()

    # Test data
    products = [
        ('Рубашка-поло с короткими рукавами', 'Мужчины', 4599,
         'Футболка-поло с короткими рукавами из трикотажа пике JACK & JONES (Джек Джонс).',
         "static/img/images/kid_in_polo.jpg"),
        ('Рубашка в клетку с длинными рукавами', 'Мужчины', 4549,
         'Рубашка прямого покроя в клетку с длинными рукавами зеленый хаки ONLY & SONS.',
         "static/img/images/man_in_shirt.jpg"),
        ('Брюки-чинос Jpstmarco', 'Мужчины', 5799, 'Брюки-чинос Jpstmarco каштановый JACK & JONES',
         "static/img/images/man_in_brown.jpg"),
        ('Шорты мандарин', 'Женщины', 8349, 'Шорты мандарин MORGAN. Заниженная посадка, оригинальные карманы спереди.',
         "static/img/images/woman_in_red.jpg"),
        ('Платье джинсовое короткое', 'Женщины', 12199,
         'Платье джинсовое короткое расклешенное цвет необработанный натуральный MORGAN.',
         "static/img/images/woman_in_dress.jpg"),
        ('Комбинезон с плиссированными брючинами', 'Женщины', 14499,
         'Комбинезон свободного покроя с плиссированными брючинами темно-синий.', "static/img/images/woman_in_black.jpg"),
        ('Тренч с поясом Signature', 'Дети', 3599, 'Тренч с поясом Signature - LA REDOUTE COLLECTIONS.',
         "static/img/images/kid_in_trench.jpg"),
        ('Брюки широкие', 'Дети', 2199, 'Брюки широкие экрю LA REDOUTE COLLECTIONS.',
         "static/img/images/kid_in_white.jpg"),
        ('Футболка принт "мячи"', 'Дети', 965, 'Футболка с круглым вырезом, принт "мячи" белый LA REDOUTE COLLECTIONS.',
         "static/img/images/kid_with_balls.jpg"),
        ('Сумка из кожи', 'Аксессуары', 4349, 'Сумка из кожи с ремешком через плечо, Onlarielle - ONLY SHOES.',
         "static/img/images/grey_bag.jpg"),
        ('Ремень тонкий', 'Аксессуары', 999, 'Ремень тонкий темно-бежевый LA REDOUTE COLLECTIONS.',
         "static/img/images/red_belt.jpg"),
        ('Шляпа с широкими мягкими полями', 'Аксессуары', 3449,
         'Шляпа с широкими мягкими полями, из натуральных волокон, мягкая натуральный LA REDOUTE COLLECTIONS.',
         "static/img/images/head.jpg")
    ]

    cursor.executemany('''
        INSERT INTO Product (name, category, price, description, image) VALUES (?, ?, ?, ?, ?)
    ''', products)

    conn.commit()
    conn.close()


def main():
    """Main function to create the table and insert test data."""
    # create_table()
    insert_test_data()
    print("Database and table created, test data inserted.")


if __name__ == "__main__":
    main()

