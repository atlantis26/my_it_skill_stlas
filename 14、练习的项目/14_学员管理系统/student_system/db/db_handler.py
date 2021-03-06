# -*- coding:utf-8 -*-
from db.orm import User, Role, Class, CourseRecord, Homework, UserM2MClass
from db import DBSession
from sqlalchemy import and_
from core.utils import SomethingError
from datetime import datetime


class DatabaseHandler(object):
    @staticmethod
    def create_user(name, account, password, qq, role_id):
        try:
            session = DBSession()
            user = User(name=name, account=account, password=password, qq=qq, role_id=int(role_id))
            session.add(user)
            session.commit()
            user = session.query(User).filter(User.account == account).first()
            session.close()
            return user
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_user_by_account(account, password=None):
        try:
            session = DBSession()
            if password:
                user = session.query(User).filter(and_(User.account == account, User.password == password)).first()
            else:
                user = session.query(User).filter(User.account == account).first()
            session.close()
            return user
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_user_by_qq(qq):
        try:
            session = DBSession()
            user = session.query(User).filter(User.qq == qq).first()
            session.close()
            return user
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_user_by_id(user_id):
        try:
            session = DBSession()
            user = session.query(User).filter(User.id == int(user_id)).first()
            session.close()
            return user
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_role_by_name(name):
        try:
            session = DBSession()
            role = session.query(Role).filter(Role.name == name).first()
            session.close()
            return role
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_role_by_id(role_id):
        try:
            session = DBSession()
            role = session.query(Role).filter(Role.id == int(role_id)).first()
            session.close()
            return role
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def delete_user_by_id(user_id):
        try:
            session = DBSession()
            session.query(User).filter(User.id == int(user_id)).delete()
            session.commit()
            session.close()
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def update_user(user_id, name, password, qq, role_id):
        try:
            session = DBSession()
            session.query(User).filter(User.id == int(user_id)).update({"name": name,
                                                                       "password": password,
                                                                        "qq": qq,
                                                                        "role_id": int(role_id)})
            session.commit()
            session.close()
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_user():
        try:
            session = DBSession()
            user_list = session.query(User).all()
            session.close()
            return [user.to_dict() for user in user_list]
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def create_class(name):
        try:
            session = DBSession()
            class1 = Class(name=name)
            session.add(class1)
            session.commit()
            class1 = session.query(Class).filter(Class.name == name).first()
            session.close()
            return class1
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def delete_class_by_id(class_id):
        try:
            session = DBSession()
            session.query(Class).filter(Class.id == int(class_id)).delete()
            session.commit()
            session.close()
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def update_class(class_id, name):
        try:
            session = DBSession()
            session.query(Class).filter(Class.id == int(class_id)).update({"name": name})
            session.commit()
            session.close()
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_class_by_name(name):
        try:
            session = DBSession()
            class1 = session.query(Class).filter(Class.name == name).first()
            session.close()
            return class1
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_class_by_id(class_id):
        try:
            session = DBSession()
            class1 = session.query(Class).filter(Class.id == int(class_id)).first()
            session.close()
            return class1
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_class():
        try:
            session = DBSession()
            class_list = session.query(Class).all()
            session.close()
            return [class1.to_dict() for class1 in class_list]
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def create_record(teacher_id, class_id, description):
        try:
            session = DBSession()
            date = datetime.now()
            record = CourseRecord(date=date, teacher_id=int(teacher_id), class_id=int(class_id), description=description)
            session.add(record)
            session.commit()
            record = session.query(CourseRecord).filter(and_(CourseRecord.description == description,
                                                             CourseRecord.class_id == class_id)).first()
            session.close()
            return record
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_record_by_id(record_id):
        try:
            session = DBSession()
            record = session.query(CourseRecord).filter(CourseRecord.id == int(record_id)).first()
            session.close()
            return record
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_record():
        try:
            session = DBSession()
            record_list = session.query(CourseRecord).all()
            session.close()
            return [record.to_dict() for record in record_list]
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def create_homework(record_id, student_id, score, homework_path):
        try:
            session = DBSession()
            homework = Homework(homework_path=homework_path, record_id=int(record_id), student_id=int(student_id), score=score)
            session.add(homework)
            session.commit()
            homework = session.query(Homework).filter(and_(Homework.record_id == int(record_id),
                                                           Homework.student_id == int(student_id))).first()
            session.close()
            return homework
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def update_homework_path(homework_id, homework_path):
        try:
            session = DBSession()
            session.query(Homework).filter(Homework.id == int(homework_id)).update(
                {"homework_path": homework_path})
            session.commit()
            session.close()
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def update_homework_score(homework_id, score):
        try:
            session = DBSession()
            session.query(Homework).filter(Homework.id == int(homework_id)).update({"score": score})
            session.commit()
            session.close()
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_homework_by_student_id(student_id):
        try:
            session = DBSession()
            homework_list = session.query(Homework).filter(Homework.student_id == int(student_id)).all()
            session.close()
            return [homework.to_dict() for homework in homework_list]
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_homework_by_record_id(record_id):
        try:
            session = DBSession()
            homework_list = session.query(Homework).filter(Homework.record_id == int(record_id)).all()
            session.close()
            return [homework.to_dict() for homework in homework_list]
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_students_by_class_id(class_id):
        try:
            session = DBSession()
            lst = session.query(UserM2MClass).filter(UserM2MClass.class_id == int(class_id)).all()
            student_list = [st.user_id for st in lst]
            session.close()
            return student_list
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_homework(student_id, record_id):
        try:
            session = DBSession()
            homework = session.query(Homework).filter(and_(Homework.student_id == int(student_id),
                                                           Homework.record_id == int(record_id))).first()
            session.close()
            return homework
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_homework_by_id(homework_id):
        try:
            session = DBSession()
            homework = session.query(Homework).filter(Homework.id == int(homework_id)).first()
            session.close()
            return homework
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_homework():
        try:
            session = DBSession()
            homework_list = session.query(Homework).filter(Homework.score != None).all()
            session.close()
            return homework_list
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_class_by_student_id(student_id):
        try:
            session = DBSession()
            lst = session.query(UserM2MClass).filter(UserM2MClass.user_id == int(student_id)).all()
            class_list = [cla.to_dict() for cla in lst]
            session.close()
            return class_list
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))

    @staticmethod
    def create_mapping_class_user(class_id, user_id):
        try:
            session = DBSession()
            mapping1 = UserM2MClass(class_id=int(class_id), user_id=int(user_id))
            session.add(mapping1)
            session.commit()
            session.close()
        except Exception as e:
            raise SomethingError(u"操作数据库时时出错，详情：{0}".format(str(e)))
