#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

#ga-mmmk-client 接口测试
import yaml
import requests
import json
import os
import traceback

f = open('config.yml', 'r', encoding='utf-8')
config = yaml.safe_load(f)
project_name = config['project_name']
project_path = config['project_root_path']
swagger_ui_html = config['swagger_ui_html']
api_file = project_name + ".json"
api_data = config['api_data']
headers = {}
for k in config['headers']:
    headers[k] = config['headers'][k]
f.closed

def read_api_info():
    assert os.path.exists(api_file) == True, 'json配置文件不存在'
    with open(api_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    f.close()
    return json_data
    
#接口测试， url， params， result
def api_test(url, json_data): 
    try:
        if api_data.count(url) == 0:
            return
        
        lastad = url.split("/")[-1]
        params = json_data[url]['params']
        result = json_data[url]['result']
        uri = project_path + url
        
        if lastad.startswith("{") and lastad.endswith("}"):
            uri = project_path + url.replace(lastad, list(params.values())[0])
        print(uri)
        
        http_mode = list(json_data[url].keys())[0]
        content = ""
        if http_mode == 'get':
            content = requests.get(uri, params=params, headers=headers)
        else:
            content = requests.post(uri, json=params, headers=headers)
            
        res = json.loads(content.content.decode("utf-8"))
        
        if res['code'] != '0' or res['result'] != result:
            print("\033[31m",uri + '  当前测试未通过!!!',"\033[0m")
            print("\033[31m",params, "\033[0m")
            print("\033[31m","origin data " + result, "\033[0m")
            print("\033[31m",res, "\033[0m")
        else:
            print("\033[32m",uri + '  当前测试结果已通过!!!',"\033[0m")
            print("\033[32m",params, "\033[0m")
            print("\033[32m",res, "\033[0m")
    except Exception:
        print("\033[31m",uri + '  当前测试未通过!!!',"\033[0m")
        print("\033[31m",params, "\033[0m")
        print("\033[31m",traceback.format_exc(), "\033[0m")
        
    print("===================================================================================")
    
    
if __name__ == "__main__":
    #接口写入json文件
    json_paths = read_api_info()
    for u in json_paths:
        api_test(u, json_paths)
    
