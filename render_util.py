from jinja2 import Template
import os

dir_dict = {"java": "./templete/java", "page": "./templete/page"}
templete_dict = {}

def render_java_code(table_info):
    """渲染java文件"""
    dir = dir_dict["java"]
    file_name_arr = os.listdir(dir)
    for x in file_name_arr:
        if not x.endswith(".templete"):
            continue
        templete = get_templete(dir + "/" + x)
        result = templete.render(t=table_info)
        out_file_path = build_out_filename(x, table_info, ".java")
        out_file = open(file=out_file_path, mode="w", encoding="utf-8")
        out_file.write(result)
        out_file.flush()
        out_file.close()


def render_html_code(table_info):
    """渲染java文件"""
    # dir = dir_dict["page"]
    # file_name_arr = os.listdir(dir)
    # for x in file_name_arr:
    #     if not x.endswith(".templete"):
    #         continue
    #     templete = get_templete(dir + "/" + x)
    #     result = templete.render(t=table_info)
    #     out_file = open(file=build_out_filename(x, table_info, ".html"), mode="w", encoding="utf-8")
    #     out_file.write(result)
    #     out_file.flush()
    #     out_file.close()


def build_out_filename(tpl_name, table_info, file_type):
    out_file_name = "./autoCode/"

    if not os.path.exists(out_file_name):
        init_dir(out_file_name)

    if tpl_name.startswith("controller"):
        out_file_name += ("controller/" + table_info.model_name + "Controller")
    elif tpl_name.startswith("dto"):
        out_file_name += ("dto/" + table_info.model_name + "Dto")
    elif tpl_name.startswith("entity"):
        out_file_name += ("entity/" + table_info.model_name)
    elif tpl_name.startswith("IService"):
        out_file_name += ("service/" + table_info.service)
    elif tpl_name.startswith("serviceImpl"):
        out_file_name += ("impl/" + table_info.serviceImpl)
    elif tpl_name.startswith("mapper"):
        out_file_name += ("mapper/" + table_info.model_name + "Mapper")
    elif tpl_name.startswith("query"):
        out_file_name += ("query/" + table_info.model_name + "Query")
    elif tpl_name.startswith("edit"):
        out_file_name += ("/" + table_info.model_name + "/" + "edit")
    elif tpl_name.startswith("list"):
        out_file_name += ("/" + table_info.model_name + "/" + "list")
    out_file_name += file_type
    return out_file_name

def init_dir(path):
    os.mkdir(path)
    os.mkdir(path+"controller")
    os.mkdir(path+"dto")
    os.mkdir(path+"entity")
    os.mkdir(path+"service")
    os.mkdir(path+"impl")
    os.mkdir(path+"mapper")
    os.mkdir(path+"query")

## 缓存template 对象提高性能

def get_templete(filename):
    if filename not in templete_dict:
        templete = Template(open(file=filename, encoding="utf-8", mode="r").read())
        templete_dict[filename] = templete
        return templete
    return templete_dict[filename]
