# -*- coding:utf-8 -*-
from rest_framework.response import Response
from models import DjangoLog


class DjangoLogSql(object):
    """支持自定义
    1 insert_sql_log 方法写数据库的时候需要的数据
    2 将1构造好的数据写入sql_obj=DjangoLog这个表
    """

    def get_request_info(self, request, method, error_type='info', error_info=None):
        """获取请求用户的基本信息"""
        user = request.user

        if user:
            user_id = user.user_id
        else:
            user_id = None
        return {
            'method': method,
            'user_id': user_id,
            'path': request.path,
            'url_params': request.query_params,
            'body_params': request.body,
            'error_type': error_type,
            'error_info': error_info,
        }

    def save_django_sql(self, request, sql_obj, method, error_type='info', error_info=None):
        """将构造好的 用户请求的数据写入到django_log表"""
        sql_info = self.get_request_info(request=request, method=method, error_type=error_type, error_info=error_info)
        if sql_obj.objects.create(**sql_info):
            return True
        else:
            print('日志写入错误')


def insert_sql_log(insert=True, sql_obj=DjangoLog, cls_obj=DjangoLogSql):
    """此方法 可以将我们设定好的日志写入到django_log表
    sql_obj 指定表
    insert 为true就是表示写入否则就是不写入到django_log表
    """
    def outer(f):
        def inner(*args, **kwargs):
            request = args[1]
            method = request.method
            try:
                # args的第一个参数为class对象 args[1]为request
                ret = f(*args, **kwargs)
                if insert:
                    cls_obj().save_django_sql(request, sql_obj, method, error_type='info', error_info=None)
                return ret
            except Exception as e:
                if insert:
                    cls_obj().save_django_sql(request, sql_obj, method, error_type='error', error_info=e)
                    print(e)
                return Response({'{}请求错误'.format(method): '错了'})
        return inner
    return outer

