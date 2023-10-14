import subprocess
import time

def _mysqld_process_checkpoint():
    '''checks if mysql is available. if not it starts one
    '''
    try:
        subprocess.check_output("pgrep mysqld", shell=True)
    except Exception:
        subprocess.Popen("mysqld", close_fds=True, shell=True)
        time.sleep(3)
