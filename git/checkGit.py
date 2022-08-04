# -*- coding: utf-8 -*-

from os import system
import sys
sys.path.insert(0, '..')
from loadProperties import Properties
from head.commonHead import *

#不同的地方注释规范可能不一样
msg_reg = "^(feature|fix|docs|style|refactor|perf|test|build|ci|chore|revert)\(.*\): #[1-9][0-9]{4,7} .{1,100}$"
mail_reg = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
ref_reg = "^refs/heads/[a-z0-9_/]+$"
properties = Properties("../.local/info.properties").getProperties()
GIT_REQUEST = properties['request']
USER_INFO = subprocess.Popen(GIT_REQUEST, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
def cmd(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.readlines()

def check(gcms):
    for m in gcms:
        cat = cmd(cat_cmd + m)
        check_commit(cat) 
        check_info(cat) 

def check_commit(cat):
    cmt = [line.replace("\n","") for line in cat][-1].split(r"\n")
    for msg in cmt:
        res = re.match(msg_reg, msg, flags=0)
        if res == None:
            print(msg + " 不符合规范")
            print("正确规范  type(scope): #RedmineIssueId 简述提交内容")
            sys.exit(0)

def check_info(cat):
    info = USER_INFO.communicate()
    print(info)
    info = info[0]
    if info == None or len(info) == 0:
        return
    user_json = json.loads(info)[0]
    info = [line.replace("\n","") for line in cat][3].split(" ")
    mail = info[2]
    name = info[1]
    if user_json['name'] != name or user_json['mail'] != mail and re.match(mail_reg, mail):
        print("邮箱和姓名不匹配!")
        sys.exit(0)

if __name__ == "__main__":
    print(GIT_REQUEST)
    rev_cmd = "git rev-list --all"
    rev = cmd(rev_cmd)
    cat_cmd = "git cat-file -p "
    # print(rev)
    gcms = [s[:-1] for s in rev]
    check(gcms)
    print("代码提交规范检查通过！")
