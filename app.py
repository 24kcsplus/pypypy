import ipaddress
import json
import secrets
import socket
import requests
from time import sleep
from urllib.parse import urlparse
from flask import Flask, Response, request, session, abort

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def merge(src, dst):
    # Recursive merge function
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            try:
                v = (globals().get(v),) if globals().get(v) is not None else v
            except:
                pass
            setattr(dst, k, v)


class classproperty:
    def __init__(self, f):
        self.f = f

    def __get__(self, instance, owner):
        return self.f(owner)


class MethodFrozenMeta(type):
    """
    元类：禁止对指定的方法名在类对象上做 __setattr__ / __delattr__ 操作。
    /src 中不会显示这段代码，主要是防止直接修改 UIka 类中的方法，造成非预期解
    """
    # 用于存储 (Class, method_name) 对
    _frozen_methods = set()

    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        # 如果类定义中有 _freeze_list 属性，就把对应 (cls, method) 注册到 _frozen_methods 中
        freeze_list = namespace.get('_freeze_list', [])
        for method_name in freeze_list:
            MethodFrozenMeta._frozen_methods.add((cls, method_name))
        return cls

    def __setattr__(cls, name, value):
        if (cls, name) in MethodFrozenMeta._frozen_methods:
            raise TypeError(f"Cannot overwrite frozen method '{name}' on class {cls.__name__}")
        return super().__setattr__(name, value)

    def __delattr__(cls, name):
        if (cls, name) in MethodFrozenMeta._frozen_methods:
            raise TypeError(f"Cannot delete frozen method '{name}' on class {cls.__name__}")
        return super().__delattr__(name)


class Sadaharu():
    @classproperty
    def subclasses(self):
        return self.__subclasses__()[1]

    dark_of_togawa = '丰川家的黑暗'


class Kiyotsuku(Sadaharu):
    osake = '一吨啤酒使劲遭'


class Sakiko(Kiyotsuku):
    tako = '软弱的我已经死了'


class Uika(Sadaharu, metaclass=MethodFrozenMeta):
    _freeze_list = ['sakiko_love']  # 这一行也不显示

    def sakiko_love(self):
        if self.dark_of_togawa == 'uika_chan_love' and self.tako == 'uika_chan_love':
            return True
        else:
            return "saki_chan_saki_chan_saki_chan"


@app.route('/')
def index():
    return 'Python 酱， Python 酱， Python 酱！Python 酱， Python 酱， Python 酱！Python 酱！<br>到 /src 的话，就能见到Python酱吗 '


# 输出源码
@app.route('/src')
def src():
    with open('./src.py', "r", encoding="utf-8") as f:
        code = f.read()
    return Response(
        code,
        status=200,
        mimetype="text/x-python; charset=utf-8"
    )


@app.route('/go')
def pollute():
    try:
        payload = request.args.get("payload")
        if payload is None:
            return "It's mygo!!!!!"
        else:
            payload = json.loads(payload)
            sakiko = Sakiko()
            merge(payload, sakiko)
            uika = Uika()
            if uika.sakiko_love() != 'saki_chan_saki_chan_saki_chan':
                session['logged_in'] = True
                return 'You are logged in the system of tariff! Please go to /self.'
            else:
                session['logged_in'] = False
                return '我们也无法寻回，那相同的瞬间'
    except TypeError:
        return "什么也改变不了我对小祥的爱"
    except Exception as e:
        print(e)
        return "欢迎来到，Ave Mujica的世界"


def is_private_ip(ip_str):
    ip = ipaddress.ip_address(ip_str)
    return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved


def is_allowed_url(url):
    # 解析 URL
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        return False

    # 解析为 IP 地址
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    # 检查每个解析到的 IP 是否为内网 IP
    for family, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        if is_private_ip(ip_str):
            return False

    return True


@app.route('/self')
def self():
    try:
        if session.get('logged_in'):
            url = request.args.get("url", "")
            if url == '':
                return '试试访问6000端口的 /flag 以绕过关税'
            if not is_allowed_url(url):
                sleep(1.45)
                abort(403, "只有 Soyo 才能进入关税系统，现已增加 145% 关税")
            resp = requests.get(url, timeout=5)
            return resp.text, resp.status_code
        else:
            return '爱音大统领将国名修改为了 the United States of Anon，并将你驱逐出境'
    except Exception as e:
        print(e)
        return '为什么要访问这个网站！'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
