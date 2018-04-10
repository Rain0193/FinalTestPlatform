from django.db import models

# Create your models here.


class Element(models.Model):
    SHIRT_SIZES = (
        ('1', 'id'),
        ('2', 'xpath'),
    )
    element_name = models.CharField(max_length=30, verbose_name='元素名称')
    access_method = models.CharField(max_length=1, choices=SHIRT_SIZES, verbose_name='获取方式')
    access_path = models.CharField(max_length=100, verbose_name='获取值')
    frame_name = models.CharField(default='default', max_length=30, verbose_name='所在frame')

    class Meta:
        verbose_name = '元素管理'
        verbose_name_plural = verbose_name


