import sqlite3
import time


class SQLite:
    base_name = f'./base/Base.db'

    @property
    def connect_base(self):
        return sqlite3.connect(self.base_name)

    def insert(self, table, **kwargs):
        connect = self.connect_base
        obj = connect.cursor()
        if len(kwargs) > 1:
            placeholder = ', '.join(['?' for _ in range(len(kwargs))])
            columns = ', '.join(kwargs.keys())
        else:
            placeholder = "?"
            columns = ''.join(kwargs.keys())
        query, value = f"INSERT INTO {table} ({columns}) VALUES({placeholder})", tuple(kwargs.values())
        try:
            obj.execute(query, value)
            connect.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def select(self, table, column=None, fetchall=True, package=None, **kwargs):
        connect = self.connect_base
        obj = connect.cursor()

        if len(tuple(kwargs)) == 0:
            placeholder = ''
        elif len(tuple(kwargs)) == 1:
            placeholder = "WHERE {value}=?".format(value=''.join(kwargs.keys()))
        else:
            placeholder = "WHERE {value}".format(value=' AND '.join([f"{_}=?" for _ in kwargs.keys()]))
        if package:
            placeholder = f" WHERE {package['column']} IN {package['value']}"
        if column:
            column = column
        else:
            column = "*"
        query, value = f"SELECT {column} FROM {table} {placeholder}", tuple(kwargs.values())

        if fetchall:
            return obj.execute(query, value).fetchall()
        else:
            return obj.execute(query, value).fetchone()

    def update(self, table, selector: dict = None, collection=None, **kwargs):
        try:
            connect = self.connect_base
            obj = connect.cursor()
            obj.execute('PRAGMA journal_mode=WAL')
            if len(tuple(kwargs)) > 0:
                placeholder = ', '.join([f"{_}=?" for _ in kwargs.keys()])
            else:
                placeholder = f"{''.join(kwargs.keys())}=?"
            key = selector.keys()
            value = selector.values()
            if collection:
                print(value)
                key = f"{''.join(key)} IN {tuple(tuple(value)[0])}".replace('=?', '')
                query, value = f"UPDATE {table} SET {placeholder} WHERE {key}", tuple(kwargs.values())
            else:
                key = ''.join(selector.keys()) + "=?"
                value = ''.join(selector.values())
                query, value = f"UPDATE {table} SET {placeholder} WHERE {key}", tuple(kwargs.values()) + (value,)
            obj.execute(query, value)
            connect.commit()
        except Exception as ex:
            print(ex)
            time.sleep(2)
            self.update(table, selector, **kwargs)
