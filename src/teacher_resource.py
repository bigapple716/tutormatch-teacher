import logging

import pymysql


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
    def _run_sql(sql):
        logging.info(sql)
        connection = TeacherResource._get_connection()
        cur = connection.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        return result

    @staticmethod
    def get_all_teachers():
        sql = "SELECT * FROM teacher_schema.teacher_info"
        return TeacherResource._run_sql(sql)

    @staticmethod
    def get_teachers_by_id(id):
        sql = "SELECT * FROM teacher_schema.teacher_info WHERE id = {}".format(id)
        return TeacherResource._run_sql(sql)

    @staticmethod
    def get_teachers_by_name(name):
        sql = "SELECT * FROM teacher_schema.teacher_info WHERE name = '{}'".format(name)
        return TeacherResource._run_sql(sql)

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
                WHERE skill_cnt.cnt = {} AND price >= {} AND price <= {}'''.format(tuple(skills), len(skills), price_min, price_max)
        return TeacherResource._run_sql(sql)

    @staticmethod
    def get_available_time_by_id_and_date(teacher_id, date):
        sql = """
            SELECT hour FROM teacher_schema.available_time
            WHERE teacher_id = {} AND date = '{}' AND occupied = 0""".format(teacher_id, date)

        return TeacherResource._run_sql(sql)


# main function is only for testing
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    res = TeacherResource.get_teachers_by_skills_and_price(skills=['Python', 'Java'], price_min=50, price_max=90)
    print(res)
