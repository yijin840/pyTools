from local_ssh import ssh_client

server = {
    # 自定义名称，可有可无，比如说，服务器1
    "name": "server",
    # 服务器地址 ，例如 127.0.0.1
    "host": "118.31.251.1",
    # 服务器端口， 例如 22
    "port": "22",
    # 用户名， 例如 root
    "user": "root",
    # 服务器密码， 例如 123456
    "password": "Wang@Yijin840_Server"
}

if __name__ == "__main__":
    ssh = ssh_client(server['host'], server['port'], server['user'],
                    server['password'], server['name'])
    # ssh.execute_cmd("ls")
    print(ssh.find_java_path())