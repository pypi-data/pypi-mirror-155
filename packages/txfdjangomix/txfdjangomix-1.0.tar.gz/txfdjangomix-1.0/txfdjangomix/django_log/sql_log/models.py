from django.db import models

# Create your models here.


class DjangoLog(models.Model):
    """接口日志"""
    user_id = models.CharField(verbose_name='用户id', null=True, blank=True)
    tb_api = models.CharField(verbose_name='接口')
    tb_method = models.CharField(verbose_name='请求方法')
    tb_header = models.CharField(verbose_name='请求头', null=True, blank=True)
    platform = models.CharField(verbose_name='操作系统', null=True, blank=True)
    url_params = models.TextField(verbose_name='url参数', null=True, blank=True)
    body_params = models.TextField(verbose_name='body参数', null=True, blank=True)
    error_type = models.CharField(verbose_name='日志级别')
    error_info = models.TextField(verbose_name='日志详情', null=True, blank=True)
    tb_date = models.DateTimeField(verbose_name='日期', auto_now_add=True)

    class Meta:
        db_table = 'django_log'
