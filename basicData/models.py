from django.db import models

# Create your models here.


class Element(models.Model):
    SHIRT_SIZES = (
        ('id', 'id'),
        ('xpath', 'xpath'),
        ('link', 'link'),
    )
    element_name = models.CharField(max_length=30, verbose_name='元素名称')
    access_method = models.CharField(max_length=10, choices=SHIRT_SIZES, verbose_name='获取方式')
    access_path = models.CharField(default='None', max_length=100, verbose_name='获取值')
    frame_name = models.CharField(default='default', max_length=30, verbose_name='所在frame')

    class Meta:
        verbose_name = '元素'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.element_name


class Steps(models.Model):
    Actions = (
        ('点击', '点击'),
        ('填写', '填写'),
        ('切换', '切换'),
        ('选择', '选择'),
        ('上传', '上传'),
        ('检查', '检查'),
    )
    step_des = models.CharField(max_length=100, default='', verbose_name='步骤描述')
    element_name = models.ForeignKey(Element, null=True, blank=True, verbose_name='元素名称')
    actions = models.CharField(max_length=2, choices=Actions, verbose_name='执行动作')
    parameter = models.CharField(max_length=100, null=True, blank=True,  default='', verbose_name='参数')
    wait_time = models.IntegerField(default=1, verbose_name='执行完等待时间')

    class Meta:
        verbose_name = '步骤'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.step_des


class StepsForCases(models.Model):
    case_name = models.CharField(max_length=50, verbose_name='用例名称')
    step_name = models.ForeignKey(Steps, verbose_name='步骤描述')
    execution_order = models.IntegerField(verbose_name='执行顺序', unique=True)

    class Meta:
        verbose_name = '用例步骤配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.case_name

