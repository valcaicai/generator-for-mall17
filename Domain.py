import str_util


class TableInfo(object):

    def __init__(self, table_name, comment):
        self.table_name = table_name
        self.comment = comment
        self.model_name = str_util.first_up(table_name)
        self.service = "I" + self.model_name + "Service"
        self.serviceImpl = self.model_name + "Service"
        self.response = self.model_name + "Response"
        self.cols = []

    def init_col(self, col_arr):
        self.cols = col_arr


## 列信息
class ColumnInfo(object):

    def __init__(self, name, type, nullable, key, default, comment) -> None:
        super().__init__()
        self.name = name
        self.col_name = name
        self.up_name = str_util.first_up(name)
        self.col_type = type.lower()
        self.nullable = nullable
        self.key = key
        self.default = default
        self.comment = comment
        self.convert_col_to_filed_statement()
        self.convert_col_to_getter_and_setter()
        self.convert_col_condition()

    def convert_col_to_filed_statement(self):
        statement = "private "
        self.type = None
        if self.col_type.startswith("varchar") | self.col_type.startswith("char") | self.col_type.startswith("blob") | self.col_type.startswith("text"):
            self.type = "String"
        elif self.col_type.startswith("integer") | self.col_type.startswith("int"):
            self.type = "Integer"
        elif self.col_type.startswith("tinyint"):
            self.type = "Boolean"
        elif self.col_type.startswith("double"):
            self.type = "Double"
        elif self.col_type.startswith("timestamp") | self.col_type.startswith("datetime"):
            self.type = "java.sql.Timestamp"
        elif self.col_type.startswith("decimal"):
            self.type = "java.math.BigDecimal"
        elif self.col_type.startswith("bigint"):
            self.type = "Long"
        else:
            raise Exception("暂时不支持的数据类型：" + self.col_type)
        statement += self.type
        statement += " "
        statement += self.name
        statement += ";\n"
        self.statement = statement

    def convert_col_to_getter_and_setter(self):
        self.getter = "public "+self.type+" get"+str_util.first_up(self.name)+"()"+"{\n" + "\t\treturn this." + self.name+";\n\t}"
        self.setter = "public void set"+str_util.first_up(self.name)+"("+self.type + " " + self.name+")"+"{\n" +"\t\tthis."+ self.name+"="+self.name+";\n\t}"

    def col_filter(self,col_name):
        if (col_name=="id") | (col_name=="createdDate") |(col_name=="cteatedDate") | (col_name=="deleted") | (col_name=="version"):
            return False
        return True

    def convert_col_condition(self):
        condition = ""
        if self.type == "String":
            condition = "if(!Strings.isNullOrEmpty(getEntity().get"+self.up_name+"())){\n"
            condition += "\t\t\tcondition.like(\""+self.name+"\",getEntity().get"+self.up_name+"());\n"
            condition += "\t\t}"
        else:
            condition = "if(getEntity().get" + self.up_name + "()!=null){\n"
            condition += "\t\t\tcondition.eq(\"" + self.name + "\",getEntity().get" + self.up_name + "());\n"
            condition += "}\t\t"
        self.condition = condition
