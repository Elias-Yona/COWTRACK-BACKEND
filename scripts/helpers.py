import getpass
import logging


def dummy2db_logger():
    '''creates a logger object'''
    username = getpass.getuser()
    FORMAT = '%(asctime)-15s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    extra_information = {'user': username}
    logger = logging.getLogger('dummy2db_logger')

    return logger, extra_information
