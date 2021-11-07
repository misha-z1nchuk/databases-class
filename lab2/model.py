import time
from middleware.sqlmiddle import origin_type
import psycopg2


class Model:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                user="postgres",
                password="root",
                host="localhost",
                port=5432,
                database="blog",
            )
            self.cursor = self.connection.cursor()
        except:
            print('Error connection to db')

    def add_table(self, records, sql_insert_query):
        try:
            cursor = self.connection.cursor()
            cursor.executemany(sql_insert_query, records)
            self.connection.commit()
            print(cursor.rowcount, "Record successfully inserted")
        except (Exception, psycopg2.Error) as error:
            print("Failed inserting record into table {}".format(error))
            self.connection.rollback()
        finally:
            if self.connection:
                cursor.close()

    def only_possible(self, val, num, err_func):
        try:
            rec = [(val,)]
            sql_origin = origin_type(num)
            curs = self.connection.cursor()
            curs.execute(sql_origin, rec)
            records = curs.fetchall()
            if records[0] is None:
                for row in records:
                    print("There is row with id: ", row[0])
        except (Exception, psycopg2.Error) as error:
            print("Failed, there are no records with such id: {}".format(error))
            err_func()
        finally:
            if self.connection:
                curs.close()

    def update_table(self, records, sql_update_query):
        try:
            cursor = self.connection.cursor()
            cursor.executemany(sql_update_query, records)
            self.connection.commit()
            row_count = cursor.rowcount
            print(row_count, "Records Updated")
        except (Exception, psycopg2.Error) as error:
            print("Failed updating record of the table {}", error)
            self.connection.rollback()
        finally:
            if self.connection:
                cursor.close()

    def del_table(self, records, sql_delete_query):
        try:
            cursor = self.connection.cursor()
            cursor.executemany(sql_delete_query, records)
            self.connection.commit()
            print(cursor.rowcount, "Record deleted")
        except (Exception, psycopg2.Error) as error:
            print("Failed deleting record into table {}".format(error))
            self.connection.rollback()
        finally:
            if self.connection:
                cursor.close()

    def show_table(self, sql_select_query, tab, record, bool):
        try:
            self.cursor = self.connection.cursor()
            if bool:
                beg = int(time.time() * 1000)
            self.cursor.execute(sql_select_query, record)
            if bool:
                end = int(time.time() * 1000) - beg
                print("Time of request", end, " ms")
            records = self.cursor.fetchall()
            #print_table(records, tab)
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            self.connection.rollback()
        finally:
            if self.connection:
                self.cursor.close()
            return records


