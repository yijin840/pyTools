# -*- coding:utf-8 -*-
import paramiko
from scp import SCPClient
import sys


class ssh_client(object):
    _ssh = paramiko.SSHClient()
    _java_path = ""

    def __init__(self, host, port, user, password):
        self._ssh.load_system_host_keys()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(hostname=host, port=port,
                          username=user, password=password)

    def set_java_path(self, path):
        self._java_path = path

    def find_java_path(self):
        cmd = "bash -lc 'which java'"
        virtual_path = self.execute_cmd(cmd, get_pty=True, isPrint=False)
        if len(virtual_path) == 1:
            return virtual_path[0]
        else:
            return None

    def execute_cmd(self, main_cmd, vl=[], hl=[], get_pty=False, sync=False, isPrint=True):
        if len(vl) != 0:
            for v in vl:
                main_cmd = main_cmd + " | " + v
        if len(hl) != 0:
            for h in hl:
                main_cmd = main_cmd + " && " + h
        stdin, stdout, stderr = self._ssh.exec_command(
            main_cmd, get_pty=get_pty)
        if sync:
            self.std_print_sync(stdin, stdout, stderr)
        else:
            return self.std_print(stdin, stdout, stderr, isPrint)

    def find_pid_by_port(self, port):
        cmd = "lsof -i:%s | awk -F = 'NR==2{print $1}' | tr -s ' '|cut -d' ' -f2" % str(
            port)
        return self.execute_cmd(cmd)

    def execute_top_mem(self):
        stdin, stdout, stderr = self._ssh.exec_command(
            "top | grep -i mem", get_pty=True)
        self.std_print(stdin, stdout, stderr)

    def java_jps(self):
        cmd = "%s/jps" % self._java_path
        return self.execute_cmd(cmd)

    def java_jmap(self, pid):
        cmd = "%s/jmap -heap " % self._java_path + str(pid)
        return self.execute_cmd(cmd)

    def java_jstat_sync(self, pid):
        cmd = "%s/jstat -gcutil %s 5000 100" % str(self._java_path,
                                                   pid)
        print("  %s     %s     %s      %s      %s     %s    %s     %s    %s    %s     %s   \n'" % ('幸存1区当前使用比例', '幸存2区当前使用比例',
                                                                                                   '伊甸园区使用比例', '老年代使用比例', '元数据区使用比例', '压缩使用比例', '年轻代垃圾回收次数', '年轻代垃圾回收消耗时间', '老年代垃圾回收次数', '老年代垃圾回收消耗时间', '垃圾回收消耗总时间'))
        return self.execute_cmd(cmd, sync=True)

    '''
    进度条
    '''

    def progress(self, filename, size, sent):
        sys.stdout.write("%s\'s progress: %.2f%%   \r" %
                         (filename, float(sent)/float(size)*100))

    def std_print(self, stdin, stdout, stderr, isPrint=True):
        stdout._set_mode("rb")
        stderr._set_mode("rb")
        result_stdout = stdout.readlines()
        result_stderr = stderr.readlines()

        res = []
        for i in result_stdout:
            if isPrint:
                print(i.decode('utf-8', errors="ignore"), end="")
            res.append(str(i.decode('utf-8', errors="ignore")[:-1]))
        for i in result_stderr:
            if isPrint:
                print(i.decode('utf-8', errors="ignore"), end="")
        return res

    def std_print_sync(self, stdin, stdout, stderr):
        stdout._set_mode("rb")
        stderr._set_mode("rb")
        for line in iter(lambda: stdout.readline(2048), ""):
            print(line.decode('utf-8', errors="ignore"), end="")
            if line == "" or stdout.channel.exit_status_ready():
                break

    '''
     1. get True 是 从服务器拿
     2. get False 是 本地发送到服务器 
    '''

    def copy_file(self, origin, target, get=True):
        print("copy file ", origin, " to ", target)
        scp = SCPClient(self._ssh.get_transport(), progress=self.progress)
        if get:
            scp.get(remote_path=origin, local_path=target)
        else:
            scp.put(files=origin, target=target)
        scp.close()

    '''
    b      块特殊文件（缓冲的）
    c      字符特殊文件（无缓冲的）
    d      目录
    p      命名管道（FIFO）
    f      常规文件
    l      符号链接
    s      套接字
    '''

    def find(self, file_name, type=None, dir="~", deep_path=None):
        cmd = "find % s " % dir
        if type != None:
            cmd += " -type %s " % type
        if deep_path != None:
            cmd += " -maxdepth %s " % deep_path
        cmd += " -name '%s' 2>/dev/null " % (file_name)
        return self.execute_cmd(cmd, isPrint=False)

    def nohup_execute(self, cmd, log_path=None):
        if log_path != None:
            cmd = "nohup %s > %s 2>&1 &" % (cmd, log_path)
        return self.execute_cmd(cmd, isPrint=False)

    def run_jmeter(self, jmx, jtl_path, jmeter_path):
        cmd = "jmeter -n -t %s -l %s" % (jmx, jtl_path)
        self.nohup_execute(cmd, jmeter_path)

    def deploy_jar_project(self, jar, port, dir="~"):
        self.copy_file(jar, dir)
        # 端口必须得要，不然没办法启动起来
        if port != None:
            self.execute_cmd("kill -9 %s" % self.find_pid_by_port(port))
        return self.nohup_execute("java -jar %s" % jar, dir=dir)
