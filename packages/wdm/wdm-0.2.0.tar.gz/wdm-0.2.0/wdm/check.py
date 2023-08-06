import subprocess
from subprocess import DEVNULL   # TODO: check Python 3.3 above
import re

# TODO: set logging level
STDIN = DEVNULL  # quiet, None for info level

def get_vboxmanage(command):
    """Get the full path of vboxmanage"""
    try:
        sp = subprocess.Popen([command, '-version'], stdin=DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        version, error = sp.communicate()
    except:
        return None, None
    else:
        return command, version

VBOXM, VBOXVER = get_vboxmanage("vboxmanage")
VBOXVER = str(VBOXVER, 'utf-8').split('\n')[0]

def is_vm_exists(name):
    """Check the given vm is exists

    Args:
        name (string): target name of vm
    """
    vmcmd = VBOXM
    command = [vmcmd] + ['list', 'vms']

    try:
        sp = subprocess.Popen(command, stdin=DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = sp.communicate()
    except:
        return False
    result = str(result, 'utf-8').split('\n')
    pattern = "^\"" + name + "\""
    for i in result:
        if re.search(pattern, i):
            return True
    return False

def is_vm_running(vmcmd, name):
    """Check the given vm is running

    Args:
        vmcmd (string): command name of virtualizer
        name (string): target name of vm
    """
    command = [vmcmd] + ['list', 'runningvms']

    try:
        sp = subprocess.Popen(command, stdin=DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = sp.communicate()
    except:
        return False
    result = str(result, 'utf-8').split('\n')
    pattern = "^\"" + name + "\""
    for i in result:
        if re.search(pattern, i):
            return True
    return False

def is_safe_to_create(name): # TODO: need to rename the method name
    """Check if the device is running
    
    :param name:
        the name of device
    """
    
    if VBOXM == None:
        print("Please install virtualbox.")
        return False

    if is_vm_exists(name) and is_vm_running(VBOXM, name):
        return False
    else:
        return True
    