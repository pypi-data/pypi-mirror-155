# -*- coding: utf-8 -*-
import json
import requests
from .url_settings import *
from .base import Map, ExceptionError

__all__ = ("MyError", "UserCenterApi", "RequestHandler")

class MyError(ExceptionError):

    def __init__(self, *err):
        super(MyError, self).__init__(*err)


class RequestHandler:
    def __init__(self):
        self.session = requests.session()

    def request(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        try:
            return self.session.request(method, url, params=params, data=data, json=json, headers=headers, **kwargs)
        except:
            pass
        finally:
            self.close_session()

    def close_session(self):
        """关闭session"""
        self.session.close()


class UserCenterApi(object):

    def __init__(self, center_url):
        self.root_url = center_url
        self.requestHandler = RequestHandler()

    def _req(self, method, url, params=None, data=None, json_data=None, headers=None, **kwargs):
        resp = self.requestHandler.request(method, url, params=params, data=data, json=json_data, headers=headers, **kwargs)
        data = None
        if resp.json():
            data = Map(json.loads(resp.content.decode("utf-8")))
            if data.errcode:
                msg = "%(errcode)d %(errmsg)s" % data
                raise MyError(msg)
        return data

    def authorization_code(self, clientId, user, pwd):
        """
        通过账号密码获取用户中授权
        :param clientId: 应用id
        :param user: 手机账号
        :param pwd: 加密密码
        :return: 授权code
        """
        url = self.root_url + AUTHORIZATION_CODE
        params = dict()
        params.setdefault("response_type", "code")
        params.setdefault("client_id", clientId)
        params.setdefault("user", user)
        params.setdefault("pwd", pwd)
        return self._req(method="get", url=url, params=params)

    def authorization_token(self, grant_type, clientId, clientSecret, **kwargs):
        """
        签发用户中心token
        :param grant_type: oauth2.0 类型
            "client_credential"     凭证式
            "authorization_code"    授权码式
            "password"              密码式
            "token"                 隐藏式
        :param client_id: 应用id
        :param clientSecret: 应用密钥
        :param kwargs: 根据不同oauth类型传不同参数
            凭证式: grant_type, client_id, clientSecret
            授权码式: grant_type, client_id, clientSecret, code
            密码式: grant_type, client_id, clientSecret, user, pwd
            隐藏式: grant_type, client_id, clientSecret, redirect_uri
        :return:
        """
        url = self.root_url + AUTHORIZATION_TOKEN
        params = dict()
        params.setdefault("grant_type", grant_type)
        params.setdefault("clientId", clientId)
        params.setdefault("clientSecret", clientSecret)
        params.setdefault("redirect_uri", kwargs.get("redirect_uri"))
        params.setdefault("code", kwargs.get("code"))
        params.setdefault("username", kwargs.get("user"))
        params.setdefault("password", kwargs.get("pwd"))
        return self._req(method="get", url=url, params=params)

    def refresh_token(self, clientId, clientSecret, refreshToken):
        """
        :param clientId: 应用id
        :param clientSecret: 应用密钥
        :param refreshToken: 用作刷新的token
        :return:
        """
        url = self.root_url + AUTHORIZATION_TOKEN
        params = dict()
        json_data = dict()
        params.setdefault("grant_type", "refresh_token")
        params.setdefault("clientId", clientId)
        params.setdefault("clientSecret", clientSecret)
        json_data.setdefault("refreshToken", refreshToken)
        return self._req(method="get", url=url, json_data=json_data, params=params)

    def verify_token(self, clientId, token):
        """
        验证签发的token是否在授权认证期
        :param clientId: 
        :param token: 
        :return: 
        """
        url = self.root_url + VERIFY_TOKEN
        headers = dict()
        headers.setdefault("Cookies", "clientId="+clientId)
        headers.setdefault("token", token)
        return self._req(method="get", url=url, headers=headers)

    def qrcode_url(self, clientId, qr_type, r_diff, state):
        """
        获取钉钉或者微信的登录二维码
        :param clientId:
        :param qr_type: 1:钉钉; 2:维系
        :param r_diff:
        :param state:
        :return: 二维码url地址
        """
        url = self.root_url + QR_CODE_ADDRESS
        headers = dict()
        params = dict()
        headers.setdefault("Cookies", "clientId="+clientId)
        params.setdefault("qr_type", qr_type)
        params.setdefault("state", state)
        params.setdefault("r_diff", r_diff)
        return self._req(method="get", url=url, params=params, headers=headers)

    def scan_create_code(self, clientId, type, code, state=None):
        """
        根据扫码认证后得到的第三方授权码换取用户中心的授权code
        :param clientId:
        :param type: 1:钉钉; 2:微信
        :param code: 认证授权码
        :param state:
        :return:
        """
        url = self.root_url + QR_AUTHORIZATION_CODE
        headers = dict()
        json_data = dict()
        headers.setdefault("Cookies", "clientId="+clientId)
        json_data.setdefault("type", type)
        json_data.setdefault("code", code)
        json_data.setdefault("state", state)
        return self._req(method="post", url=url, json_data=json_data, headers=headers)

    def bingding(self, clientId, token, type, code, state=None):
        """
        已登录用户可通过扫描二维码后绑定
        :param clientId:
        :param token:
        :param type: 1:钉钉; 2:微信
        :param code: 认证授权码
        :param state:
        :return:
        """
        url = self.root_url + QR_BINGDING
        headers = dict()
        json_data = dict()
        headers.setdefault("Cookies", "clientId="+clientId)
        headers.setdefault("Authorization", "Bearer " + token)
        json_data.setdefault("type", type)
        json_data.setdefault("code", code)
        json_data.setdefault("state", state)
        return self._req(method="post", url=url, json_data=json_data, headers=headers)

    def register(self, json_data:dict):
        """
        :param json_data: 注册参数查看文档
        410147:return:
        """
        url = self.root_url + REGISTER_USER
        return self._req(method="post", url=url, json_data=json_data)

    def add_user(self, token, clientId, json_data:dict):
        """
        新增用户
        :param token:
        :param clientId:
        :param json_data:
        :return:
        """
        url = self.root_url + ADD_USER
        headers = dict()
        headers.setdefault("Cookies", "clientId="+clientId)
        headers.setdefault("Authorization", "Bearer " + token)
        return self._req(method="post", url=url, json_data=json_data, headers=headers)

    def own_detail(self, clientId, token):
        """
        通过token获取个人详情
        :param clientId:
        :param token:
        :return:
        """
        url = self.root_url + OWN_USER_DETAIL
        headers = dict()
        headers.setdefault("Cookies", "clientId="+clientId)
        headers.setdefault("Authorization", "Bearer " + token)
        return self._req(method="get", url=url, headers=headers)

    def user_detail(self, token, userId, clientId=None):
        """
        通过id获取自己或他人详情
        :param clientId:
        :param token:
        :return:
        """
        url = self.root_url + DETAIL_USER.format(userId)
        headers = dict()
        headers.setdefault("Cookies", "clientId="+clientId)
        headers.setdefault("Authorization", "Bearer " + token)
        return self._req(method="get", url=url, headers=headers)

    def user_list(self, clientId=None, token=None, params: dict=None, json_data: dict=None):
        """
        获取用户列表
        :param clientId:
        :param token:
        :param params:
                        page: int = Query(1, ge=1),
                        page_size: int = Query(10, ge=10),
                        order_by: str = 'id',  # '-id' 如有 - 号为降序 从大到小
                        like: int = 0,  # 传1 or 0
        :param json_data:
                        phoneNumber: str = None
                        realName: str = None
                        gender: str = None
                        flag: int = None
                        status: int = None
        :return:
        """
        url = self.root_url + LIST_USER
        headers = dict()
        if clientId:
            headers.setdefault("Cookies", "clientId="+clientId)
        if token:
            headers.setdefault("Authorization", "Bearer " + token)
        return self._req(method="post", url=url, json_data=json_data, params=params, headers=headers)

    def reset_password(self, token, userId):
        """
        重置密码, 新密码为手机号
        :param token:
        :param userId:
        :return:
        """
        url = self.root_url + RESET_PWD.format(userId)
        headers = dict()
        headers.setdefault("Authorization", "Bearer "+token)
        return self._req(method="put", url=url, headers=headers)

    def set_password(self, token, userId, json_data:dict):
        """
        修改密码
        :param token:
        :param userId:
        :param json_data:
                        password: 旧密码
                        new_password: 新密码
        :return:
        """
        url = self.root_url + SET_PWD.format(userId)
        headers = dict()
        headers.setdefault("Authorization", "Bearer "+token)
        return self._req(method="put", url=url, json_data=json_data, headers=headers)

    def update_user(self, token, userId, clientId=None, json_data:dict=None,):
        """
        修改用户信息
        :param token:
        :param userId:
        :param clientId:
        :param json_data:
                        server: str
                        realName:  None
                        gender:  None
                        flag:   None
                        hospital:  None
                        department:  None
                        otherContact:  None
                        expertImage:  None
                        userEmail:  None
                        nick_name:  None
                        jobNumber:  None
                        status:  None
        :return:
        """
        url = self.root_url + UPDATE_USER.format(userId)
        headers = dict()
        headers.setdefault("Authorization", "Bearer " + token)
        if clientId:
            headers.setdefault("Cookies", "clientId=" + clientId)
        return self._req(method="put", url=url, json_data=json_data, headers=headers)