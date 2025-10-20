import sys
import mysql.connector
from helper.log import set_log
from configs.globals import (
    collect_db_host,
    collect_db_user,
    collect_db_password,
    collect_db_name
)


def open_coll_connection():
     try:
          conn = mysql.connector.connect(
               host=collect_db_host,
               user=collect_db_user,
               password=collect_db_password,
               database=collect_db_name,
               connection_timeout=7200,
               read_timeout=7200,
               use_pure=True
          )
          set_log("Collection database connection established", "Info", open_coll_connection.__name__)
          return conn

     except mysql.connector.Error as err:
          set_log(str(err), "Error", open_coll_connection.__name__)
          raise Exception(str(err))
     except KeyboardInterrupt:
          set_log("Collection database connection closed by user", "Info", open_coll_connection.__name__)
          sys.exit(0)

def close_coll_connection(conn):
    if conn.is_connected():
        conn.close()
        set_log("Collection database connection closed", "Info", close_coll_connection.__name__)