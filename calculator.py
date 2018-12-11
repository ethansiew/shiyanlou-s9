# -*- coding: utf-8 -*-
import sys
import csv
from collections import namedtuple

# 税率表条目类，该类由 namedtuple 动态创建，代表一个命名元组
IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
)

# 起征点常量
INCOME_TAX_START_POINT = 3500

# 税率表，里面的元素类型为前面创建的 IncomeTaxQuickLookupItem
INCOME_TAX_QUICK_LOOKUP_TABLE = [
    IncomeTaxQuickLookupItem(80000, 0.45, 13505),
    IncomeTaxQuickLookupItem(55000, 0.35, 5505),
    IncomeTaxQuickLookupItem(35000, 0.30, 2755),
    IncomeTaxQuickLookupItem(9000, 0.25, 1005),
    IncomeTaxQuickLookupItem(4500, 0.2, 555),
    IncomeTaxQuickLookupItem(1500, 0.1, 105),
    IncomeTaxQuickLookupItem(0, 0.03, 0)
]


class Args(object):
    """
    命令行参数处理类
    """

    def __init__(self):
        # 保存命令行参数列表
        self.args = sys.argv[1:]

    def _value_after_option(self, option):
        """
        内部函数，用来获取跟在选项后面的值
        """

        try:
            # 获得选项位置
            index = self.args.index(option)
            # 下一位置即为选项值
            return self.args[index + 1]
        except (ValueError, IndexError):
            print('Parameter Error')
            exit()

    @property
    def config_path(self):
        """
        配置文件路径
        """

        return self._value_after_option('-c')

    @property
    def userdata_path(self):
        """
        用户工资文件路径
        """

        return self._value_after_option('-d')

    @property
    def export_path(self):
        """
        税后工资文件路径
        """

        return self._value_after_option('-o')


# 创建一个全局参数类对象供后续使用
args = Args()


class Config(object):
    """
    配置文件处理类
    """

    def __init__(self):
        # 读取配置文件
        self.config = self._read_config()

    def _read_config(self):
        """
        内部函数，用来读取配置文件中的配置项
        """

        config = {}
        with open(args.config_path) as f:
            # 依次读取配置文件里的每一行并解析得到配置项名称和值
            for line in f.readlines():
                key, value = line.strip().split('=')
                try:
                    # 去掉前后可能出现的空格
                    config[key.strip()] = float(value.strip())
                except ValueError:
                    print('Parameter Error')
                    exit()

        return config

    def _get_config(self, key):
        """
        内部函数，用来获得配置项的值
        """

        try:
            return self.config[key]
        except KeyError:
            print('Config Error')
            exit()

    @property
    def social_insurance_baseline_low(self):
        """
        获取社保基数下限
        """

        return self._get_config('JiShuL')

    @property
    def social_insurance_baseline_high(self):
        """
        获取社保基数上限
        """

        return self._get_config('JiShuH')

    @property
    def social_insurance_total_rate(self):
        """
        获取社保总费率
        """

        return sum([
            self._get_config('YangLao'),
            self._get_config('YiLiao'),
            self._get_config('ShiYe'),
            self._get_config('GongShang'),
            self._get_config('ShengYu'),
            self._get_config('GongJiJin')
        ])


# 创建一个全局的配置文件处理对象供后续使用
config = Config()


class UserData(object):
    """
    用户工资文件处理类
    """

    def __init__(self):
        # 读取用户工资文件
        self.userdata = self._read_users_data()

    def _read_users_data(self):
        """
        内部函数，用来读取用户工资文件
        """

        userdata = []
        with open(args.userdata_path) as f:
            # 依次读取用户工资文件中的每一行并解析得到用户 ID 和工资
            for line in f.readlines():
                employee_id, income_string = line.strip().split(',')
                try:
                    income = int(income_string)
                except ValueError:
                    print('Parameter Error')
                    exit()
                userdata.append((employee_id, income))

        return userdata

    def __iter__(self):
        """
        实现 __iter__ 方法，使得 UserData 对象成为可迭代对象。
        """

        # 直接返回属性 userdata 列表对象的迭代器
        return iter(self.userdata)


