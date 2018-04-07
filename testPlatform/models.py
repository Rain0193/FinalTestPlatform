from django.db import models

# Create your models here.


class TestCase(models.Model):
    case_id = models.CharField(max_length=10, default='0', verbose_name='用例id')
    case_name = models.CharField(max_length=30, verbose_name='用例名称')
    case_step = models.CharField(max_length=1000, verbose_name='用例步骤')
    has_automatic = models.BooleanField(default=False, verbose_name='是否自动化')
    test_report = models.CharField(max_length=200, verbose_name='测试报告')
    class_name = models.CharField(default='', max_length=50, verbose_name='所属测试类')
    test_method = models.CharField(default='', max_length=50, verbose_name='所属测试方法')
    test_file = models.CharField(default='', max_length=50, verbose_name='所属测试文件')
    test_result = models.NullBooleanField(default=None, verbose_name='上次测试结果')

    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name


