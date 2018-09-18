# -*- coding: UTF-8 -*- 
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Register your models here.
from archer import settings
from .models import users, master_config, slave_config, workflow, WorkflowAudit, WorkflowAuditSetting, \
    DataMaskingColumns, DataMaskingRules, AliyunAccessKey, AliyunRdsConfig


# 主库配置管理
@admin.register(master_config)
class master_configAdmin(admin.ModelAdmin):
    list_display = ('id', 'cluster_name', 'master_host', 'master_port', 'master_user', 'create_time')
    search_fields = ['id', 'cluster_name', 'master_host', 'master_port', 'master_user', 'master_password',
                     'create_time', 'update_time']


# SQL工单管理
@admin.register(workflow)
class workflowAdmin(admin.ModelAdmin):
    list_display = ('id', 'workflow_name', 'cluster_name', 'engineer', 'create_time', 'status', 'is_backup')
    search_fields = ['id', 'workflow_name', 'engineer', 'review_man', 'sql_content']
    exclude = ('is_manual',)

@admin.register(users)
class usersAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('id', 'username', 'display', 'role', 'email', 'is_superuser', 'is_staff', 'is_active')
        self.search_fields = ('id', 'username', 'display', 'role', 'email')
        # 以上的属性都可以在django源码的UserAdmin类中找到，我们做以覆盖

    def changelist_view(self, request, extra_context=None):
        # 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，我们要重新定义它，以达到不同权限的用户，返回的表单内容不同
        if request.user.is_superuser:
            # 此字段定义UserChangeForm表单中的具体显示内容，并可以分类显示
            self.fieldsets = (
                (('认证信息'), {'fields': ('username', 'password')}),
                (('个人信息'), {'fields': ('display', 'role', 'email')}),
                (('权限信息'), {'fields': ('is_active', 'is_staff')}),
                # (('Important dates'), {'fields': ('last_login', 'date_joined')}),
            )
            # 此字段定义UserCreationForm表单中的具体显示内容
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': ('username', 'display', 'role', 'email', 'password1', 'password2'),
                                          }),
                                  )
        return super(UserAdmin, self).changelist_view(request, extra_context)


if settings.QUERY:
    # 查询从库配置
    @admin.register(slave_config)
    class WorkflowAuditAdmin(admin.ModelAdmin):
        list_display = (
            'id', 'cluster_name', 'slave_host', 'slave_port', 'slave_user', 'create_time', 'update_time')
        search_fields = ['id', 'cluster_name', 'slave_host', 'slave_port', 'slave_user', 'slave_password', ]


    # 工作流审核配置
    @admin.register(WorkflowAuditSetting)
    class WorkflowAuditSettingAdmin(admin.ModelAdmin):
        list_display = ('audit_setting_id', 'workflow_type', 'audit_users',)

if settings.DATA_MASKING_ON_OFF:
    # 脱敏字段页面定义
    @admin.register(DataMaskingColumns)
    class DataMaskingColumnsAdmin(admin.ModelAdmin):
        list_display = (
            'column_id', 'rule_type', 'active', 'cluster_name', 'table_schema', 'table_name', 'column_name',
            'create_time',)
        search_fields = ['cluster_name', 'table_schema', 'table_name', 'column_name']


    # 脱敏规则页面定义
    @admin.register(DataMaskingRules)
    class DataMaskingRulesAdmin(admin.ModelAdmin):
        list_display = (
            'rule_type', 'rule_regex', 'hide_group', 'rule_desc', 'sys_time',)

if settings.ALIYUN_RDS_MANAGE:
    # 阿里云的认证信息
    @admin.register(AliyunAccessKey)
    class AliyunAccessKeyAdmin(admin.ModelAdmin):
        list_display = ('ak', 'secret', 'is_enable', 'remark',)


    # 阿里云集群配置信息
    @admin.register(AliyunRdsConfig)
    class AliyunRdsConfigAdmin(admin.ModelAdmin):
        list_display = ('cluster_name', 'rds_dbinstanceid',)
