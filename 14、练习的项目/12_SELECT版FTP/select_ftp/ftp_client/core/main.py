# coding=utf-8
from core.client_handler import FtpClient


class FtpPortal(object):
    def __init__(self, host, ip):
        self.client = FtpClient(host, ip)

    def register(self):
        """注册用户"""
        username = input(u"请输入注册用户名：").strip()
        password1 = input(u"请输入设置密码：").strip()
        password2 = input(u"请重复输入设置的密码：").strip()
        print(u"新用户系统默认存储配额为50G")
        return self.client.register(username, password1, password2, quota=50)

    def login(self):
        """用户登录"""
        username = input(u"请输入用户名：").strip()
        password = input(u"请输入密码：").strip()
        return self.client.login(username, password)

    def _client_shell(self, username):
        """登录用户后进入客户端shell"""
        while True:
            try:
                cmd_args = input(u"${0}>: ".format(username)).strip()
                if cmd_args == "exit":
                    break
                cmd_args = [s.strip() for s in cmd_args.split(" ")]
                rsp = self.client.run_cmd(cmd_args[0], *cmd_args[1:])
                print(rsp.msg + "\n" + "-" * 40)
            except (KeyboardInterrupt, EOFError) as e:
                msg = u"\n当前客户端shell连接被终止。{0}".format(str(e))
                print(msg)
                self.client.restart()
                break

    def console(self):
        home_page = """
        --------------------欢迎访问无忧FTP云盘系统---------------------
        请选择输入操作编号进行操作：
        <\033[36;1m1\033[0m>.用户注册                      <\033[36;1m2\033[0m>.用户登录
        """
        while True:
            print(home_page)
            action = input(u"请输入您选择的操作编号：").strip()
            if action == "1":
                rsp = self.register()
                print(rsp.msg)
            elif action == "2":
                rsp = self.login()
                print(rsp.msg)
                if rsp.code == 200:
                    username = rsp.data["username"]
                    self._client_shell(username)
            else:
                print(u"输入的操作项编号{0}不存在，请核对后再试".format(action))

