from __future__ import print_function
#
# Windows-only (right now)
#
# Code by Alexander Pruss and under the MIT license
#

from platform import system

if system() == 'Windows':
    from ctypes import windll, Structure, c_ulong, c_ushort, POINTER, Union, byref, c_int, sizeof, c_long

    LBUTTON = 1
    RBUTTON = 2
    CANCEL = 3
    MBUTTON = 4
    BACK = 8
    TAB = 9
    CLEAR = 12
    RETURN = 13
    SHIFT = 16
    CONTROL = 17
    MENU = 18
    PAUSE = 19
    CAPITAL = 20
    KANA = 21
    HANGUL = 21
    JUNJA = 23
    FINAL = 24
    HANJA = 25
    KANJI = 25
    ESCAPE = 27
    CONVERT = 28
    NONCONVERT = 29
    ACCEPT = 30
    MODECHANGE = 31
    SPACE = 32
    PRIOR = 33
    NEXT = 34
    END = 35
    HOME = 36
    LEFT = 37
    UP = 38
    RIGHT = 39
    DOWN = 40
    SELECT = 41
    PRINT = 42
    EXECUTE = 43
    SNAPSHOT = 44
    INSERT = 45
    DELETE = 46
    HELP = 47
    LWIN = 91
    RWIN = 92
    APPS = 93
    NUMPAD0 = 96
    NUMPAD1 = 97
    NUMPAD2 = 98
    NUMPAD3 = 99
    NUMPAD4 = 100
    NUMPAD5 = 101
    NUMPAD6 = 102
    NUMPAD7 = 103
    NUMPAD8 = 104
    NUMPAD9 = 105
    MULTIPLY = 106
    ADD = 107
    SEPARATOR = 108
    SUBTRACT = 109
    DECIMAL = 110
    DIVIDE = 111
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    F13 = 124
    F14 = 125
    F15 = 126
    F16 = 127
    F17 = 128
    F18 = 129
    F19 = 130
    F20 = 131
    F21 = 132
    F22 = 133
    F23 = 134
    F24 = 135
    NUMLOCK = 144
    SCROLL = 145
    LSHIFT = 160
    RSHIFT = 161
    LCONTROL = 162
    RCONTROL = 163
    LMENU = 164
    RMENU = 165
    PROCESSKEY = 229
    ATTN = 246
    CRSEL = 247
    EXSEL = 248
    EREOF = 249
    PLAY = 250
    ZOOM = 251
    NONAME = 252
    PA1 = 253
    OEM_CLEAR = 254
    XBUTTON1 = 0x05
    XBUTTON2 = 0x06
    VOLUME_MUTE = 0xAD
    VOLUME_DOWN = 0xAE
    VOLUME_UP = 0xAF
    MEDIA_NEXT_TRACK = 0xB0
    MEDIA_PREV_TRACK = 0xB1
    MEDIA_PLAY_PAUSE = 0xB3
    BROWSER_BACK = 0xA6
    BROWSER_FORWARD = 0xA7
    KEY_0 = 0x30
    KEY_1 = 0x31
    KEY_2 = 0x32
    KEY_3 = 0x33
    KEY_4 = 0x34
    KEY_5 = 0x35
    KEY_6 = 0x36
    KEY_7 = 0x37
    KEY_8 = 0x38
    KEY_9 = 0x39
    KEY_A = 0x41
    KEY_B = 0x42
    KEY_C = 0x43
    KEY_D = 0x44
    KEY_E = 0x45
    KEY_F = 0x46
    KEY_G = 0x47
    KEY_H = 0x48
    KEY_I = 0x49
    KEY_J = 0x4A
    KEY_K = 0x4B
    KEY_L = 0x4C
    KEY_M = 0x4D
    KEY_N = 0x4E
    KEY_O = 0x4F
    KEY_P = 0x50
    KEY_Q = 0x51
    KEY_R = 0x52
    KEY_S = 0x53
    KEY_T = 0x54
    KEY_U = 0x55
    KEY_V = 0x56
    KEY_W = 0x57
    KEY_X = 0x58
    KEY_Y = 0x59
    KEY_Z = 0x5A
    KEY_SEMICOLON = 0xBA
    KEY_PLUS = 0xBB
    KEY_COMMA = 0xBC
    KEY_MINUS = 0xBD
    KEY_PERIOD = 0xBE
    KEY_SLASH = 0xBF
    KEY_BACKQUOTE = 0xC0
    KEY_OPEN_BRACKET = 0xDB
    KEY_BACKSLASH = 0xDC
    KEY_CLOSE_BRACKET = 0xDD
    KEY_APOSTROPHE = 0xDE
    
    KEYEVENT_KEYUP = 0x0002
        
    class KeybdInputType(Structure):
        _fields_ = [('wVk', c_ushort), 
                    ('wScan', c_ushort),
                    ('dwFlags', c_ulong),
                    ('time', c_ulong),
                    ('dwExtraInfo', POINTER(c_ulong))]
                    
    class HardwareInputType(Structure):
        _fields_ = (('uMsg', c_ulong),
                    ('wParamL', c_ushort),
                    ('wParamH', c_ushort))

    class MouseInputType(Structure):
        _fields_ = (('dx', c_long),
                    ('dy', c_long),
                    ('mouseData', c_ulong),
                    ('dwFlags', c_ulong),
                    ('time', c_ulong),
                    ('dwExtraInfo', POINTER(c_ulong)))
                
    class InputUnionType(Union):
        _fields_ = [('mi', MouseInputType), ('ki', KeybdInputType), ('hi', HardwareInputType)]
                    
    class InputType(Structure):
        _fields_ = [('type', c_ulong),
                    ('union', InputUnionType)]
                    
    def pressKey(key):
        data = (InputType*1)(InputType(1, InputUnionType(ki=KeybdInputType(key,key,0,0,None))))
        windll.user32.SendInput(1, data, c_int(sizeof(data)))
        
    def releaseKey(key):
        data = (InputType*1)(InputType(1, InputUnionType(ki=KeybdInputType(key,key,KEYEVENT_KEYUP,0,None))))
        windll.user32.SendInput(1, data, c_int(sizeof(data)))
        
    def getPressState(key):
        v = windll.user32.GetAsyncKeyState(int(key))
        return bool(0x8000 & v), bool(0x0001 & v)
    
    def isPressedNow(key):
        return bool(0x8000 & windll.user32.GetAsyncKeyState(int(key)))

    def wasPressedSinceLast(key):
        return bool(0x0001 & windll.user32.GetAsyncKeyState(int(key)))
        
    def clearPressBuffer(key):
        while wasPressedSinceLast(key):
            pass

    """            
    class POINT(Structure):
        _fields_ = [("x", c_ulong), ("y", c_ulong)]
            
    def getMousePosition():
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return (pt.x, windll.user32.GetSystemMetrics(1)-1-pt.y)
        
    def getScreenSize():
        return (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
    """
        
else:
    raise Exception('Platform '+system()+' not supported.')
            
if __name__ == '__main__':
    from time import sleep
    print("Press ESC to exit. Testing spacebar.")
    while True:
        if wasPressedSinceLast(ESCAPE):
            print("Done")
            break
        now,last = getPressState(ord(' '))
        if now or last:
            print(now, last)
#        print(getMousePosition(), getScreenSize())
        sleep(0.01)
        