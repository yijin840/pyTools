import requests


u = "http://tech.meituan.com/2017/06/29/database-availability-architecture.html"

def main():
    response = requests.get(u)
    print(response.content)
    print(response.reason)
    
main()