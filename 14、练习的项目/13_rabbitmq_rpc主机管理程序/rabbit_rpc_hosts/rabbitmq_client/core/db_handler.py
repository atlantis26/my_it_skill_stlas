# coding:utf-8
from core.orm import Task
from conf.settings import DB_Task
import json
import os


def save_task(task_id, queue, data):
    task = Task(task_id, queue, data)
    json_data = json.dumps(task.__dict__)
    file_path = os.path.join(DB_Task, task_id)
    with open(file_path, "w") as f:
        f.write(json_data)


def load_task(task_id):
    file_path = os.path.join(DB_Task, task_id)
    with open(file_path, "r") as f:
        return json.loads(f.read())
