import psycopg2 as pg
import psycopg2.extras as ex
from logging import basicConfig, INFO, getLogger, DEBUG, error, warning
import time
from datetime import datetime

log = getLogger('Connector log ')
basicConfig(level=DEBUG)

def perf_check(f):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = f(*args, **kwargs)
        log.info(f'{f.__name__} took {round(time.perf_counter()-start, 2)} second(s)')
        return res
    return wrapper


class POSTGRESS:
    def __init__(self, DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT=5432):
        self.DB_NAME = DB_NAME
        self.DB_USER = DB_USER
        self.DB_PASS = DB_PASS
        self.DB_HOST = DB_HOST
        self.DB_PORT = DB_PORT

        try:
            self.conn = pg.connect(dbname=self.DB_NAME,
                                   user=self.DB_USER,
                                   password=self.DB_PASS,
                                   host=self.DB_HOST,
                                   port=self.DB_PORT)
            log.info('[SUCCESS] Connection to Postgres ...')
        except Exception as e:
            log.error('[ERROR] Connecting to Postgres: '+str(e))

    @perf_check
    def create_query(self, column_list, schema, table, where_condition, order_by=None):
        query = "SELECT"
        if where_condition is None:
            where_condition = "1=1"

        if order_by is not None:
            order = f'ORDER BY {order_by}'

        if column_list is None or column_list == '':
            query = f"SELECT * FROM {schema}.{table} WHERE {where_condition} {order} "
        else:
            query = f"""SELECT {column_list} FROM {schema}.{table} WHERE {where_condition} {order}"""

        return query

    @perf_check
    def select(self, column_list=None, schema=None, table=None, where_condition=None, order_by=None, query=None):
        try:
            sql = query
            if query is None:
                sql = self.create_query(column_list, schema, table, where_condition, order_by)

            with self.conn.cursor(cursor_factory = ex.RealDictCursor) as cur:
                cur.execute(sql)
                records = cur.fetchall()
                log.info('[SUCCESS] Data Retrieved')
                return records

        except Exception as e:
            log.error('[ERROR] Fetching Postgres data: '+str(e))

    def close_conn(self):
        if self.conn:
            self.conn.close()
        log.info("[SUCCESS] Postgres connection closed!")
