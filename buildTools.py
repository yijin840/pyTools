import os

upath = os.path.expanduser('~')

mdir = upath + "\.tools"
a = os.getenv("path")

def get_path():
    return os.getenv("path")
def set_path():
    os.environ["path"] = mdir + ";" + a

if __name__ == "__main__":
    cur_path = get_path()
    print(cur_path)