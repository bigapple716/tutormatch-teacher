import pymysql

import os


class TeacherResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        connection = pymysql.connect(
            user='root',
            password='Bluesun777!',
            host='localhost',
            port=3306,
        )
        return connection

    @staticmethod
    def get_by_key(key):
        sql = "SELECT * FROM teacher_schema.teacher_info where id = 1"
        connection = TeacherResource._get_connection()
        cur = connection.cursor()
        cur.execute(sql, args=key)
        result = cur.fetchone()

        return result

