# -*- coding: utf-8 -*-

import requests
import json
import uuid as UUID
import os
import sys

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54",
    "Cookie": "buvid3=E96441D3-5ED9-F126-E581-8513EB68885B55588infoc; b_nut=1692640355; b_lsid=955111A2_18A193A24B8; _uuid=2E2DF3FF-F10B1-5997-10F101-96C9D46A6A1655523infoc; buvid4=C6679B55-E8B1-6968-0047-45366AACED5956405-023082201-F0gxg+zv2R92/zf2iMN6bQ%3D%3D; buvid_fp=952ae08576a84835337ff357c7743890; bili_ticket_expires=1692899556; bili_ticket=eyJhbGciOiJFUzM4NCIsImtpZCI6ImVjMDIiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2OTI4OTk1NTYsImlhdCI6MTY5MjY0MDM1NiwicGx0IjotMX0.3VsEZ3RxzCqYswqsNYps4ThISYFxHfNpP2VFMaiHJVy3ikDJebuMOx5YmuHH5gipX1EJ7KxpFvT3R4p4Xbg6X0XWzJl4FEdMkVtkNTx7G_jfFe2Cux2TU03WdsXYpaMQ",
}
debugger = False


## 用法： python -u BiliSpace.py "UserId" "xxx/xxx(指定路径)"

class BiliSpace:
    spaceUrl = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=%s&host_mid=%s&timezone_offset=-480&features=itemOpusStyle"
    # 用户ID
    spaceId = -1
    dirPath = "/"

    def __init__(self, spaceId: str = None, dirPath: str = None):
        self.spaceId = spaceId
        self.dirPath = dirPath + self.spaceId + "/"
        print(self.dirPath)
        print(os.path.exists(self.dirPath) == False)
        if os.path.exists(self.dirPath) == False:
            os.mkdir(self.dirPath)
        if debugger:
            exit(0)

    # offset 居然是下一页第一条动态ID
    # 获取动态信息 filter 过滤条件
    def dynamic(self, offset=""):
        if debugger:
            print(offset)
        if offset == None:
            print("dynamic get end")
            return
        if self.spaceId == -1:
            raise RuntimeError("id is null")
        response = requests.get(self.spaceUrl % (offset, self.spaceId), headers=headers)
        if debugger:
            print(response.text)
        return self.dynamic(self.getId(response.text, -1))

    def getId(self, data: dict, isLast) -> str:
        jsonData = json.loads(data)
        if jsonData["code"] != 0:
            raise RuntimeError("code is not 0")

        itemsJson = jsonData["data"]["items"]
        if len(itemsJson) == 0:
            return None
        self.get_values_by_key(itemsJson, "src")
        return itemsJson[isLast if -1 else 0]["id_str"]

    def get_values_by_key(self, json_obj, target_key):
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                if key == target_key:
                    endwithIdent = value[value.rindex(".") : len(value)]
                    if endwithIdent.count("?") != 0:
                        endwithIdent = endwithIdent[: endwithIdent.rindex("?")]
                    self.downloadResource(value, UUID.uuid1().hex + endwithIdent)
                self.get_values_by_key(value, target_key)
        elif isinstance(json_obj, list):
            for item in json_obj:
                self.get_values_by_key(item, target_key)

    def downloadResource(self, url: str, fileName: str):
        response = requests.get(url, headers=headers)
        with open(self.dirPath + fileName, "wb") as f:
            f.write(response.content)


if __name__ == "__main__":
    id = sys.argv[1]
    path = sys.argv[2]
    print("space Id is %s" % id)
    print("path is %s" % path)
    space = BiliSpace(id, path)
    space.dynamic()
