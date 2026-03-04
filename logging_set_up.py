import logging

def setup_loggers(name,log_file):
    #creating custom loggers
    logger = logging.getLogger(name)


    #configure custom loggers
    logger.setLevel(logging.DEBUG)
    file_handling = logging.FileHandler(log_file)
    formating = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
    file_handling.setFormatter(formating)
    logger.addHandler(file_handling)
    return logger