import sqlite3

CONN = sqlite3.connect("dogs.db")
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None  
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        CURSOR.execute(
            """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
            """
        )
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        CURSOR.execute(
            """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
            """,
            (self.name, self.breed),
        )
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        id, name, breed = row
        dog = cls(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM dogs")
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM dogs WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM dogs WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            new_dog = cls(name, breed)
            new_dog.save()
            return new_dog

    def update(self):
        if self.id:
            CURSOR.execute(
                """
                UPDATE dogs
                SET name = ?, breed = ?
                WHERE id = ?
                """,
                (self.name, self.breed, self.id),
            )
            CONN.commit()

Dog.create_table()
