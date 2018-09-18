# -*- coding: UTF-8 -*-
from sql.workflow import Workflow
from .models import users
from django.conf import settings

leftMenuBtnsCommon = (
    {'key': 'allworkflow', 'name': '全部历史工单', 'url': '/allworkflow/', 'class': 'glyphicon glyphicon-home',
     'display': True},
    {'key': 'submitsql', 'name': '正式SQL上线', 'url': '/submitsql/', 'class': 'glyphicon glyphicon-pencil',
     'display': True},
    {'key': 'sqlquery', 'name': 'SQL在线查询', 'url': '/sqlquery/', 'class': 'glyphicon glyphicon-search',
     'display': settings.QUERY},
    {'key': 'slowquery', 'name': 'SQL慢查日志', 'url': '/slowquery/', 'class': 'glyphicon glyphicon-align-right',
     'display': settings.SLOWQUERY},
    {'key': 'sqladvisor', 'name': 'SQL优化工具', 'url': '/sqladvisor/', 'class': 'glyphicon glyphicon-wrench',
     'display': settings.SQLADVISOR},
    {'key': 'queryapply', 'name': '查询权限管理', 'url': '/queryapplylist/', 'class': 'glyphicon glyphicon-eye-open',
     'display': settings.QUERY}
)

leftMenuBtnsSuper = (
    {'key': 'diagnosis', 'name': '主库会话管理', 'url': '/diagnosis_process/', 'class': 'glyphicon  glyphicon-scissors',
     'display': True},
    {'key': 'admin', 'name': '后台数据管理', 'url': '/admin/sql/', 'class': 'glyphicon glyphicon-list', 'display': True},
)

leftMenuBtnsDoc = (
    {'key': 'dbaprinciples', 'name': 'SQL审核必读', 'url': '/dbaprinciples/', 'class': 'glyphicon glyphicon-book',
     'display': True},
    {'key': 'charts', 'name': '统计图表展示', 'url': '/charts/', 'class': 'glyphicon glyphicon-file', 'display': True},
)


def global_info(request):
    """存放用户，会话信息等."""
    loginUser = request.session.get('login_username', None)
    if loginUser is not None:
        user = users.objects.get(username=loginUser)
        UserDisplay = user.display
        if UserDisplay == '':
            UserDisplay = loginUser
        if user.is_superuser:
            leftMenuBtns = leftMenuBtnsCommon + leftMenuBtnsSuper + leftMenuBtnsDoc
        else:
            leftMenuBtns = leftMenuBtnsCommon + leftMenuBtnsDoc
        # 获取代办数量
        try:
            todo = Workflow().auditlist(user, 0, 0, 1)['data']['auditlistCount']
        except Exception:
            todo = 0
    else:
        leftMenuBtns = ()
        UserDisplay = ''
        todo = 0

    return {
        'loginUser': loginUser,
        'leftMenuBtns': leftMenuBtns,
        'UserDisplay': UserDisplay,
        'todo': todo
    }
