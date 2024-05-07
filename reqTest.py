import requests
import random

url = "https://hwdms.mot.gov.cn/BMWebSite/company/baseTab.do?id=1c385fc53fc14232bd5752d501e43667&type=0"
u = "https://hwdms.mot.gov.cn/BMWebSite/company/getCompanyAptitudeTab.do"

params = {
    "text": "中铁十八局集团第五工程有限公司",
    "page": 1,
    "rows": 15,
    "type": 0,
    "caname": "",
    "regProvinceCode": "",
    "catype": "",
    "grade": "",
}
header = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Cookie": "JSESSIONID=B23E342E76AE3AA6EE9654EC5A03DB62",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def main():
    html = requests.post(url=u, params=params, headers=header, timeout=5)
    print(html.content.decode())


main()
