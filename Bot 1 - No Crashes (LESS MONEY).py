import mss
import numpy as np
import keyboard
import time
import pyautogui
import cv2

subtract = 0
count = 0
direction = True  
moveCount = 0
offset_x = 0
offset_y = 0

TemplateLobbyScreen = cv2.imread("templates/CartSurferLobbyScreen.png", cv2.IMREAD_GRAYSCALE)
if TemplateLobbyScreen is None:
    raise FileNotFoundError("CartSurferLobbyScreen.png not found")
TemplateEndScreen = cv2.imread("templates/EndGameScreen.png", cv2.IMREAD_GRAYSCALE)
if TemplateEndScreen is None:
    raise FileNotFoundError("EndGameScreen.png not found")


#pyautogui.click(offset_x + lx, offset_y + ly)

def imageScan(sct):
    global offset_x, offset_y

    for monitor in sct.monitors[1:]:
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = img[:, :, :3]
        img = img[:, :, ::-1]

        #Find Club Penguin
        matches = (img[:,:,0] == 34) & (img[:,:,1] == 164) & (img[:,:,2] == 243)
    
        #If no game found then:
        if np.any(matches) == False :
            continue
    
        # Get coordinates of all matching pixels
        ys, xs = np.where(matches)

        # Top-left and bottom-right
        x1, y1 = xs.min(), ys.min()
        x2, y2 = xs.max(), ys.max()

        # Offset
        offset_x = monitor['left']
        offset_y = monitor['top']

        mid_x = round((x1+x2)/2)
        mid_y = round((y1+y2)/2)

        mid_y = img.shape[0] // 2
        mid_x = img.shape[1] // 2
        Crop_y1, Crop_y2, Crop_x1, Crop_x2 = 0, 0, 0, 0

        # Finding Club Penguin BOX

        # Blue Colour One CROP!

        if np.any((img[:,:,0] == 34) & (img[:,:,1] == 164) & (img[:,:,2] == 243)):
            while not ((img[mid_y-Crop_y1, mid_x, 0] == 34) & (img[mid_y-Crop_y1, mid_x, 1] == 164) & (img[mid_y-Crop_y1, mid_x, 2] == 243)) :
                Crop_y1 += 1
            Crop_y1 = mid_y - Crop_y1

            while not ((img[mid_y+Crop_y2, mid_x, 0] == 34) & (img[mid_y+Crop_y2, mid_x, 1] == 164) & (img[mid_y+Crop_y2, mid_x, 2] == 243)):
                Crop_y2 += 1
            Crop_y2 = mid_y + Crop_y2

            while not ((img[mid_y, mid_x-Crop_x1, 0] == 34) & (img[mid_y, mid_x-Crop_x1, 1] == 164) & (img[mid_y, mid_x-Crop_x1, 2] == 243)):
                Crop_x1 += 1
            Crop_x1 = mid_x - Crop_x1

            while not ((img[mid_y, mid_x+Crop_x2, 0] == 34) & (img[mid_y, mid_x+Crop_x2, 1] == 164) & (img[mid_y, mid_x+Crop_x2, 2] == 243)):
                Crop_x2 += 1
            Crop_x2 = mid_x + Crop_x2

            img = img[Crop_y1:Crop_y2, Crop_x1:Crop_x2]
        
        offset_x = offset_x + Crop_x1
        offset_y = offset_y + Crop_y1
        Crop_y1, Crop_y2, Crop_x1, Crop_x2 = 0, 0, 0, 0

        # Blue Colour TWO CROP!
        if np.any((img[:,:,0] == 40) & (img[:,:,1] == 165) & (img[:,:,2] == 250)):
            while not ((img[mid_y-Crop_y1, mid_x, 0] == 40) & (img[mid_y-Crop_y1, mid_x, 1] == 165) & (img[mid_y-Crop_y1, mid_x, 2] == 250)) :
                Crop_y1 += 1

            while not ((img[mid_y+Crop_y2, mid_x, 0] == 40) & (img[mid_y+Crop_y2, mid_x, 1] == 165) & (img[mid_y+Crop_y2, mid_x, 2] == 250)):
                Crop_y2 += 1

            while not ((img[mid_y, mid_x-Crop_x1, 0] == 40) & (img[mid_y, mid_x-Crop_x1, 1] == 165) & (img[mid_y, mid_x-Crop_x1, 2] == 250)):
                Crop_x1 += 1

            while not ((img[mid_y, mid_x+Crop_x2, 0] == 40) & (img[mid_y, mid_x+Crop_x2, 1] == 165) & (img[mid_y, mid_x+Crop_x2, 2] == 250)):
                Crop_x2 += 1
            
            Crop_y1 = mid_y - Crop_y1
            Crop_y2 = mid_y + Crop_y2
            Crop_x1 = mid_x - Crop_x1
            Crop_x2 = mid_x + Crop_x2

            offset_x = offset_x + Crop_x1
            offset_y = offset_y + Crop_y1

            img = img[Crop_y1+1:Crop_y2+1, Crop_x1:Crop_x2]

        return img, True
    return img, False

def signFound(img):
    matches = (img[:,:,0] == 45) & (img[:,:,1] == 36) & (img[:,:,2] == 0)
    return np.any(matches)

