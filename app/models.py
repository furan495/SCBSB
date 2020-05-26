from django.db import models

# Create your models here.


class Event(models.Model):
    time = models.DateTimeField(
        auto_now_add=True, verbose_name='事件时间')
    title = models.CharField(max_length=200, verbose_name='事件描述')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '事件'


class BomAna(models.Model):
    time = models.DateTimeField(
        auto_now_add=True, verbose_name='操作时间')
    operator = models.CharField(max_length=200, verbose_name='操作人')
    target = models.CharField(max_length=200, verbose_name='操作对象')
    result = models.CharField(max_length=200, verbose_name='操作结果')

    def __str__(self):
        return self.operator+self.target+self.result

    class Meta:
        verbose_name = 'BOM统计'


class Department(models.Model):
    name = models.CharField(max_length=10, verbose_name='部门')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'


PROJECT_STATUS = (
    ('1', '进行中'),
    ('2', '已完成'),
)


class Project(models.Model):
    name = models.CharField(
        max_length=50, verbose_name='项目名称', blank=True, null=True)
    status = models.CharField(choices=PROJECT_STATUS,
                              default='1', max_length=10, verbose_name='项目状态')
    owner = models.CharField(
        max_length=20, verbose_name='项目甲方', blank=True, null=True)
    startTime = models.DateTimeField(
        verbose_name='开始时间')
    endTime = models.DateTimeField(
        verbose_name='结束时间', auto_now=True)
    number = models.CharField(
        max_length=20, verbose_name='项目编号', blank=True, null=True)

    def __str__(self):
        return self.name+self.owner

    class Meta:
        verbose_name = '项目'


class Section(models.Model):
    project = models.ForeignKey(
        Project, related_name='sections', on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=20, verbose_name='节点名称')
    time = models.DateTimeField(verbose_name='节点时间')
    description = models.CharField(max_length=200, verbose_name='节点描述')

    def __str__(self):
        return '%s/%s/%s' % (self.name, str(self.time), self.description)

    class Meta:
        verbose_name = '节点'


class Progress(models.Model):
    project = models.ForeignKey(
        Project, related_name='progresses', on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=20, verbose_name='进度名称')
    time = models.DateTimeField(verbose_name='进度时间')
    description = models.CharField(max_length=200, verbose_name='进度描述')
    creator = models.CharField(max_length=20, verbose_name='创建人')

    def __str__(self):
        return '%s/%s/%s/%s' % (self.name, str(self.time), self.description, self.creator)

    class Meta:
        verbose_name = '进度'


class Role(models.Model):
    name = models.CharField(max_length=10, verbose_name='角色名')
    authority = models.CharField(max_length=200, verbose_name='权限')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色'


USER_GENDER = (
    ('1', '男'),
    ('2', '女'),
)


class User(models.Model):
    department = models.ForeignKey(
        Department, related_name='members', on_delete=models.CASCADE, verbose_name='部门')
    projects = models.ManyToManyField(
        Project, related_name='persons', verbose_name='参与项目', blank=True, null=True)
    role = models.ForeignKey(Role, related_name='role',
                             on_delete=models.CASCADE, verbose_name='角色')
    name = models.CharField(max_length=10, verbose_name='姓名')
    password = models.CharField(max_length=20, verbose_name='密码')
    phone = models.CharField(max_length=20, verbose_name='电话')
    gender = models.CharField(
        choices=USER_GENDER, max_length=10, verbose_name='性别')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用户'


PROBLEM_STATUS = (
    ('1', '待解决'),
    ('2', '处理中'),
    ('3', '已解决'),
)


class Problem(models.Model):
    theme = models.CharField(max_length=100, verbose_name='主题')
    number = models.CharField(
        max_length=20, verbose_name='问题编号', blank=True, null=True)
    promoter = models.CharField(max_length=10, verbose_name='发起人')
    receiver = models.CharField(max_length=10, verbose_name='接收人')
    carbonCopy = models.CharField(
        max_length=200, verbose_name='抄送人', blank=True, null=True)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expectTime = models.DateTimeField(verbose_name='期望回复时间')
    endTime = models.DateTimeField(
        verbose_name='结束时间', auto_now=True, blank=True, null=True)
    status = models.CharField(choices=PROBLEM_STATUS,
                              default='1', max_length=10, verbose_name='问题状态')
    description = models.CharField(max_length=200, verbose_name='问题描述')
    appendix = models.CharField(max_length=500, verbose_name='附件')
    promAdvice = models.CharField(
        max_length=200, verbose_name='发起人意见', blank=True, null=True)
    receAdvice = models.CharField(
        max_length=200, verbose_name='接收人意见', blank=True, null=True)
    updateCount = models.IntegerField(verbose_name='修改次数', default=0)
    read = models.CharField(max_length=20, default='未读', verbose_name='回复状态')

    def __str__(self):
        return self.number+self.promoter

    class Meta:
        verbose_name = '问题'
