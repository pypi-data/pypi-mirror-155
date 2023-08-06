from colorama import Fore as _Fore
from colorama import Style as _Style


_CONFIG = {
    "verbose":True,
}

def get(key,default_value=None):
    if key in _CONFIG:
        return _CONFIG[key]
    return default_value


def log(message,style=None):
    if get("verbose",False):
        if style is None:
            print(message)
        if style == "error":
            print(_Fore.RED + message + _Style.RESET_ALL)
        if style == "success":
            print(_Fore.GREEN + message + _Style.RESET_ALL)
        

