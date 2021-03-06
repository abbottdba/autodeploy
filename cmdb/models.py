from django.db import models
from user_center import models as user_center_models


class BusinessUnit(models.Model):
    """
    业务线
    """
    parent_unit = models.ForeignKey('self', related_name='parent_level', blank=True, null=True)
    name = models.CharField('业务线', max_length=64)
    contact = models.ManyToManyField(user_center_models.UserGroup, verbose_name='业务联系人', related_name='c', blank=True)
    manager = models.ManyToManyField(user_center_models.UserGroup, verbose_name='系统管理员', related_name='m', blank=True)
    memo = models.CharField('备注', max_length=64, blank=True, null=True)
    order_num = models.SmallIntegerField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "业务线表"

    def __str__(self):
        return self.name


class IDC(models.Model):
    """
    机房信息
    """
    name = models.CharField('机房', max_length=32)
    floor = models.IntegerField('楼层', default=1)
    phone = models.CharField(u'联系电话', max_length=32, blank=True, null=True)
    idc_address = models.CharField(u'地址', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name_plural = "机房表"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    资产标签
    """
    name = models.CharField('标签', max_length=32, unique=True)
    order_id = models.SmallIntegerField('排序ID', default=0)

    class Meta:
        verbose_name_plural = "标签表"

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
    """
    device_type_choices = (
        (1, 'Server'),
        (2, 'Docker'),
        (3, 'CloudServer'),
        (4, 'XenServer'),
        (5, 'OpenvzServer'),
        (6, 'PublicIP'),
    )
    device_status_choices = (
        (1, 'Active'),
        (2, 'Free'),
        (3, 'Delete'),
    )
    device_type_id = models.IntegerField(choices=device_type_choices, default=1)
    device_status_id = models.IntegerField(choices=device_status_choices, default=1)
    asset_num = models.CharField(verbose_name='资产编号', max_length=20, unique=True)
    sn = models.CharField('SN号', max_length=64, unique=True)
    idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True, on_delete=models.SET_NULL)
    manage_ip = models.GenericIPAddressField('管理IP', null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='归属业务线', null=True, blank=True,
                                      on_delete=models.SET_NULL)
    raid_type_choices = (
        ('RAID 1', 'RAID 1'),
        ('RAID 5', 'RAID 5'),
        ('RAID 01', 'RAID 01'),
        ('RAID 10', 'RAID 10'),
        ('RAID 1 & 5', 'RAID 1 & 5'),
        ('RAID 1 & 10', 'RAID 1 & 10'),
    )
    raid_type = models.CharField(choices=raid_type_choices, max_length=20, default='RAID 10')
    tag = models.ManyToManyField('Tag')
    memo = models.CharField(verbose_name='备注', max_length=200, null=True, blank=True)
    power_cable = models.SmallIntegerField('电源数量', null=True, blank=True, default=2)
    rack = models.SmallIntegerField('机柜编号', null=True, blank=True, default=1)
    purchasing = models.DateField(u'采购时间', auto_now_add=True)
    creator = models.ForeignKey(user_center_models.UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    latest_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "资产表"

    def __unicode__(self):
        return self.server.ipaddress

    #__str__ = __unicode__

    #
    # def __str__(self):
    #     return self.id



class Server(models.Model):
    """
    服务器信息
    """
    asset = models.OneToOneField('Asset', related_name='server')
    hostname = models.CharField(max_length=128, null=True, blank=True)
    manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    model = models.CharField('型号', max_length=64, null=True, blank=True)
    ipaddress = models.GenericIPAddressField('IP地址', unique=True)
    configuration = models.CharField(u'硬件配置', max_length=100, blank=True, null=True)
    Memory = models.IntegerField(u'内存配置', blank=True, null=True)
    DeviceSize = models.IntegerField(u'硬盘配置', blank=True, null=True)
    CpuUsage = models.IntegerField(u'CPU使用率', blank=True, null=True)
    MemUsage = models.IntegerField(u'内存使用率', blank=True, null=True)
    DiskUsage = models.IntegerField(u'磁盘使用率', blank=True, null=True)
    LoadInfo = models.FloatField(u'系统负载', blank=True, null=True)
    os_type = models.CharField('系统', max_length=16, null=True, blank=True)
    os_release = models.CharField('系统版本', max_length=200, null=True, blank=True)
    cpu_count = models.IntegerField('CPU物理个数', null=True, blank=True)
    cpu_core_count = models.IntegerField('CPU核数', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "服务器表"

    # def __str__(self):
    #     return self.ipaddress


class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插槽位', max_length=64)
    manufactory = models.CharField(u'制造商', max_length=64, blank=True, null=True)
    model = models.CharField(u'磁盘型号', max_length=128, blank=True, null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )
    iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choice, default='SAS')
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("asset", "slot")
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"

    def __unicode__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id, self.slot, self.capacity)

    auto_create_fields = ['sn', 'slot', 'manufactory', 'model', 'capacity', 'iface_type']


