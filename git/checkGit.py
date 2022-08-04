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
        cmt = [line.replace("\n","") for line in cat]
        all_cmt = cmt[-1].split(r"\n")
        for msg in all_cmt:
            res = re.match(msg_reg, msg, flags=0)
            if res != None:
                print(res + " 通过检查")
            else:
                print(msg + " 不符合规范")
