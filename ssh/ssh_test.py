from local_ssh import ssh_client

server = {
    # 自定义名称，可有可无，比如说，服务器1
    "name": "name",
    # 服务器地址 ，例如 127.0.0.1
    "host": "host",
    # 服务器端口， 例如 22
    "port": "port",
    # 用户名， 例如 root
    "user": "user",
    # 服务器密码， 例如 123456
    "password": "password"
}

if __name__ == "__main__":
    ssh = ssh_client(server['host'], server['port'], server['user'],
                    server['password'], server['name'])
    ssh.execute_cmd("ls")