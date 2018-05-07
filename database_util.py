import mysql.connector
from Domain import TableInfo, ColumnInfo


class DatabaseUtil(object):
    table_info = []

    user = None
    password = None
    database = None

    def __init__(self, **kwargs):
        if ("user" not in kwargs) | ("database" not in kwargs) | ("password" not in kwargs):
            raise Exception("check args,make sure you have user&password&database args")
        self.user = kwargs["user"]
        self.password = kwargs["password"]
        self.database = kwargs["database"]

    def get_connection(self):
        """get mysql connection"""
        return mysql.connector.connect(user=self.user, password=self.password, database=self.database)

    def get_table_info(self):
        """get table info and recursive load each table's col info """
        conn = self.get_connection()
        info = conn.cursor()
        info.execute("show table status")
        for table in info:

            ## ignore foreign key table

            if table[0].startswith("f_"):
                continue
            table_info = TableInfo(table[0], table[len(table) - 1])
            table_info.init_col(self.get_col_info(table[0]))
            self.table_info.append(table_info)

    def get_col_info(self, table_name):
        col_arr = []
        conn = self.get_connection()
        info = conn.cursor()
        info.execute("show full fields from " + table_name)
        for x in info:
            if not ColumnInfo.col_filter(None,x[0]):
                ## 过滤公共属性
                continue
            col = ColumnInfo(x[0], x[1], x[3], x[4], x[5], x[8])
            col_arr.append(col)
        return col_arr

