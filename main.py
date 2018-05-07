from database_util import DatabaseUtil
import render_util

databaseUtil = DatabaseUtil(user="root", password="123456", database="mall17")
databaseUtil.get_table_info()

table_infos = databaseUtil.table_info

## render templete
# for t in table_infos:
#     render_util.render_java_code(t)


a = "headImage"
a = a[0].capitalize()+a[1:]
