#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

#ga-mmmk-client 生成配置文件
import requests
import json
import os
import yaml

f = open('config.yml', 'r', encoding='utf-8')
config = yaml.safe_load(f)
project_name = config['project_name']
project_path = config['project_path']
swagger_ui_html = config['swagger_ui_html']
api_file = project_name + ".json"
f.closed    
def write_api_info(info):
    with open(api_file, "a", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)
    f.close()
    
def generate_json_file(json_paths):
    if os.path.exists(api_file):
        os.remove(api_file)
    paths_len = len(json_paths)
    count = 0
    json_data = "{"
    for item in json_paths:
        json_paths[item]['params'] = ""
        json_paths[item]['result'] = ""
        json_data = json_data + "\"" + item + "\"" + ":" + json.dumps(json_paths[item]);
        if(count == paths_len - 1):
            break
        json_data = json_data + ","
        count = count + 1
    json_data = json_data + "}"
    write_api_info(json.loads(json_data))
    
if __name__ == "__main__":
    response = requests.get(project_path + swagger_ui_html)
    content = response.content.decode()
    json_content = json.loads(content)
    #接口写入json文件
    json_paths = json_content['paths']
    generate_json_file(json_paths)
