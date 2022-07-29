from gettext import find
import os
from re import T
import sys


def find_process(port):
    process = "netstat -ano | findstr " + port
    pids = list(map(lambda s : s.replace("  ", " "), os.popen(process).read().replace("  ", " ").split("\n")))
    pids = [pid.split(" ") for pid in pids]
    pids = [p[-1] for p in pids if len(p) >= 11 and p[2].split(":")[-1] == port]
    return pids
    
def kill_process(pid):
    kill_cmd = "taskkill /pid "+pid+" /f"
    os.system(kill_cmd)
    # print(kill_cmd)
    
if __name__ == '__main__': 
    ports = [sys.argv[i] for i in range(1, len(sys.argv))]
    for port in ports:
        print("开始终止当前端口" + port + "进程")
        pids = find_process(port)
        if(len(pids) == 0):
            print("当前端口没有进程")
            continue
        print("查找到的 pids 集合 ", end='')
        print(pids)
        for pid in pids:
            print("开始终止 " + pid + " 进程")
            kill_process(pid)
        print("当前端口进程终止完毕")
