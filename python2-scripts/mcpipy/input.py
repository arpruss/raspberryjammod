#
# Windows-only (right now)
# Copyright (c) 2016 Alexander Pruss. MIT License
#

from platform import system

if system() == 'Windows':
    from ctypes import windll

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
            print now, last
        sleep(0.01)
        