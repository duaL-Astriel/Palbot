import subprocess

def is_service_running(service_name):
    try:
        output = subprocess.check_output("systemctl is-active --quiet " + service_name, shell=True)
        if output == b'active\n':
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False
