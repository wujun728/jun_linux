import ctypes;

class OSINFO(ctypes.Structure):
    _fields_ = [
        ("dwOSVersionInfoSize",ctypes.c_long),
        ("dwMajorVersion",ctypes.c_long),
        ("dwMinorVersion",ctypes.c_long),
        ("dwBuildNumber",ctypes.c_long),
        ("dwPlatformId",ctypes.c_long),
        ("szCSDVersion",ctypes.c_char*128)
    ];

def GetSystemVersionString():
    kernel32 = ctypes.windll.LoadLibrary("kernel32.dll");
    os = OSINFO();
    os.dwOSVersionInfoSize = ctypes.sizeof(os);
    if kernel32.GetVersionExA(ctypes.byref(os))==0:
        return "Null Version";
    if os.dwPlatformId==1: #windows 95/98/me
        if os.dwMajorVersion==4 and os.dwMinorVersion==0:
            verStr = "windows 95";
        elif os.dwMajorVersion==4 and os.dwMinorVersion==10:
            verStr = "windows 98";
        elif os.dwMajorVersion==4 and os.dwMinorVersion==90:
            verStr = "windows me";
        else:
            verStr = "unknown version";
    elif os.dwPlatformId==2: #windows vista/server 2008/server 2003/xp/2000/nt
        if os.dwMajorVersion==4 and os.dwMinorVersion==0:
            verStr = "windows nt 4.0";
        elif os.dwMajorVersion==5 and os.dwMinorVersion==0:
            verStr = "windows 2000";
        elif os.dwMajorVersion==5 and os.dwMinorVersion==1:
            verStr = "windows xp";
        elif os.dwMajorVersion==5 and os.dwMinorVersion==2:
            verStr = "windows 2003";
        elif os.dwMajorVersion==6 and os.dwMinorVersion==0:
            verStr = "windows vista"; # or 2008
        elif os.dwMajorVersion>=0:
            verStr = "windows 7";
        else:
            verStr = "unknown version";
    else:
        return "unknown Version";
    return verStr+" build"+str(os.dwBuildNumber)+" "+ctypes.string_at(os.szCSDVersion);

if __name__ == "__main__":
    print(GetSystemVersionString());
