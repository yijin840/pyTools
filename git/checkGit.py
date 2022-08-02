import sys
sys.path.insert(0, '..')

from head.commonHead import *

msg_reg = "^(feature|fix|docs|style|refactor|perf|test|build|ci|chore|revert)\(.*\): #[1-9][0-9]{4,7} .{1,100}$"
def cmd(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.readlines()
if __name__ == "__main__":
    rev_cmd = "git rev-list --all"
    rev = cmd(rev_cmd)
    cat_cmd = "git cat-file -p "
    # print(rev)
    gcms = [s[:-1] for s in rev]
    for m in gcms:
        cat = cmd(cat_cmd + m)
        for i in cat:
            print(i)
