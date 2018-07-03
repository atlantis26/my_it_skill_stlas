# coding:utf-8
import logging

logger = logging.getLogger("system.student_view")


class StudentView(object):
    """学员视图"""
    def __init__(self, username):
        self.username = username

    def console(self):
        """ 学员视图主页"""
        while True:
            msg = u"""-------------------------------------------------
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.提交作业                   <\033[36;1m2\033[0m>.查询分数
                    <\033[36;1m3\033[0m>.查看成绩排名               <\033[36;1m4\033[0m>.退出视图
            """
            print(msg)
            actions = {"1": self.commit_homework,
                       "2": self.query_score,
                       "3": self.query_rank,
                       "4": self.logout}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num not in actions:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue
            actions[num]()

    def commit_homework(self, student_id, record_id, file_path):
        pass

    def query_score(self):
        pass

    def query_rank(self):
        pass

    def logout(self):
        pass
