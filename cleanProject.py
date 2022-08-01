from head.commonHead import *

remove_dirs = ["build", "dist", "__pycache__", r".*\.spec"]

def rm_dir(name):
    for r in os.listdir(name):
        dr = os.path.join(name, r)
        if(os.path.isdir(dr)):
            rm_dir(dr)
        for p in remove_dirs:
            if re.match(p, r, flags=0):
                if os.path.isdir(dr):
                    print("删除文件夹 ===> " + dr)
                    shutil.rmtree(dr)
                else:
                    print("删除文件 =====> " + dr);
                    os.remove(dr)

if __name__ == "__main__":
    for name in os.listdir("."):
        if(os.path.isdir(name)):
            rm_dir(name)
    