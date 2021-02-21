import sqlite3
import datetime

class Date:
    def __init__(self):
        self.current_date = datetime.datetime.now()
        self.days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        self.set_current_date()


        if self.is_leap_year(self.current_date.year):
            self.days_in_months[1] = 29

    def set_current_date(self):
        self.active_day = int(self.current_date.day)
        self.active_month = int(self.current_date.month)
        self.active_year = int(self.current_date.year)

    def is_leap_year(self, year: int):
        if year % 4 == 0:
            return True
        return False

    def get_weekday(self, day, month, year):
        return datetime.date(year, month, day).weekday()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('Calendar.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Notes (id integer primary key,
                                                                      date text,
                                                                      note text)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS Setting (id integer primary key,
                                                              name text,
                                                              value text)''')
        self.conn.commit()

    def get_note_of_day(self, day, month, year):
        note = [i for i in self.c.execute('''SELECT note
                                          FROM Notes WHERE date="'''
                                          + self.formate_date(day, month, year)+'"')]
        if note == []:
            self.insert_day(day, month, year)
            return ""
        return note[0][0]

    def insert_day(self, day, month, year):
        self.c.execute('''INSERT INTO Notes (date, note) VALUES (?, ?)''',
                       (self.formate_date(day, month, year), ""))
        self.conn.commit()

    def is_noted_day(self, day, month, year):
        note = [i for i in self.c.execute('''SELECT note
                                                  FROM Notes WHERE date="'''
                                          + self.formate_date(day, month, year) + '"')]
        if note == []:
            return False
        elif note[0][0] == "":
            return False
        return True

    def modify_note_of_day(self, day, month, year, note):
        self.c.execute('''UPDATE Notes SET note=? WHERE date=?''',
                       (note, self.formate_date(day, month, year)))
        self.conn.commit()

    def formate_date(self, day, month, year):
        return str(day) + "." + str(month) + "." + str(year)

    def get_setting(self, name:str):
        value = [i for i in self.c.execute('''SELECT value FROM Setting WHERE name="''' + name + '''"''')]
        if value == []:
            return None
        return value[0][0]

    def insert_setting(self, name, value):
        self.c.execute('''INSERT INTO Setting (name, value) VALUES (?, ?)''',
                       (name, value))
        self.conn.commit()

    def update_setting(self, name, value):
        self.c.execute('''UPDATE Setting SET value=? WHERE name=?''', (value, name))
        self.conn.commit()
