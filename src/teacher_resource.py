import logging
import os

import pymysql


class TeacherResource:
    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        # connect to my local database
        # connection = pymysql.connect(
        #     user='root',
        #     password='Bluesun777!',
        #     host='localhost',
        #     port=3306,
        #     autocommit = True
        # )
        connection = pymysql.connect(
            user='root',
            password=os.environ.get("DBPASSWORD"),
            host=os.environ.get("DBHOST"),
            port=3306,
            autocommit=True
        )
        return connection

    @staticmethod
    def _run_sql(sql):
        logging.info(sql)
        connection = TeacherResource._get_connection()
        cur = connection.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        return result

    @staticmethod
    def _run_insert_sql(sql):
        last_id_sql = 'SELECT LAST_INSERT_ID() FROM teacher_schema.teacher_info LIMIT 1'

        logging.info(sql)
        connection = TeacherResource._get_connection()
        cur = connection.cursor()
        cur.execute(sql)
        cur.execute(last_id_sql)
        for row in cur:
            return row[0]

    @staticmethod
    def get_all_teachers():
        sql = "SELECT id, name, price, introduction FROM teacher_schema.teacher_info"
        return TeacherResource._run_sql(sql)

    @staticmethod
    def get_teachers_by_id(id):
        sql = "SELECT id, name, price, introduction FROM teacher_schema.teacher_info WHERE id = {}".format(id)
        return TeacherResource._run_sql(sql)

    # deprecated
    @staticmethod
    def get_teachers_by_name(name):
        sql = "SELECT * FROM teacher_schema.teacher_info WHERE name = '{}'".format(name)
        return TeacherResource._run_sql(sql)

    # deprecated
    @staticmethod
    def get_teachers_by_price_range(price_min, price_max):
        sql = "SELECT * FROM teacher_schema.teacher_info WHERE price >= {} AND price <= {}" \
            .format(price_min, price_max)
        return TeacherResource._run_sql(sql)

    @staticmethod
    def get_teachers_by_skills(skills):
        if len(skills) == 1:
            sql = """
                SELECT info.id, info.name, info.price, info.introduction
                FROM teacher_schema.skills JOIN teacher_schema.teacher_info info on info.id = skills.teacher_id
                WHERE skill_name = '{}' """.format(skills[0])
        else:
            sql = '''
                SELECT info.id, info.name, info.price, info.introduction
                FROM (
                         SELECT teacher_id, count(*) as cnt
                         FROM teacher_schema.skills
                         WHERE skill_name IN {}
                         GROUP BY teacher_id
                     ) skill_cnt
                         JOIN teacher_schema.teacher_info info ON skill_cnt.teacher_id = info.id
                WHERE skill_cnt.cnt = {}'''.format(tuple(skills), len(skills))
        return TeacherResource._run_sql(sql)

    @staticmethod
    def get_teachers_by_skills_and_price(skills, price_min, price_max):
        if len(skills) == 1:
            sql = """
                SELECT info.id, info.name, info.price, info.introduction
                FROM teacher_schema.skills
                         JOIN teacher_schema.teacher_info info on info.id = skills.teacher_id
                WHERE skill_name = '{}' AND price >= {} AND price <= {}""".format(skills[0], price_min, price_max)
        else:
            sql = '''
                SELECT info.id, info.name, info.price, info.introduction
                FROM (
                         SELECT teacher_id, count(*) as cnt
                         FROM teacher_schema.skills
                         WHERE skill_name IN {}
                         GROUP BY teacher_id
                     ) skill_cnt
                         JOIN teacher_schema.teacher_info info ON skill_cnt.teacher_id = info.id
                WHERE skill_cnt.cnt = {} AND price >= {} AND price <= {}'''.format(tuple(skills), len(skills),
                                                                                   price_min, price_max)
        return TeacherResource._run_sql(sql)

    @staticmethod
    def add_teacher_info(name, price, introduction):
        sql = """
            INSERT INTO teacher_schema.teacher_info (name, price, introduction)
            VALUES ('{}', {}, '{}')""".format(name, price, introduction)
        id = TeacherResource._run_insert_sql(sql)
        return id

    @staticmethod
    def get_available_time_by_id_and_date(teacher_id, date):
        sql = """
            SELECT hour FROM teacher_schema.available_time
            WHERE teacher_id = {} AND date = '{}' AND occupied = 0""".format(teacher_id, date)
        return TeacherResource._run_sql(sql)

    @staticmethod
    def update_available_time_by_id_and_date(teacher_id, date, hour, occupied):
        sql = """
            UPDATE teacher_schema.available_time
            SET occupied = {}
            WHERE teacher_id = {} AND date = '{}' AND hour = {}""".format(occupied, teacher_id, date, hour)
        return TeacherResource._run_sql(sql)

    @staticmethod
    def get_skills_by_ids(teacher_ids):
        if len(teacher_ids) == 1:
            sql = '''
                SELECT teacher_id, skill_name
                FROM teacher_schema.skills
                WHERE teacher_id = {}
                ORDER BY teacher_id'''.format(teacher_ids[0])
        else:
            sql = '''
                SELECT teacher_id, skill_name 
                FROM teacher_schema.skills 
                WHERE teacher_id IN {}
                ORDER BY teacher_id'''.format(tuple(teacher_ids))
        return TeacherResource._run_sql(sql)

    @staticmethod
    def add_skill(teacher_id, skill):
        sql = """
            INSERT INTO teacher_schema.skills (teacher_id, skill_name)
            VALUES ({}, '{}')""".format(teacher_id, skill)
        return TeacherResource._run_sql(sql)


# main function is only for testing
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    res = TeacherResource.get_skills_by_ids([1,2])
    print(res)
