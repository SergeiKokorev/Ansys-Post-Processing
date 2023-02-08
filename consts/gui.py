import ctypes

USER32 = ctypes.windll.user32

SCREEN_SIZE = [USER32.GetSystemMetrics(0)/2, USER32.GetSystemMetrics(1)/2]
QTABS = ["Expressions", "PerformanceMaps", "UserSurfaces"]

QTABBFONT = ['Calibri', 12]
QLISTFONT = ['Calibri', 12]