def CartSurfGameScreen(img):
    matches = (img[:,:,0] == 117) & (img[:,:,1] == 146) & (img[:,:,2] == 164)
    return np.any(matches)

def CartSurfLobbyScreen(img, TemplateLobbyScreen):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    matchRes = cv2.matchTemplate(gray, TemplateLobbyScreen, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(matchRes)
    return max_val >= 0.45

def InitaliseGame(img):
    print("Clicking to Start MineSurfer")

    height, width = img.shape[:2]
    pyautogui.click(round(offset_x+0.83*width),round(offset_y+0.34*height))
    time.sleep(3.6)
    pyautogui.click(round(offset_x+0.42*width),round(offset_y+0.45*height))
    time.sleep(1)
    pyautogui.click(round(offset_x+0.84*width),round(offset_y+0.78*height))

def EndGameScreen(img, TemplateEndScreen):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    matchRes = cv2.matchTemplate(gray, TemplateEndScreen, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(matchRes)
    return max_val >= 0.45

def RestartGame():
    height, width = img.shape[:2]
    pyautogui.click(round(offset_x+0.70*width),round(offset_y+0.139*height))
    time.sleep(0.3)

def CheckSign(img):
    ## True = right turn approaching
    ## False = left turn approaching
    height, width = img.shape[:2]
    midX = width // 2
    matches = (img[:,:,0] == 45) & (img[:,:,1] == 36) & (img[:,:,2] == 0)
    ys, xs = np.where(matches)
    if xs[0] < midX:
        print("Right Turn Approaching!")
        return True
    else:
        print("Left Turn Approaching!")
        return False


def GrindRight():
    print("Grinding Right")
    keyboard.press('down')
    time.sleep(0.1)
    keyboard.press('right')
    time.sleep(1.2)
    keyboard.release('down')
    keyboard.release('right')

def GrindLeft():
    print("Grinding Left")
    keyboard.press('down')
    time.sleep(0.1)
    keyboard.press('left')
    time.sleep(1.2)
    keyboard.release('down')
    keyboard.release('left')
    
def BackFlip(sct):
    global count
    global direction
    global subtract
    count = 0
    print("BackFlip")
    keyboard.press_and_release('down')
    time.sleep(0.1 )
    keyboard.press_and_release('space')
    start_time = time.time()
    while time.time() - start_time < 0.5:
        img, gameFound = imageScan(sct)
        if signFound(img):
            count = count + 1
            subtract = 0.1*count-0.2
            if CheckSign(img):
                direction = True
            else:
                direction = False
        time.sleep(0.001)

    if count == 0 :
        time.sleep(0.5)

def SideFlip(sct):
    global count
    global direction
    global subtract
    count = 0
    print("SideFlip")
    keyboard.press_and_release('space')
    time.sleep(0.1)
    keyboard.press_and_release('right')
    start_time = time.time()
    while time.time() - start_time < 0.5:
        img, gameFound = imageScan(sct)
        if signFound(img):
            if count != 4:
                count = count + 1
            subtract = 0.2*count-0.2
            if count == 4:
                subtract = subtract + 0.1
            if CheckSign(img):  
                direction = True
            else:
                direction = False
        time.sleep(0.001)

    if count == 0 :
        time.sleep(0.2)


def MakeMove(sct):
    global moveCount
    if moveCount % 2 == 1  :
        BackFlip(sct)
    else :
        SideFlip(sct)
    moveCount = moveCount + 1


with mss.mss() as sct:
    print("Hold 'M' to start scanning. Hold 'Q' to stop scanning. Press 'ESC' to terminate the program.")
    while True:
        if keyboard.is_pressed('m'):
            while True:  # Outer loop listens for key presses
                img, gameFound = imageScan(sct)  # Take a screenshot every loop
                if not gameFound or img is None or img.size == 0 :
                    print("Club Penguin not detected")
                else : 
                    # Only check sign if the game screen is detected
                    if CartSurfGameScreen(img):

                        # If sign was detected during a Flip, it reduces cooldown to compensate
                        if count > 0:
                            count = 0
                            if subtract <= 1.2:
                                time.sleep(1.2-subtract)
                            if direction:
                                GrindRight()
                            else:
                                GrindLeft()

                        # If sign detected normally, it flips!
                        elif signFound(img):
                            time.sleep(0.9)
                            if CheckSign(img):
                                GrindRight()
                            else:
                                GrindLeft()
                        else:
                            MakeMove(sct)

                        

                    # Check if player is in Lobby Screen
                    elif CartSurfLobbyScreen(img, TemplateLobbyScreen):
                        print("Cart Surfer Lobby Found!")
                        InitaliseGame(img)
                    elif EndGameScreen(img, TemplateEndScreen):
                        print("Game Finished! Restarting!")
                        RestartGame()
                    else:
                        print("Cart Surfer not found")

                time.sleep(0.005)
                # Stop scanning if Q is pressed 
                if keyboard.is_pressed('q'): 
                    print("Scanning stopped. Press 'M' to start again. Press 'ESC' to terminate the program.") 
                    break
                if keyboard.is_pressed('esc'):
                    print("Terminating...")
                    exit()
        if keyboard.is_pressed('esc'):
            print("Terminating...")
            exit()


