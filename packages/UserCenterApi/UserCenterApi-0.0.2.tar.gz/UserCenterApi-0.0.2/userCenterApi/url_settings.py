"""
此模块包含嘞用户中心的全局配置
"""


ROOT_ROUTER = "/api/v1"


#获取授权code
AUTHORIZATION_CODE = ROOT_ROUTER + "/authior/code"

#签发token
AUTHORIZATION_TOKEN = ROOT_ROUTER + "/authior/token"

#刷新token
REFRESH_TOKEN = ROOT_ROUTER + "/authior/refresh"

#验证token
VERIFY_TOKEN = ROOT_ROUTER + "/authior/verify/token"

#申请应用
APPLY_CLIENTID = ROOT_ROUTER + "/authior/app"

#获取二维码地址
QR_CODE_ADDRESS = ROOT_ROUTER + "/dingding/qrcode"

#扫码获取授权code
QR_AUTHORIZATION_CODE = ROOT_ROUTER + "/dingding"

#绑定应用
QR_BINGDING = ROOT_ROUTER + "/dingding/bingding"

"*******************************"

#注册普通用户
REGISTER_USER = ROOT_ROUTER + "/users/register"

#新增用户
ADD_USER = ROOT_ROUTER + "/users/newuser"

#个人详情
OWN_USER_DETAIL = ROOT_ROUTER + "/users/own"

#用户详情
DETAIL_USER = ROOT_ROUTER + "/users/{}"

#获取用户列表
LIST_USER = ROOT_ROUTER + "/users/list"

#重置密码
RESET_PWD = ROOT_ROUTER + "/{}/pwd/reset"

#修改密码
SET_PWD = ROOT_ROUTER + "/{}/pwd/set"

#修改个人资料

UPDATE_USER = ROOT_ROUTER + "/users/{}"

#使用其他软件登录者修改用户账号
UPDATE_PHONENUMBER = ROOT_ROUTER + "/users/ticket/update/{}"









