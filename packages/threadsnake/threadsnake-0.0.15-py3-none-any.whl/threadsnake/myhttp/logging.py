##    threadsnake. A tiny experimental server-side express-like library.
##    Copyright (C) 2022  Erick Fernando Mora Ramirez
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.
##
##    mailto:erickfernandomoraramirez@gmail.com


from enum import IntEnum
import sys
from threading import Lock, Thread, get_ident
from time import strftime
from typing import final
import ctypes, ctypes.wintypes
import atexit



if sys.platform == 'win32':
    oldConsoleMode = ctypes.wintypes.DWORD(0)
    def reset_console_mode():
        global oldConsoleMode
        if sys.platform == 'win32':
            kernel = ctypes.windll.kernel32
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), oldConsoleMode)
    kernel = ctypes.windll.kernel32
    kernel.GetConsoleMode(kernel.GetStdHandle(-11), ctypes.byref(oldConsoleMode))
    kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
    atexit.register(reset_console_mode)
    

    

    
    
class LogColorMode(IntEnum):
    NONE = 0
    MESSAGE = 1
    TITLE = 2
    ALL = 3

class LogLevel(IntEnum):
    NONE = 0
    SUCCESS = 1
    INFO = 2
    WARNING = 4
    ERROR = 8
    FATAL = 16
    LOAD = 32
    ALL = 63
    
class LogColors:
    BRIGHT_FOREGROUND_WHITE = '\033[97m'
    BRIGHT_FOREGROUND_RED = '\033[91m'
    BRIGHT_FOREGROUND_GREEN = '\033[92m'
    BRIGHT_FOREGROUND_BLUE = '\033[94m'
    BRIGHT_FOREGROUND_YELLOW = '\033[93m'
    BRIGHT_FOREGROUND_MAGENTA = '\033[95m'
    BRIGHT_FOREGROUND_CYAN = '\033[96m'
    BRIGHT_FOREGROUND_BLACK = '\033[90m'
    
    DARK_FOREGROUND_WHITE = '\033[37m'
    DARK_FOREGROUND_RED = '\033[31m'
    DARK_FOREGROUND_GREEN = '\033[32m'
    DARK_FOREGROUND_BLUE = '\033[34m'
    DARK_FOREGROUND_YELLOW = '\033[33m'
    DARK_FOREGROUND_MAGENTA = '\033[35m'
    DARK_FOREGROUND_CYAN = '\033[36m'
    DARK_FOREGROUND_BLACK = '\033[30m'
    
    BRIGHT_BACKGROUND_WHITE = '\033[107m'
    BRIGHT_BACKGROUND_RED = '\033[101m'
    BRIGHT_BACKGROUND_GREEN = '\033[102m'
    BRIGHT_BACKGROUND_BLUE = '\033[104m'
    BRIGHT_BACKGROUND_YELLOW = '\033[103m'
    BRIGHT_BACKGROUND_MAGENTA = '\033[105m'
    BRIGHT_BACKGROUND_CYAN = '\033[106m'
    BRIGHT_BACKGROUND_BLACK = '\033[100m'
    
    DARK_BACKGROUND_WHITE = '\033[47m'
    DARK_BACKGROUND_RED = '\033[41m'
    DARK_BACKGROUND_GREEN = '\033[42m'
    DARK_BACKGROUND_BLUE = '\033[44m'
    DARK_BACKGROUND_YELLOW = '\033[43m'
    DARK_BACKGROUND_MAGENTA = '\033[45m'
    DARK_BACKGROUND_CYAN = '\033[46m'
    DARK_BACKGROUND_BLACK = '\033[40m'
    ENDC = '\033[0m'

colors = {
    LogLevel.SUCCESS : LogColors.BRIGHT_FOREGROUND_GREEN,
    LogLevel.INFO : LogColors.BRIGHT_FOREGROUND_BLUE,
    LogLevel.WARNING : LogColors.BRIGHT_FOREGROUND_YELLOW,
    LogLevel.ERROR: LogColors.BRIGHT_FOREGROUND_RED,
    LogLevel.FATAL: LogColors.DARK_BACKGROUND_RED + LogColors.DARK_FOREGROUND_BLACK,
    LogLevel.LOAD: LogColors.BRIGHT_FOREGROUND_MAGENTA
}

prefixes = {
    LogLevel.SUCCESS : 'Success',
    LogLevel.INFO : 'Info',
    LogLevel.WARNING : 'Warning',
    LogLevel.ERROR: 'Error',
    LogLevel.FATAL: 'Fatal',
    LogLevel.LOAD: 'Load' 
}

logLevel:LogLevel = LogLevel.NONE
logMode:LogColorMode = LogColorMode.TITLE
logLock:Lock = Lock()

def set_log_config(level:LogLevel = LogLevel.NONE, mode:LogColorMode = LogColorMode.TITLE):
    global logLevel, logMode
    logLevel = level
    logMode = mode

def toggle_log_level(level:LogLevel):
    global logLevel
    logLevel ^= level

def log(message:str, title:str = None, level:LogLevel = LogLevel.INFO, threadId:int = 0):
    global logLevel, logMode, colors, prefixes, logLock
    try:
        logLock.acquire()
        if level & logLevel == level and level in colors:
            moment = strftime('%Y-%m-%d %H:%M:%S')
            color = colors[level]
            logPrefix = '>' if level not in prefixes else prefixes[level]
            title = logPrefix if title is None else f'{logPrefix}:{title}'
            title = f'{moment} (Thread:{threadId}) [{title}]'
            fullMessage = title if (logMode & LogColorMode.TITLE != LogColorMode.TITLE) else color + title + LogColors.ENDC
            fullMessage += ' '
            fullMessage += message if (logMode & LogColorMode.MESSAGE != LogColorMode.MESSAGE) else color + title + LogColors.ENDC
            print(fullMessage)
    except Exception as e:
        print(e)
    finally:
        logLock.release()

def badge(text:str, textBackground:LogColors = LogColors.DARK_BACKGROUND_BLUE, title:str = None, titleBackground:LogColors = LogColors.DARK_BACKGROUND_BLACK):
    message = titleBackground + f' {title or ""} ' + textBackground + f' {text} ' + LogColors.ENDC
    try:
        logLock.acquire()
        print()
        print(message)
        print()
    except Exception as e:
        print(e)
    finally:
        logLock.release()

def badge_async(text:str, textBackground:LogColors = LogColors.DARK_BACKGROUND_BLUE, title:str = None, titleBackground:LogColors = LogColors.DARK_BACKGROUND_BLACK):
    Thread(target=lambda: badge(text, textBackground, title, titleBackground)).start()
        
def log_async(message:str, title:str = None, level:LogLevel = LogLevel.INFO):
    Thread(target=lambda: log(message, title, level, get_ident())).start()

def log_success(message:str, title:str = None) -> None:
    log_async(message, title, LogLevel.SUCCESS)
    
def log_info(message:str, title:str = None) -> None:
    log_async(message, title, LogLevel.INFO)
    
def log_error(message:str, title:str = None) -> None:
    log_async(message, title, LogLevel.ERROR)
    
def log_warning(message:str, title:str = None) -> None:
    log_async(message, title, LogLevel.WARNING)
    
def log_fatal(message:str, title:str = None) -> None:
    log_async(message, title, LogLevel.FATAL)
    
def log_load(message:str, title:str = None) -> None:
    log_async(message, title, LogLevel.LOAD)
    
