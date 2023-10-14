import subprocess
import time

from helpers import dummy2db_logger


logger, extra_information = dummy2db_logger()


def _mysqld_process_checkpoint():
    '''checks if mysql is available. if not it starts one
    '''
    try:
        subprocess.check_output("pgrep mysqld", shell=True)
    except Exception:
        logger.warning(
            'Your mysql server is offline, dummy2db will try to launch it now!',
            extra=extra_information)

        subprocess.Popen("mysqld", close_fds=True, shell=True)
        time.sleep(3)


def main(db=None):
    if db is None:
        logger.error(
            'Provide a database name!', extra=extra_information)
