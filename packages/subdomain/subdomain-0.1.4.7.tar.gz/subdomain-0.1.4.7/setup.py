# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subdomain']

package_data = \
{'': ['*'], 'subdomain': ['dict/*']}

install_requires = \
['IPy>=1.01,<2.0',
 'aiodns>=3.0.0,<4.0.0',
 'autopep8>=1.6.0,<2.0.0',
 'cp-common>=0.1.2,<0.2.0',
 'loguru>=0.6.0,<0.7.0',
 'pytest>=5.2,<6.0']

setup_kwargs = {
    'name': 'subdomain',
    'version': '0.1.4.7',
    'description': '这是一个使用异步协程的子域名爆破工具。',
    'long_description': "<!--\n * @Version: 0.1\n * @Autor: zmf96\n * @Email: zmf96@qq.com\n * @Date: 2022-02-21 08:41:27\n * @LastEditors: zmf96\n * @LastEditTime: 2022-02-22 03:49:57\n * @FilePath: /README.md\n * @Description: \n-->\n# subdomain\n使用异步协程的子域名爆破工具\n\n采用cname与黑名单ip的方式来处理泛解析.\n\n## 安装\n\npython3.8.10 \n\n```bash\ngit clone https://github.com/HotSec/subdomain\ncd subdomain\npip3 install poetry\npoetry install\npoetry shell\n\npython subdomain/subdomain.py -h\n```\n## usage\n\n```bash\nusage: subdomain.py [-h] [-v] [-f FILE] -d DOMAIN [-s DEEP]\n\n使用aiodns爆破子域名\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --version         show program's version number and exit\n  -f FILE, --file FILE  指定字典文件\n  -d DOMAIN, --domain DOMAIN\n                        目标域名\n  -s DEEP, --deep DEEP  域名深度,默认 1\n```\n\n## Thanks\n\nsubdomain在[subdns](https://github.com/ldbfpiaoran/subdns.git)的基础上进行开发的.",
    'author': 'zmf96',
    'author_email': 'zmf96@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HotSec/subdomain',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
