# # -*- coding: utf-8 -*-
import os
import sys
# 兼容安装到非系统默认目录导入找不到模块的问题
package_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if package_path not in sys.path:
    sys.path.append(package_path)

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__, __copyright__
from .hmac_auth import HmacAuth  # pylint: disable=unused-import