class RAM(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    model = models.CharField(u'内存型号', max_length=128)
    slot = models.CharField(u'插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(MB)')
    memo = models.CharField(u'备注',max_length=128, blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"
        unique_together = ("asset", "slot")

    def __unicode__(self):
        return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)

    auto_create_fields = ['sn', 'slot', 'model', 'capacity']


class NewAssetApprovalZone(models.Model):
    ipaddress = models.GenericIPAddressField(u'IP', blank=True, null=True)
    sn = models.CharField(u'资产SN号',max_length=128, unique=True)
    hostname = models.CharField(max_length=200, null=True, blank=True)
    manufactory = models.CharField(max_length=64,blank=True,null=True)
    model = models.CharField(max_length=128,blank=True,null=True)
    asset_resume_num = models.CharField(max_length=128, blank=True, null=True)
    ram_size = models.IntegerField(blank=True,null=True)
    cpu_model = models.CharField(max_length=128,blank=True,null=True)
    cpu_count = models.IntegerField(blank=True,null=True)
    cpu_core_count = models.IntegerField(blank=True,null=True)
    os_type =  models.CharField(max_length=64,blank=True,null=True)
    os_release =  models.CharField(max_length=64,blank=True,null=True)
    client_version = models.CharField(max_length=10, null=True, blank=True)
    data = models.TextField(u'资产数据')
    date = models.DateTimeField(u'汇报日期',auto_now_add=True)
    approved = models.BooleanField(u'已批准',default=False)
    approved_by = models.CharField(max_length=64,blank=True,null=True)
    approved_date = models.DateTimeField(u'批准日期',blank=True,null=True)

    def __str__(self):
        return self.sn
    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"


class AssetRecord(models.Model):
    """
    资产变更记录,creator为空时，表示是资产汇报的数据。
    """
    asset_obj = models.ForeignKey('Asset', related_name='ar', blank=True, null=True)
    event_type_choice = (
        (1, 'Asset Create'),
        (2, 'Asset Update'),
        (3, 'Asset Delete'),
        (4, 'Asset Apply'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choice, default=2)
    content = models.TextField(null=True)
    creator = models.ForeignKey(user_center_models.UserProfile, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产记录表"

    def __str__(self):
        return str(self.id)


class ErrorLog(models.Model):
    """
    错误日志,如：agent采集数据错误 或 运行错误
    """
    asset_obj = models.ForeignKey('Asset', null=True, blank=True)
    title = models.CharField(max_length=16)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "错误日志表"

    def __str__(self):
        return self.title


class DockerInstance(models.Model):
    asset = models.ForeignKey('Asset', related_name='docker')
    obj_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    cpu = models.SmallIntegerField(blank=True, null=True)
    mem = models.SmallIntegerField(blank=True, null=True)
    disk = models.SmallIntegerField(blank=True, null=True)
    cpu_usage = models.FloatField(blank=True, null=True)
    mem_usage = models.FloatField(blank=True, null=True)
    disk_usage = models.FloatField(blank=True, null=True)
    port = models.CharField(max_length=100, blank=True, null=True)
    port_map = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Docker实例'
        verbose_name_plural = "Docker实例"

    def __str__(self):
        return self.obj_id


# 云主机申请详情表
class ServerApplyDetail(models.Model):
    ipaddress = models.GenericIPAddressField(u'IP地址', blank=True, null=True)
    idc = models.CharField(max_length=100)
    sys_type = models.CharField(u'系统类型', max_length=100)
    function = models.CharField(u'功能分类', max_length=100)
    cpu = models.SmallIntegerField()
    mem = models.SmallIntegerField()
    disk = models.SmallIntegerField()
    memo = models.CharField(u'备注', max_length=100)
    user_apply = models.CharField(u'申请用户', max_length=100, blank=True, null=True)
    user_approve = models.CharField(u'审批用户', max_length=100, blank=True, null=True)
    date_apply = models.DateTimeField(auto_now_add=True)
    date_approve = models.DateTimeField(u'批准日期',blank=True,null=True)
    approved_status_choices = (
        (1, 'Pending'),
        (2, 'Standby'),
        (3, 'Created'),
        (4, 'False'),
    )
    approved = models.SmallIntegerField(choices=approved_status_choices, default=1)


# 任务表
class ServerApplyOrder(models.Model):
    """
    资产申请任务表
    """
    name = models.CharField(max_length=64)
    order_type_choices = (
        (1, 'CloudServer Apply'),
    )
    order_type = models.SmallIntegerField(choices=order_type_choices, default=1)
    business = models.CharField(u'业务线', max_length=100)
    project = models.ManyToManyField(ServerApplyDetail, related_name='server_apply_order')
    user_apply = models.CharField(u'申请用户', max_length=100, blank=True, null=True)
    user_approve = models.CharField(u'审批用户', max_length=100, blank=True, null=True)
    date_apply = models.DateTimeField(auto_now_add=True)
    date_approve = models.DateTimeField(u'批准日期', blank=True, null=True)
    approved = models.BooleanField(u'已审核', default=False)


    class Meta:
        verbose_name_plural = "资产申请任务表"

    def __str__(self):
        return self.name
