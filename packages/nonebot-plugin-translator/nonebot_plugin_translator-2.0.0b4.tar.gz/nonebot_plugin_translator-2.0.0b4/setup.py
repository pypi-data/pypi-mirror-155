# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_translator']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.4,<3.0.0',
 'ujson>=4.3.0,<6.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-translator',
    'version': '2.0.0b4',
    'description': 'Multi language tanslator worked with nonebot2',
    'long_description': '##############################################################################\n多语种翻译插件\n##############################################################################\n| 基于 `NoneBot2 <https://github.com/nonebot/nonebot2>`_。\n\n******************************************************************************\n前言\n******************************************************************************\n| 接口来自 `腾讯机器翻译 TMT <https://cloud.tencent.com/product/tmt>`_ 目前使用 `签名方法 v1 <https://cloud.tencent.com/document/api/213/15692#.E4.BD.BF.E7.94.A8.E7.AD.BE.E5.90.8D.E6.96.B9.E6.B3.95-v1-.E7.9A.84.E5.85.AC.E5.85.B1.E5.8F.82.E6.95.B0>`_\n\n******************************************************************************\n准备工作\n******************************************************************************\n* 在 `云API密钥 <https://console.cloud.tencent.com/capi>`_ 新建密钥\n   取得 ``SecretId`` 和 ``SecretKey``\n* 打开 `机器翻译控制台 <https://console.cloud.tencent.com/tmt>`_ 确认是否能正常看到概览页面\n   若提示没有完成实名认证，则需要完成才能继续和正常使用\n\n******************************************************************************\n开始使用\n******************************************************************************\n| 建议使用 poetry\n|\n\n* 通过 poetry 添加到 NoneBot2 项目的 pyproject.toml\n\n.. code:: cmd\n\n poetry add nonebot-plugin-translator\n\n* 也可以通过 pip 从 `PyPI <https://pypi.org/project/nonebot-plugin-translator/>`_ 安装\n\n.. code:: cmd\n\n pip install nonebot-plugin-translator\n\n* 参照下文在 NoneBot2 项目的环境文件 ``.env.*`` 中添加配置项\n\n******************************************************************************\n配置项\n******************************************************************************\n| 腾讯云 API 请求的公共参数（必须）\n\n* tencentcloud_common_region ``str``\n   | `地域参数 <https://cloud.tencent.com/document/api/551/15615#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8>`_ ，用来标识希望操作哪个地域的数据\n* tencentcloud_common_secretid ``str``\n   | 在 `云API密钥 <https://console.cloud.tencent.com/capi>`_ 上申请的标识身份的 ``SecretId``，一个 ``SecretId`` 对应唯一的 ``SecretKey``\n* tencentcloud_common_secretkey ``str``\n   | 你的 ``SecretKey`` 用来生成请求签名 Signature\n\n.. code:: python\n\n # .env.prod\n tencentcloud_common_region = "ap-shanghai"\n tencentcloud_common_secretid = ""\n tencentcloud_common_secretkey = ""\n\n| 这样，就能够在 bot 所在群聊或私聊发送 ``翻译`` 或 ``机翻`` 使用了\n\n******************************************************************************\n常见问题\n******************************************************************************\n* 我确认我的安装和配置过程正确，但我发送 ``翻译`` 或 ``机翻`` 没有反应\n   | 如果在 ``.env.*`` 的 ``command_start`` 内仅设置了非空前缀，就必须在命令前加上前缀，比如 ``/翻译`` ``/机翻``\n\n******************************************************************************\n特别感谢\n******************************************************************************\n* `Mrs4s / go-cqhttp <https://github.com/Mrs4s/go-cqhttp>`_\n* `nonebot / nonebot2 <https://github.com/nonebot/nonebot2>`_\n\n******************************************************************************\n优化建议\n******************************************************************************\n| 请积极提交 Issues 或 Pull requests\n',
    'author': 'Lancercmd',
    'author_email': 'lancercmd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lancercmd/nonebot_plugin_translator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
