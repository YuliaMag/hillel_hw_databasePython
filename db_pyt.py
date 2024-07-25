import sqlite3
from typing import List, Any, Type
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    email: str


class DatabaseTable:
    def __init__(self, db_name: str, table_name: str, user_class: Type):
        self.db_name = db_name
        self.table_name = table_name
        self.user_class = user_class
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
                )
            ''')
            conn.commit()

    def add_records(self, *records: Any):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            for record in records:
                if isinstance(record, self.user_class):
                    cursor.execute(f'''
                        INSERT OR REPLACE INTO {self.table_name} (name, email)
                        VALUES (?, ?)
                    ''', (record.name, record.email))
            conn.commit()

    def update_records(self, condition: str, **values):
        set_clause = ', '.join([f"{i} = ?" for i in values.keys()])
        sql = f'''
            UPDATE {self.table_name}
            SET {set_clause}
            WHERE {condition}
        '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(values.values()))
            conn.commit()

    def get_records(self, condition: str = '1=1') -> List[Type]:
        sql = f'''
            SELECT * FROM {self.table_name}
            WHERE {condition}
        '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [self.user_class(*row) for row in rows]

    def delete_records(self, condition: str):
        sql = f'''
            DELETE FROM {self.table_name}
            WHERE {condition}
        '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()


# Usage Example:
if __name__ == '__main__':
    @dataclass
    class User:
        id: int
        name: str
        email: str

# ========================================================================================= #

    db_table = DatabaseTable('data.db', 'employees', User)

    db_table.add_records(User(id=1, name='Margot', email='margotcat@xmpl.com'), User(id=2, name='Tamir', email='tamirdog@xmpl.com'))

    db_table.update_records("name = 'Margot'", email='margotcat_nn@xmpl.com')

    users = db_table.get_records()
    for user in users:
        print(user)

    db_table.delete_records("name = 'Margot'")
    db_table.delete_records("name = 'Tamir'")

    print('\n')
    users = db_table.get_records()
    for user in users:
        print(user)
