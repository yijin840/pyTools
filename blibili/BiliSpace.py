# -*- coding: utf-8 -*-

import requests
import json
import os
import sys
import hashlib

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54",
    "Cookie": "innersign=0; buvid3=4B09F15B-CBFF-9B88-1CE4-934D532517AF60472infoc; b_nut=1692684560; i-wanna-go-back=-1; b_ut=7; b_lsid=1DE10EFCE_18A1BDCA611; _uuid=739810EA2-3154-1861-D793-102313391098B359898infoc; header_theme_version=undefined; home_feed_column=4; browser_resolution=1033-606; buvid4=03A4948C-185F-28B4-B823-077D6F4469CE61391-023082214-F0gxg%2Bzv2R92%2Fzf2iMN6bQ%3D%3D; bili_ticket=eyJhbGciOiJFUzM4NCIsImtpZCI6ImVjMDIiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2OTI5NDM3NjUsImlhdCI6MTY5MjY4NDU2NSwicGx0IjotMX0.pYj06dnRnGj2c7pon-uzZ9pjPiY08M8uvA1eVyL8kEn4pVJjrPM7dW1C4K6Aqf7hlWKz3ttdvJvQ95LsMLbryKk6kclKQUxGrNHgZ8Wa5E2D8B-XAKG4qWY-81ohgXhK; bili_ticket_expires=1692943765; fingerprint=952ae08576a84835337ff357c7743890; buvid_fp=11CEFAB0-DF25-4695-58D6-E58BA844835A75869infoc; buvid_fp_plain=undefined",
}

retryData = {}
debugger = False

## 用法： python -u BiliSpace.py "UserId" "xxx/xxx(指定路径)"


class BiliSpace:
    spaceUrl = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=%s&host_mid=%s&timezone_offset=-480&features=itemOpusStyle"
    # 用户ID
    spaceId = -1
    dirPath = "/"
    reTryCount = 0

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
        return self.dynamic(self.getId(response, -1, offset))

    def getId(self, response, isLast, offset) -> str:
        jsonData = json.loads(response.text)
        if jsonData["code"] != 0:
            if self.reTryCount == 0:
                self.reTryCount += 1
                ## 重试
                self.retry(response)
                self.dynamic(offset)
                return
            print(response.content.decode("utf-8"))
            raise RuntimeError("code is not 0")
        itemsJson = jsonData["data"]["items"]
        if len(itemsJson) == 0:
            return None
        self.get_values_by_key(itemsJson, "src")
        return itemsJson[isLast if -1 else 0]["id_str"]
        
    def retry(self, resp):
        #出错需要过验证码校验
        retryData['X-Bili-Gaia-Vvoucher'] = resp.headers['X-Bili-Gaia-Vvoucher']
        voucherResp = requests.post(
            "https://api.bilibili.com/x/gaia-vgate/v1/register",
            data=retryData,
            headers=headers,
        )
        print("retryData ===> ", retryData)
        print("voucher ===> ", voucherResp.content.decode("utf-8"))
        print("retry success. retry count is %s" % self.reTryCount)

    def get_values_by_key(self, json_obj, target_key):
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                if key == target_key:
                    endwithIdent = value[value.rindex(".") : len(value)]
                    imgFileName = hashlib.md5(value.encode("utf-8")).hexdigest()
                    print(imgFileName)
                    if endwithIdent.count("?") != 0:
                        endwithIdent = endwithIdent[: endwithIdent.rindex("?")]
                    self.downloadResource(value, imgFileName + endwithIdent)
                self.get_values_by_key(value, target_key)
        elif isinstance(json_obj, list):
            for item in json_obj:
                self.get_values_by_key(item, target_key)

    def downloadResource(self, url: str, fileName: str):
        response = requests.get(url, headers=headers)
        if os.path.exists(self.dirPath + fileName):
            print("%s file exists" % fileName)
            return
        with open(self.dirPath + fileName, "wb") as f:
            f.write(response.content)


if __name__ == "__main__":
    id = sys.argv[1]
    path = sys.argv[2]
    print("space Id is %s" % id)
    print("path is %s" % path)
    space = BiliSpace(id, path)
    space.dynamic()
