# -*- coding:utf-8 -*-
import paramiko
from scp import SCPClient
import sys
import re
import time
from paramiko.channel import ChannelStdinFile


class ssh_client(object):
    _ssh = paramiko.SSHClient()
    _java_path = ""
    _channel = any

    _name = ""
    _host = ""
    _port = ""
    _password = ""
    # 初始化

    def __init__(self, host, port, user, password, name):
        self._ssh.load_system_host_keys()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(hostname=host, port=port,
                          username=user, password=password)
        self._name = name
        self._host = host
        self._port = port
        self._password = password
        self._channel = self._ssh.get_transport().open_session()

    # 设置Java路径
    def set_java_path(self, path):
        self._java_path = path

    # 查找Java路径
    def find_java_path(self, cmd="which java"):
        virtual_path = self.execute_cmd(cmd, get_pty=True, isPrint=False)
        fd = virtual_path[0].find("->")
        if fd != -1:
            virtual_path[0] = virtual_path[0][fd+3:] 
        if len(virtual_path) == 0:
            return None
        virtual_path[0] = virtual_path[0].strip('\r').strip(' ')
        if virtual_path[0] == "/usr/bin/java" or virtual_path[0] == "/etc/alternatives/java":
            return self.find_java_path("bash -lc 'ls -lrt " + virtual_path[0] + "'")
        else:
            return virtual_path[0]

    '''
        1. main_cmd: 主命令
        2. vl: 管道命令
        3. hl: 逻辑命令
        4. get_pty: 是否开启新的终端，一般用于top这种需要持续输出的命令
        5. isPrint: 是否打印输出,默认打印
    '''

    def execute_cmd(self, main_cmd, vl=[], hl=[], get_pty=False, isPrint=True, isPw=False):
        if main_cmd == "" or main_cmd == None:
            return
        if len(vl) != 0:
            for v in vl:
                main_cmd = main_cmd + " | " + v
        if len(hl) != 0:
            for h in hl:
                main_cmd = main_cmd + " && " + h
        stdin, stdout, stderr = self._ssh.exec_command(
            main_cmd, get_pty=get_pty)
        if isPw:
            stdin.write(self._password + "\n")
            stdin.flush()
        return self.std_print(stdin, stdout, stderr, isPrint)

    '''
        1. 根据端口号查看进程号
    '''

    def find_pid_by_port(self, port):
        cmd = "lsof -i:%s | awk -F = 'NR==2{print $1}' | tr -s ' '|cut -d' ' -f2" % str(
            port)
        return self.execute_cmd(cmd)

    '''
        1.执行top命令
    '''

    def execute_top_mem(self):

        stdin, stdout, stderr = self._ssh.exec_command(
            "top | grep -i mem", get_pty=True)
        self.std_print(stdin, stdout, stderr)

    '''
        1. jps查看java进程，需要设置java环境，因为可能存在多种Java环境
    '''

    def java_jps(self):
        cmd = "%s/jps" % self._java_path
        return self.execute_cmd(cmd)

    '''
        1. jmap查看java内存对象，需要设置java环境，因为可能存在多种Java环境
    '''

    def java_jmap(self, pid):
        cmd = "%s/jmap -heap " % self._java_path + str(pid)
        return self.execute_cmd(cmd)

    '''
        1. jmap查看jvm参数数据，需要设置java环境，因为可能存在多种Java环境
        2. 默认异步输出，不能停止，谨慎使用
    '''

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
    '''
        1. 打印输出
        2. stdin 输入
        3. stdout 输出
        4. stderr 错误输出
        5. isPrint 是否打印输出
    '''

    def std_print(self, stdin: ChannelStdinFile, stdout: ChannelStdinFile, stderr: ChannelStdinFile, isPrint=True):
        stdout._set_mode("rb")
        stderr._set_mode("rb")
        res = []
        for line in iter(lambda: stdout.readline(2048), ""):
            if isPrint:
                print(line.decode('utf-8', errors="ignore"), end="")
            res.append(str(line.decode('utf-8', errors="ignore")[:-1]))
            stdout.flush()
            if not line:
                break

        for line in iter(lambda: stderr.readline(2048), ""):
            if isPrint:
                print(line.decode('utf-8', errors="ignore"), end="")
            stderr.flush()
            if not line:
                break
        return res

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
            scp.put(files=origin, remote_path=target)
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

    '''
        nohup执行命令，默认没有输出，需要指定日志路径
        1. 默认日志路径是回收站，即不会保存日志文件
    '''

    def nohup_execute(self, cmd, log_path="/dev/null"):
        cmd = "bash -lc 'nohup %s > %s 2>&1 & '" % (cmd, log_path)
        return self.execute_cmd(cmd, isPrint=False)

    '''
        1. 运行jmeter
        2. jmx jmeter脚本 jmx脚本路径
        3. jtl_path jtl文件路径 , 报告文件
        4. jmeter_path jmeter路径 jmeter路径
    '''

    def run_jmeter(self, jmx, jtl_path, jmeter_path):
        cmd = "sh %s -n -t %s -l %s " % (jmeter_path, jmx, jtl_path)
        return self.nohup_execute(cmd)

    '''
        1. 部署jar包到服务器
        2. jar jar包路径， 会将本地jar包拷贝到服务器的dir路径
        3. port 端口号， 默认会停止port进程，谨慎使用
        4. dir 部署路径
    '''

    def deploy_jar_project(self, jar, port, dir="~"):
        self.copy_file(jar, dir)
        # 端口必须得要，不然没办法启动起来
        if port != None:
            self.execute_cmd("kill -9 %s" % self.find_pid_by_port(port))
        return self.nohup_execute("java -jar %s" % jar, dir=dir)
