from termcolor import colored

# Private interface
def __log(prefix : str, color : str, message : str, **kwargs):
    # forward kwargs into string.format
    message = message.format(**kwargs)
    # insert color escape codes
    message = colored(prefix + message, color)
    # TODO add timestamp, write to file, filter by verbosity, etc
    print(message)

# Public interface
def log_info(message : str, **kwargs):
    __log('[Info] ', 'white', message, **kwargs)

def log_warning(message : str, **kwargs):
    __log('[Warning] ', 'yellow', message, **kwargs)

def log_error(message : str, **kwargs):
    __log('[Error] ', 'red', message, **kwargs)
