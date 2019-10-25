import logging
#
# logger = logging.getLogger("django")  # 为loggers中定义的名称
# logger.info("some info...")


logger=logging.getLogger('hello')
handle=logging.FileHandler('log.txt')
formatter=logging.Formatter("%(levelname)s - %(asctime)s - %(message)s ")
handle.setFormatter(formatter)
logger.addHandler(handle)
logger.error('你错了')
logger.critical('你错了')
logger.warning('哈哈')