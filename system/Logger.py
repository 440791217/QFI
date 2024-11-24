import logging
import colorlog


class Logger:

    def __init__(self, log_name='mylog',logfile=None, loglevel='debug'):
        """初始化日志记录器
    
        Args:
            logfile: 日志文件名，不写入日志文件则传入None
            loglevel: 日志级别，可选值为debug、info、warning、error、critical
    
        Returns:
            logger: 返回初始化后的logger对象
            :param loglevel:
            :param logfile:
            :param log_name:
        """
        # 创建logger对象
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)

        # 创建控制台输出handler
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s %(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white'
            }
        ))
        self.logger.addHandler(console_handler)

        if logfile:
            # 创建文件输出handler
            file_handler = logging.FileHandler(logfile, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            self.logger.addHandler(file_handler)

        # 设置日志级别
        if loglevel == 'debug':
            self.logger.setLevel(logging.DEBUG)
        elif loglevel == 'info':
            self.logger.setLevel(logging.INFO)
        elif loglevel == 'warning':
            self.logger.setLevel(logging.WARNING)
        elif loglevel == 'error':
            self.logger.setLevel(logging.ERROR)
        elif loglevel == 'critical':
            self.logger.setLevel(logging.CRITICAL)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    logger = Logger()
    # logger.init_logger(None, 'debug')
    # 初始化日志记录器，不写文件
    # logger = init_logger(None, 'debug')
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')

    # 初始化日志记录器，写文件
    # logger = init_logger('test.log', 'info')
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warning message')
    # logger.error('error message')
    # logger.critical('critical message')
