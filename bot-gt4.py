import time
import win32gui
import win32api
import win32con
import pyautogui
import cv2
import numpy as np
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#codeliste für tastensimulation
VK_CODE = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift ':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0}

def _get_windows_bytitle(title_text, exact = False):
    def _window_callback(hwnd, all_windows):
        all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    windows = []
    win32gui.EnumWindows(_window_callback, windows)
    if exact:
        return [hwnd for hwnd, title in windows if title_text == title]
    else:
        return [hwnd for hwnd, title in windows if title_text in title]


def shot():
	#sucht das fenster nach dem namen, holt es in den vordergrund
	#macht einen screenshot und schneidet den auf die größe des fenster zu.
	hwnd = _get_windows_bytitle('Gran Turismo 4')
	win32gui.SetForegroundWindow(hwnd[0])#17765310
	l,t,r,b=win32gui.GetWindowRect(hwnd[0])
	time.sleep(0.2)
	image = pyautogui.screenshot('screen.png', region=(l,t,r-l,b-t))
	time.sleep(0.5)

def pic_search(pic):
	#ein bildausschnitt wird im screenshot gesucht und zurückgegeben
	#ob sich der bildausschnitt im screenshot befindet.
	#öffnen beider bilder
	screenshot = cv2.imread('screen.png')
	template = cv2.imread(pic)
	
	#prüfen ob es im bild vorhanden ist
	result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
	
	#schwellwert für die erkennung
	threshold = 0.925
	locations = np.where(result >= threshold)

	#wenn es erkannt wurde wird True zurückgegeben
	if len(locations[0]) > 0:
		return True
	else:
		return False

def keypress(key):
	#simulieren eines tastenfdrucks
	win32api.keybd_event(VK_CODE[key], 0,0,0)
	time.sleep(.05)
	win32api.keybd_event(VK_CODE[key],0 ,win32con.KEYEVENTF_KEYUP ,0)
	time.sleep(1)

#eingabe der vorhandenen credits
cr_old = input("Credits:")
if cr_old == "":
	cr_old = 0
else:
	cr_old = int(cr_old)

#eingabe ob A-Spec oder B-Spec
spec = input("A oder B-Spec:")

#3 sekunden warten bevor das fenster in den vordergrund geholt wird
time.sleep(3)
hwnd = _get_windows_bytitle('Gran Turismo 4')
win32gui.SetForegroundWindow(hwnd[0])

cr_n = 0
cr_p_min_total = 0


#endlosschleife 
while True:
	#zeitstempel speichern
	start = time.time()
	#screenshot
	shot()
	#prüfen ob man im rennmenü oder hauptmenü ist
	res = pic_search("race.png")
	if res == False:
		print ("Hauptmenü")
		keypress("k")
		keypress("k")
		time.sleep(10)
	else:
		print ("Spielmenü")
		time.sleep(4)
	
	#im rennmenü auswählen ob A-Spec oder B-Spec
	if spec == "A":
		print ("A-Spec")
		keypress("k")
	elif spec == "B":
		print ("B-Spec")
		keypress("d")#fuer b-spec
		keypress("k")
		time.sleep(5)
		keypress("i")
	
	#endlosschleife ob das rennen noch läuft
	while True:
		shot()
		res = pic_search("seiko.png")
		if res == True:
			#print ("rennen ende")
			time.sleep(3)
			keypress("k")
			time.sleep(1)
			keypress("enter")
			#print ("seiko")
			break
		time.sleep(10.2)
	
	#endlosscheife ob die gewonnen credits gebucht wurden
	#außerdem wird neuer kontostand aus dem screenshot ausgelesen
	#mit tesseract
	while True:
		shot()
		res = pic_search("ok.png")
		if res == True:
			#print ("rennen ende")
			image_path = 'screen.png'
			image = cv2.imread(image_path)
			x, y, w, h = 924, 728, 440, 49
			cropped_image = image[y:y+h, x:x+w]
			gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
			thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
			text = pytesseract.image_to_string(thresh, lang='eng')
			replaces = ["Cr.", ",", "\n", " ", "#"]
			for r in replaces:
				text = text.replace(r, "")
			cr_new = int(text)
			keypress("k")
			time.sleep(1)
			break
		time.sleep(10.1)
	keypress("k")
	time.sleep(2)
	#zweiten zeitstempel speichern
	ende = time.time()
	
	#berechnen wie viel credits man pro minute gewonnen hat.
	if cr_old > 0:
		cr_n += 1
		cr_win = cr_new - cr_old
		cr_p_min = cr_win/((ende-start)/60)
		cr_p_min_total += cr_p_min
		print ("Cr/Min:", round(cr_p_min))
		print ("avg:", round(cr_p_min_total/cr_n))
		print ("---")
	cr_old = cr_new
