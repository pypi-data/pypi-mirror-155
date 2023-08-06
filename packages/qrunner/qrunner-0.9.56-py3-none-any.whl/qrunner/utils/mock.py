import time
from qrunner.utils.faker import Faker
from qrunner.utils.log import logger

"""
Faker库支持方法：https://zhuanlan.zhihu.com/p/87203290
"""


class MockData(Faker):
    """随机数据+当前时间数据"""

    def __init__(self, language='cn'):
        """
        language: 支持语言，中文 cn、英文 en
        """
        if language == 'cn':
            locale = 'zh_CN'
            super().__init__(locale=locale)
        elif language == 'en':
            super().__init__()
        else:
            logger.debug(f'暂不支持这种语言-{language}')

    # -----------------------------随机数据-------------------------------
    def get_word(self):
        """随机词语"""
        return self.word()

    def get_words(self):
        """随机词语列表"""
        return self.words()

    def get_phone(self):
        """随机手机号"""
        return self.phone_number()

    def get_company_name(self):
        """随机公司名"""
        return self.company()

    def get_name(self):
        """随机人名"""
        return self.name()

    def get_timezone(self):
        """随机时区"""
        return self.timezone()

    def get_random_date(self):
        """随机日期"""
        return self.date()

    def get_number(self, length=3):
        """随机数"""
        return self.random_number(digits=length)

    def get_ssn(self):
        """随机身份证号"""
        return self.ssn()

    def get_email(self):
        """随机邮箱"""
        return self.email()

    def get_url(self):
        """随机url地址"""
        return self.url()

    # ------------------------当前时间------------------------
    @staticmethod
    def get_now_timestamp(length=None) -> str:
        """获取当前时间戳"""
        timestamp = str(int(time.time()))
        if length is None:
            return timestamp
        else:
            return timestamp.ljust(length, '0')

    @staticmethod
    def get_now_date(_format="%Y-%m-%d"):
        """获取当前日期"""
        return time.strftime(_format)

    @staticmethod
    def get_now_time(_format="%Y-%m-%d %H:%M:%S"):
        """获取当前时间"""
        return time.strftime(_format)


# 初始化
mock_data = MockData()










