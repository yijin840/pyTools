import logging
import yaml
import traceback


# 获取文件属性
def get_value(key, file_name):
    try:
        # 打开文件
        file = open(file_name, 'r', encoding="utf-8")
        value = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        list = str(key).split("#")
        for index in range(0, len(list)-1):
            value = value[list[index]]
        return value[list[-1]]
    except Exception as e:
        logging.error("get_value error, cause : " + traceback.format_exc())

