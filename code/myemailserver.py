import zmail
from typing import List
import logging
from MyLogger import Logger

logger = Logger(log_file_name='log.txt', log_level=logging.DEBUG).get_log()

class MyEmailServer:

    @staticmethod
    def send_mail(subject: str, content_text: str, to_addr: List[str] or str) -> bool:
        try:
            # 配置发送方的邮箱和密码
            server = zmail.server('buddaa@163.com', 'xxxxxx')
            # 邮件的主题和内容
            mail_content = {'subject': subject, 'content_text': content_text}

            return server.send_mail(to_addr, mail_content)
        except:
            logger.info('email or password is error ... ')
            logger.debug("hello")
            return False

if __name__ == '__main__':
    result = MyEmailServer.send_mail("般若波罗蜜多心经",
                            "观自在菩萨，行深般若波罗蜜多时，照见......",
                            'buddaa@foxmail.com')

    print(result)
