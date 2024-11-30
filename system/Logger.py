import logging
import colorlog


class Logger:
    logger=None
    @staticmethod
    def init_logger(log_name='mylog',logfile=None, loglevel='debug'):
        # 创建logger对象
        Logger.logger = logging.getLogger(log_name)
        Logger.logger.setLevel(logging.DEBUG)

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
        Logger.logger.addHandler(console_handler)

        if logfile:
            # 创建文件输出handler
            file_handler = logging.FileHandler(logfile, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            Logger.logger.addHandler(file_handler)

        # 设置日志级别
        if loglevel == 'debug':
            Logger.logger.setLevel(logging.DEBUG)
        elif loglevel == 'info':
            Logger.logger.setLevel(logging.INFO)
        elif loglevel == 'warning':
            Logger.logger.setLevel(logging.WARNING)
        elif loglevel == 'error':
            Logger.logger.setLevel(logging.ERROR)
        elif loglevel == 'critical':
            Logger.logger.setLevel(logging.CRITICAL)
    @staticmethod
    def debug(msg):
        Logger.logger.debug(msg)
    @staticmethod
    def info(msg):
        Logger.logger.info(msg)
    @staticmethod
    def warning(msg):
        Logger.logger.warning(msg)
    @staticmethod
    def error(msg):
        Logger.logger.error(msg)
    @staticmethod
    def critical(msg):
        Logger.logger.critical(msg)

Logger.init_logger()


if __name__ == '__main__':
    # logger = Logger()
    # logger.init_logger(None, 'debug')
    # 初始化日志记录器，不写文件
    # logger = init_logger(None, 'debug')
    Logger.debug('debug message')
    Logger.info('info message')
    Logger.warning('warning message')
    Logger.error('error message')
    Logger.critical('critical message')

    # 初始化日志记录器，写文件
    # logger = init_logger('test.log', 'info')
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warning message')
    # logger.error('error message')
    # logger.critical('critical message')
