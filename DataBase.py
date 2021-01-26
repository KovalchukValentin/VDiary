import sqlite3
import datetime

class Date:
    def __init__(self):

        self.current_date = datetime.datetime.now()
        self.days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        self.active_day = int(self.current_date.day)
        self.active_month = int(self.current_date.month)
        self.active_year = int(self.current_date.year)

        if self.is_leap_year(self.current_date.year):
            self.days_in_months[1] = 29

        print(self.get_weekday(1, 1, 2021))

    def is_leap_year(self, year: int):
        if year % 4 == 0:
            return True
        return False

    def get_weekday(self, day, month, year):
        return datetime.date(year, month, day).weekday()




class DB:
    def __init__(self):
        pass


# class DB2:
#     def __init__(self):
#         self.data = time.strftime('%d.%m.%Y')
#         self.conn = sqlite3.connect('Calendar.db')
#         self.c = self.conn.cursor()
#         self.c.execute('''CREATE TABLE IF NOT EXISTS Specializations (id integer primary key,
#                                                                       title text,
#                                                                       last_name text,
#                                                                       name text,
#                                                                       middle_name text,
#                                                                       telephone text)''')
#
#         self.c.execute('''CREATE TABLE IF NOT EXISTS Scientific_works (id integer primary key,
#                                                                        specialization_id integer,
#                                                                        title text,
#                                                                        type_work text,
#                                                                        task text,
#                                                                        last_name text,
#                                                                        name text,
#                                                                        middle_name text,
#                                                                        telephone text,
#                                                                        data text,
#                                                                        complete bool)''')
#
#         self.c.execute('''CREATE TABLE IF NOT EXISTS Students (id integer primary key,
#                                                                specialization_id integer,
#                                                                task_id integer,
#                                                                last_name text,
#                                                                name text,
#                                                                middle_name text,
#                                                                specialization integer,
#                                                                course integer,
#                                                                group_name text,
#                                                                telephone text)''')
#         self.conn.commit()
#
#     def insert_specialization(self, title, last_name, name, middle_name, telephone):
#         self.c.execute('''INSERT INTO Specializations (title, last_name, name, middle_name, telephone)
#                           VALUES (?, ?, ?, ?, ?)''',
#                        (title, last_name, name, middle_name, telephone))
#         self.conn.commit()
#
#     def delete_specialization(self, specialization_id):
#         specialization_id = str(specialization_id)
#         self.c.execute('''DELETE FROM Specializations WHERE id=''' + specialization_id)
#         self.c.execute('''DELETE FROM Scientific_works WHERE specialization_id=''' + specialization_id)
#         self.c.execute('''DELETE FROM Students WHERE specialization_id=''' + specialization_id)
#         self.conn.commit()
#
#     def insert_scientific_work(self, specialization_id, title, type_work, task, last_name, name, middle_name, telephone):
#         self.c.execute('''INSERT INTO Scientific_works (specialization_id, title, type_work, task, last_name, name, middle_name, telephone, data)
#                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#                        (specialization_id, title, type_work, task, last_name, name, middle_name, telephone, self.data))
#         self.conn.commit()
#
#     def completing_scientific_work(self, scientific_work_id):
#         self.c.execute('''UPDATE Scientific_works SET complete='%s' WHERE id='%s' ''' % ("true", scientific_work_id))
#         self.conn.commit()
#
#     def delete_scientific_work(self, task_id):
#         task_id = str(task_id)
#         self.c.execute('''DELETE FROM Scientific_works WHERE id=''' + task_id)
#         self.c.execute('''DELETE FROM Students WHERE task_id=''' + task_id)
#         self.conn.commit()
#
#     def insert_student(self, specialization_id, task_id, last_name, name, middle_name, specialization, course, group_name, telephone):
#         self.c.execute('''INSERT INTO Students (specialization_id, task_id, last_name, name, middle_name, specialization, course, group_name, telephone)
#                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#                        (specialization_id, task_id, last_name, name, middle_name, specialization, course, group_name, telephone))
#         self.conn.commit()
#
#     def delete_student(self, student_id):
#         self.c.execute('''DELETE FROM Students WHERE id=''' + str(student_id))
#         self.conn.commit()
#
#     def get_select_specializations(self):
#         specializations = []
#         select_specializations = [i for i in self.c.execute('''SELECT id, title FROM Specializations LIMIT 10 ''')]
#         for num, i in enumerate(select_specializations):
#             specializations.append((i[0], str(num + 1) + ". " + i[1]))
#         return specializations
#
#     def get_select_scientific_works(self, specialization_id):
#         scientific_works = []
#         select_scientific_works = [i for i in self.c.execute('''SELECT id, title, type_work, data FROM Scientific_works WHERE specialization_id='''
#                                                              + str(specialization_id) + ''' AND complete IS NULL LIMIT 10''')]
#         if select_scientific_works == []:
#             return None
#         for num, i in enumerate(select_scientific_works):
#             scientific_works.append((i[0], str(num+1) + ". " + str(i[1]) + " | " + str(i[2]) + " | Дата: " + str(i[3])))
#         return scientific_works
#
#     def get_select_scientific_work(self, scientific_work_id):
#         select_scientific_work = [i for i in self.c.execute('''SELECT title, type_work, task, last_name, name,
#                                                                middle_name, telephone, data FROM Scientific_works WHERE id='''
#                                                              + str(scientific_work_id) + ''' LIMIT 10''')][0]
#         if select_scientific_work == []:
#             return None
#
#         scientific_work = [select_scientific_work[0],
#                            select_scientific_work[1],
#                            "\n                                                                     Завдання\n"
#                            + select_scientific_work[2] +
#                            "\n\nКеруючий: " + select_scientific_work[3] + ' ' +
#                                             select_scientific_work[4] + ' ' +
#                                             select_scientific_work[5] +
#                            "\nТелефон: " + select_scientific_work[6] +
#                            '''\n\n\n
#                                                                                                       Дата створення: '''
#                            + select_scientific_work[7]]
#
#         return scientific_work
#
#     def get_select_students(self, task_id):
#         students = []
#         select_students = [i for i in self.c.execute('''SELECT id, last_name, name, middle_name, group_name
#                                                         FROM Students WHERE task_id='''
#                                                      + str(task_id) + ''' LIMIT 10''')]
#         for num, i in enumerate(select_students):
#             students.append((i[0], (str(num+1) + ". " + ' '.join((i[1], i[2], i[3])) + " | Група: " + i[4])))
#         return students
#
#     def get_select_student(self, student_id):
#         select_student = [i for i in self.c.execute('''SELECT id, last_name, name, middle_name, specialization, course,
#                                                         group_name, telephone FROM Students WHERE id='''
#                                                      + str(student_id) + ''' LIMIT 10''')][0]
#
#         student = ("\nПІБ: " + ' '.join((select_student[1], select_student[2], select_student[3])) +
#                     '\n\nСпеціальність: ' + str(select_student[4]) +
#                     "\n\nКурс: " + str(select_student[5]) +
#                     "\n\nГрупа: " + str(select_student[6]) +
#                     "\n\nТелефон: " + str(select_student[7]))
#         return student
