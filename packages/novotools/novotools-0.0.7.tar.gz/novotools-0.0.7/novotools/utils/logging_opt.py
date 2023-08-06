import logging

#=======================================
#basic_log set the basicConfig of logging and return a logger 
#========================================

def basic_log(name,level=logging.DEBUG,logfile=None,filemode="w",log_format=None):
    """
    Set basic logging config and name a logger
    """
    if not log_format:
        log_format = '[%(asctime)s:%(funcName)s:%(name)s:%(levelname)s] %(message)s'
    if logfile:
        logging.basicConfig(filename=logfile,level=level,
            filemode=filemode,format= log_format
            )
    else:
        logging.basicConfig(level=level,format=log_format)

    logger = logging.getLogger(name)

    return logger

#==========================================
#multi_logger output log to logfile and stdout at the same time
#==========================================
def multi_logger(name,level=logging.DEBUG,logfile='foo.log',mode='w',log_format=None):
    """
    this functions output log to standard output and log file
    """
    if not log_format:
        log_format = '[%(asctime)s:%(funcName)s:%(name)s:%(levelname)s] %(message)s'
        formatter = logging.Formatter(log_format)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    fh = logging.FileHandler(logfile,mode=mode,encoding='utf-8')
    fh.setLevel(level)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
