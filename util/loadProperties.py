# 读取Properties文件类
class Properties:
    def __init__(self, file_name):
        self.file_name = file_name
 
    def getProperties(self):
        try:
            pro_file = open(self.file_name, 'r', encoding='utf-8')
            properties = {}
            for line in pro_file:
                if line.find('=') > 0:
                    left = line[0:line.find("=")]
                    right = line[line.find("=")+1:]
                    properties[left] = right
        except Exception as e:
            raise e
        else:
            pro_file.close()
        return properties