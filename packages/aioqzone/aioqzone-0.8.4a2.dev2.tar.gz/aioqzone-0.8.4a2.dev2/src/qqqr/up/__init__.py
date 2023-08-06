import re
from dataclasses import dataclass
from os import environ as env
from random import choice, random
from time import time_ns
from typing import Awaitable, Callable, Dict, Optional, Type

from aiohttp import ClientSession
from multidict import istr

from ..base import LoginBase
from ..constants import StatusCode
from ..exception import TencentLoginError
from ..type import APPID, PT_QR_APP, CheckResult, Proxy
from ..utils import get_all_cookie
from .encrypt import NodeEncoder, PasswdEncoder, TeaEncoder

CHECK_URL = "https://ssl.ptlogin2.qq.com/check"
LOGIN_URL = "https://ssl.ptlogin2.qq.com/login"
LOGIN_JS = "https://qq-web.cdn-go.cn/any.ptlogin2.qq.com/v1.3.0/ptlogin/js/c_login_2.js"


@dataclass
class User:
    uin: int
    pwd: str


UseEncoder = (
    TeaEncoder if env.get("AIOQZONE_PWDENCODER", "").strip().lower() == "python" else NodeEncoder
)


class UPLogin(LoginBase):
    node = "node"
    _captcha = None
    get_smscode = None
    encode_cls: Type[PasswdEncoder] = UseEncoder

    def __init__(
        self,
        sess: ClientSession,
        app: APPID,
        proxy: Proxy,
        user: User,
        info: Optional[PT_QR_APP] = None,
    ):
        super().__init__(sess, app, proxy, info=info)
        assert user.uin
        assert user.pwd
        self.user = user
        self.pwder = self.encode_cls(sess, user.pwd)

    def register_smscode_getter(self, getter: Callable[[], Awaitable[int]]):
        self.get_smscode = getter

    async def encodePwd(self, r: CheckResult) -> str:
        return await self.pwder.encode(r)

    async def deviceId(self) -> str:
        return ""

    async def check(self):
        """check procedure before login. This will return a CheckResult object containing
        verify code, session, etc.

        :raises `aiohttp.ClientResponseError`:

        :return: CheckResult
        """
        data = {
            "regmaster": "",
            "pt_tea": 2,
            "pt_vcode": 1,
            "uin": self.user.uin,
            "appid": self.app.appid,
            # 'js_ver': 21072114,
            "js_type": 1,
            "login_sig": self.login_sig,
            "u1": self.proxy.s_url,
            "r": random(),
            "pt_uistyle": 40,
        }
        async with self.session.get(CHECK_URL, params=data, ssl=self.ssl) as r:
            r.raise_for_status()
            r = re.findall(r"'(.*?)'[,\)]", await r.text())
        r[0] = int(r[0])
        return CheckResult(*r)

    async def sms(self, pt_sms_ticket: str):
        """Send verify sms (to get dynamic code)

        :param pt_sms_ticket: corresponding value in cookie, of the key with the same name
        """
        data = {
            "bkn": "",
            "uin": self.user.uin,
            "aid": self.app.appid,
            "pt_sms_ticket": pt_sms_ticket,
        }
        async with self.session.get(
            "https://ui.ptlogin2.qq.com/ssl/send_sms_code", params=data, ssl=self.ssl
        ) as r:
            rl = re.findall(r"'(.*?)'[,\)]", await r.text(encoding="utf8"))
            # ptui_sendSMS_CB('10012', '短信发送成功！')
        assert int(rl[0]) == 10012, rl[1]

    async def login(self, r: CheckResult, pastcode: int = 0, **add) -> Dict[str, str]:
        if r.code == StatusCode.Authenticated:
            # OK
            pass
        elif r.code == StatusCode.NeedCaptcha and pastcode == 0:
            # 0 -> 1: OK; !0 -> 1: Error
            cookie = await self.login(await self.passVC(r), StatusCode.NeedCaptcha)
            return cookie
        elif r.code == pastcode == StatusCode.NeedVerify:
            # !10009 -> 10009: OK; 10009 -> 10009: Error
            raise TencentLoginError(r.code, str(r))
        else:
            raise TencentLoginError(r.code, str(r))

        const = {
            "h": 1,
            "t": 1,
            "g": 1,
            "ptredirect": 0,
            "from_ui": 1,
            "ptlang": 2052,
            "js_type": 1,
            "pt_uistyle": 40,
        }
        data = {
            "u": self.user.uin,
            "p": await self.encodePwd(r),
            "verifycode": r.verifycode,
            "pt_vcode_v1": 1 if pastcode == StatusCode.NeedCaptcha else 0,
            "pt_verifysession_v1": r.verifysession,
            "pt_randsalt": r.isRandSalt,
            "u1": self.proxy.s_url,
            "action": f"{3 if pastcode == StatusCode.NeedCaptcha else 2}-{choice([1, 2])}-{int(time_ns() / 1e6)}",
            # 'js_ver': 21072114,
            "login_sig": self.login_sig,
            "aid": self.app.appid,
            "daid": self.app.daid,
            "ptdrvs": r.ptdrvs,
            "sid": r.session,
            "o1vId": await self.deviceId(),
        }
        data.update(const)
        data.update(add)
        self.session.headers.update({istr("referer"): "https://xui.ptlogin2.qq.com/"})
        async with self.session.get(LOGIN_URL, params=data, ssl=self.ssl) as response:
            response.raise_for_status()
            rl = re.findall(r"'(.*?)'[,\)]", await response.text())

        rl[0] = int(rl[0])
        if rl[0] == StatusCode.Authenticated:
            pass
        elif rl[0] == StatusCode.NeedVerify:
            m = response.cookies.get("pt_sms_ticket")
            if self.get_smscode:
                await self.sms(m.value if m else "")
                smscode = await self.get_smscode()
                await self.login(r, StatusCode.NeedVerify, pt_sms_code=smscode)
            else:
                raise NotImplementedError
        else:
            raise TencentLoginError(rl[0], rl[4])

        async with self.session.get(rl[2], allow_redirects=False, ssl=self.ssl) as response:
            return get_all_cookie(response)

    def captcha(self, sid: str):
        if not self._captcha:
            from .captcha import Captcha

            self._captcha = Captcha(self.session, self.ssl, self.app.appid, sid)
        return self._captcha

    async def passVC(self, r: CheckResult):
        c = self.captcha(r.session)
        await c.prehandle(self.xlogin_url)
        d = await c.verify()
        r.code = d.errorCode
        r.verifycode = d.randstr
        r.verifysession = d.ticket
        return r
