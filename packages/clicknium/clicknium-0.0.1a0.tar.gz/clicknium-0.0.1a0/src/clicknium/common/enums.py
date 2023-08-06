from enum import Enum


class WindowMode(Enum):
    Auto = "auto"
    TopMost = "topmost"
    NoAction = "noaction"

class ClickType(Enum):
    Click = "click"
    Up = "up"
    Down = "down"

class PreAction(Enum):
    SetFocus = "setfocus"
    Click = "click"

class MouseButton(Enum):
    Left = "left"
    Right = "right"
    Middle = "middle"

class ClickLocation(Enum):
    Center = "center"
    LeftTop = "lefttop"
    LeftBottom = "leftbottom"
    RightTop = "righttop"
    RightBottom = "rightbottom"

class ModifierKey(Enum):
    NoneKey = "nonekey"
    Alt = "alt"
    Ctrl = "ctrl"
    Shift = "shift"
    Win = "win"

class CheckType(Enum):
    Check = "check"
    UnCheck = "uncheck"
    Toggle = "toggle"

class Color(object):
    Black = "#000000"
    Blue = "#0000ff"
    Green = "#008000"
    Orange = "#ffa500"
    Pink = "#ffcocb"
    Purple = "#800080"
    Red = "#ff0000"
    Yellow = "#ffff00"

class WebUserDataMode(Enum):
    Automatic = "automatic"
    DefaultFolder = "defaultfolder"
    CustomFolder = "customfolder"

class InputMethod(Enum):
    Default = "default"
    ControlSetValue = "controlsetvalue"
    KeyboardSimulateWithClick = "keyboardsimulatewithclick"
    KeyboardSimulateWithSetFocus = "keyboardsimulatewithsetfocus"

class ClickMethod(Enum):
    Default = "default"
    MouseEmulation = "mouseemulation"
    ControlInvocation = "controlinvocation"

class ClearMethod(Enum):
    ControlClearValue = "controlclearvalue"
    SendHotKey = "sendhotkey"

class ClearHotKey(Enum):    
        CtrlA_Delete = "{CTRL}{A}{DELETE}"
        End_ShiftHome_Delete = "{END}{SHIFT}{HOME}{DELETE}"
        Home_ShiftEnd_Delete = "{HOME}{SHIFT}{END}{DELETE}"

class _InternalClickType:
    Click = 0
    DoubleClick = 1
    Up = 2
    Down = 3

class BrowserType:
    Default = "default"
    IE = "ie"
    Chrome = "chrome"
    FireFox = "firefox"
    Edge = "edge"

class AutomationTech:
    Uia = "uia"
    Java ="java"
    IE ="ie"
    Chrome = "chrome"
    Firefox = "firefox"
    Sap = "sap"
    Edge = "edge"
    IA = 'ia'

class EventTypes:
    ApiCall = 0
    ExceptionReport = 1

def convert_clickType(source_type):
    source_type = ClickType(source_type)
    if source_type == ClickType.Click:
        return _InternalClickType.Click
    elif source_type == ClickType.Down:
        return _InternalClickType.Down
    elif source_type == ClickType.Up:
        return _InternalClickType.Up