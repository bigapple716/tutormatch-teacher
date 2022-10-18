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
        # logging.info(sql)
        print(sql)
        connection = TeacherResource._get_connection()
        cur = connection.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        return result

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
            sql = "SELECT teacher_id FROM teacher_schema.skills WHERE skill_name = '{}'".format(skills[0])
        else:
            sql = '''
                SELECT teacher_id 
                FROM (
                    SELECT teacher_id, count(*) as cnt 
                    FROM teacher_schema.skills 
                    WHERE skill_name IN {} 
                    GROUP BY teacher_id) skill_cnt 
                WHERE skill_cnt.cnt = {}'''.format(tuple(skills), len(skills))
        return TeacherResource._run_sql(sql)


# main function is only for testing
if __name__ == '__main__':
    res = TeacherResource.get_teachers_by_skills(['Python', 'Java'])
    print(res)
