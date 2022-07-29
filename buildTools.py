import os

upath = os.path.expanduser('~')

mdir = upath + "\.tools"
a = os.getenv("path")

# print(a)
spath = "set path \"" + os.getenv("path") + ";" + mdir + "\" /m"
# spath = "setx path \"" + os.getenv("path") + ";" + mdir + "\" /m"
cmd = "mkdir " + mdir
s = os.getenv("Path") + ";" + mdir
print(s)
os.putenv("path", "%s"%s)
# print(mdir)
print()
print(os.getenv("path"))
commands.getoutput('java -version')
# print("设置环境变量ing ......")
# os.system(spath)
# print("设置环境变量完毕")

# os.system(cmd)