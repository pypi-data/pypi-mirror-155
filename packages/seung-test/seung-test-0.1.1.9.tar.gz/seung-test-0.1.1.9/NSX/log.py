#######################################################################logger사용법#######################################################################
#main 모듈에서
#from NSX.log import CreateLogger
#def main():
#    logger.info('xxxx')
#
#if __name__ == '__main__':
#    logger = CreateLogger('NSX') #package이름으로 해야 로그파일이 남음.
#    main()
#
#연결된 모듈에서
#logger = logging.getLogger(__name__)
# def xxx
#     logger.info('xxxx')



import logging
from logging.handlers import RotatingFileHandler

def CreateLogger(logger_name):
    # Create Logger
    logger = logging.getLogger(logger_name)

    # Check handler exists
    if len(logger.handlers) > 0:
        return logger # Logger already exists

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('\n[%(levelname)s|%(name)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    # Create Handlers
    #streamHandler = logging.StreamHandler()
    #streamHandler.setLevel(logging.DEBUG)

    fileMaxByte =  1024 * 1024 * 1
    fileHandler = RotatingFileHandler(f'{logger_name}.txt', mode='a', maxBytes = fileMaxByte,backupCount = 10)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)

    #logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)

    return logger
