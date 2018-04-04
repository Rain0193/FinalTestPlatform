from django.db import models

# Create your models here.


class TestCase(models.Model):
    case_id = models.IntegerField(default=0, verbose_name='用例id')
    case_name = models.CharField(max_length=30, verbose_name='用例名称')
    case_step = models.CharField(max_length=1000, verbose_name='用例步骤')

    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name


