Der Bot wiederholt in einer Endlosschleife ein ausgewähltes Rennen. Mit Hilfe von cv2 wird werden Bilder in Screenshots gesucht, mit verschiedenen win32-modulen werden die Screenshots erstellen und Tastendruck simuliert. Außerdem wird mit Tesseract nach jedem Rennen der Kontostand aus dem Screenshot ausgelesen und berechnet wie viele Credits man pro Minute effektiv gewonnen hat.

benötigt wird:
win32gui. win32api, win32con, pyautogui, cv2, numpy, pytesseract, PIL und tesseract.
