import os

upath = os.path.expanduser('~')
# print(upath)
mdir = upath + "\.tools"

spath = "setx path " + mdir + " /m"
# cmd = "mkdir " + mdir
# setx "Path" ""
print(spath)
print("设置环境变量ing ......")
os.system(spath)
print("设置环境变量完毕")

# os.system(cmd)