# Inputs
LOGIN_SERVER = u'输入您要进入的服务器地址 > '
LOGIN_USERNAME = u'输入您的用户名 > '
MENU_SELECT = u'选择您的操作（编号） > '
INVITE = u'输入您要邀请的玩家ID > '
ACTION = u'请输入{ACTION}行动的值 > '

# Outputs Normal
WAIT = u'等待中……'
GAME_START = u'您与 {name} 的对局已经创建，游戏即将开始！'
MENU = u'''----------------欢迎来到Pointa！您的ID是{key}----------------
    当前服务器在线人数 {num} 名
    ---- [0] 邀请玩家
    ---- [1] 等待邀请
    ---- [2] 开始匹配
    ---- [3] 退出游戏
'''
ROUND_BEGIN = u'\n----------------第{num}回合开始----------------'
ROLLED = u'{name}掷出了{num}点！'
ATK_JUDGE = u'{name}进行攻击判定，掷出了{num}点！造成{dmg}点伤害！'
STATUS = u'''\n---- {name} 的当前状态 ----
    - HP: {HP}
    - DEF: {DEF}
    - PT: {PT}
'''
PLAYER_KILLED = u'{name} 死亡……'
GAME_END = u'游戏结束！{lose}失败！'
GAME_END_EQUAL = u'游戏结束！平局！'
ACTIONS_HEAD = u'\n-------第{num}回合行动总结-------'

ACTION_ATK = '{name} 使用了{num}点攻击，判定为{judge}点'
ACTION_DEF = '{name} 使用了{num}点防御'
ACTION_HEL = '{name} 使用了{num}点治疗'

PHASE_2 = '您有25秒的时间完成本回合行动！'

# Outputs Errors
TIMEOUT_BAD = u'您的操作超时或输入有误！'
REQUEST_ERROR = u'向服务器请求失败……错误码为{code}'
QUIT = u'输入Ctrl+C退出……'
BAD_INPUT = u'错误的输入！'
INVITE_404 = u'未找到该玩家'