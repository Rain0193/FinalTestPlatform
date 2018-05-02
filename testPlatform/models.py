from django.db import models

# Create your models here.
from basicData.models import StepsForCases


class TestCase(models.Model):
    case_name = models.CharField(max_length=30, verbose_name='用例名称')
    test_report = models.CharField(max_length=200, verbose_name='测试报告')
    test_result = models.NullBooleanField(default=None, verbose_name='上次测试结果')
    steps = models.ManyToManyField(StepsForCases, verbose_name=u'用例步骤')

    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.case_name



