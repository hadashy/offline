import time
import pyautogui
import win32clipboard
import win32con
import win32gui
from pywinauto import application


calc_data = dict(
    program_path=r'C:\Windows\System32\calc.exe',
    digit='5',
    operator='+',
    calc_result='10',

)

pyautogui.PAUSE = 0.2


def open_program(program_path: str) -> None:
    app = application.Application()
    app.start(program_path)
    time.sleep(2)
    maxi = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(maxi, win32con.SW_MAXIMIZE)


def calculate() -> None:
    pyautogui.press(calc_data['digit'])
    pyautogui.press(calc_data['operator'])
    pyautogui.press(calc_data['digit'])
    pyautogui.press('enter')
    pyautogui.screenshot('screenshots/calc_screenshot.png')


def close_program() -> None:
    pyautogui.press('escape')
    pyautogui.hotkey('alt', 'f4')


def validate_result() -> None:
    open_program(calc_data['program_path'])
    calculate()
    pyautogui.doubleClick(pyautogui.position(1550, 165))
    pyautogui.hotkey('ctrl', 'c')
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    assert data == calc_data['calc_result'], "Calculator result wasn't expected"


def err() -> None:
    assert 3 == 4, "Result wasn't expected"
