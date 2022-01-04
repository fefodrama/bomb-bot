# -*- coding: utf-8 -*-    
from cv2 import cv2

from os import listdir
from src.logger import logger, loggerMapClicked
from random import randint
from random import random

import numpy as np
import mss
import pyautogui
import time
import sys

import yaml


cat = """
=========================================================================
====================== foda-se ==========================================
============== agora tá funcionando =====================================
=========================================================================


>>---> Dá CTRL + C para parar o BOT

>>---> As configurações podem ser encontradas no arquivo config.yaml."""


print(cat)
#time.sleep(4)


#if __name__ == '__main__': # mudado por ser importado como function - 
if True:
    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)

ct = c['threshold']
ch = c['home']

if not ch['enable']:
    print('>>---> Casa não ativada\
        \n>>---> se fode aí pobre kkk')
print('\n')

pause = c['time_intervals']['interval_between_moviments']
pyautogui.PAUSE = pause

pyautogui.FAILSAFE = False
hero_clicks = 0
login_attempts = 0
last_log_is_progress = False


def addRandomness(n, random_factor_size=None):
    if random_factor_size is None:
        randomness_percentage = 0.1
        random_factor_size = randomness_percentage * n

    random_factor = 2 * random() * random_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - random_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    # logger('{} with randomness -> {}'.format(int(n), randomized_n))
    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images():
    file_names = listdir('./targets/')
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets

images = load_images()


def loadHeroesToSendHome():
    file_names = listdir('./targets/heroes-to-send-home')
    heroes = []
    for file in file_names:
        path = './targets/heroes-to-send-home/' + file
        heroes.append(cv2.imread(path))

    print('>>---> %d heroes that should be sent home loaded' % len(heroes))
    return heroes

if ch['enable']:
    home_heroes = loadHeroesToSendHome()

# go_work_img = cv2.imread('targets/go-work.png')
# commom_img = cv2.imread('targets/commom-text.png')
# arrow_img = cv2.imread('targets/go-back-arrow.png')
# hero_img = cv2.imread('targets/hero-icon.png')
# x_button_img = cv2.imread('targets/x.png')
# teasureHunt_icon_img = cv2.imread('targets/treasure-hunt-icon.png')
# ok_btn_img = cv2.imread('targets/ok.png')
# connect_wallet_btn_img = cv2.imread('targets/connect-wallet.png')
# select_wallet_hover_img = cv2.imread('targets/select-wallet-1-hover.png')
# select_metamask_no_hover_img = cv2.imread('targets/select-wallet-1-no-hover.png')
# sign_btn_img = cv2.imread('targets/select-wallet-2.png')
# new_map_btn_img = cv2.imread('targets/new-map.png')
# green_bar = cv2.imread('targets/green-bar.png')
full_stamina = cv2.imread('targets/full-stamina.png')

robot = cv2.imread('targets/robot.png')
# puzzle_img = cv2.imread('targets/puzzle.png')
# piece = cv2.imread('targets/piece.png')
slider = cv2.imread('targets/slider.png')



def show(rectangles, img = None):

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)


def clickBtn(img,name=None, timeout=3, threshold = ct['default']):
    logger(None, progress_indicator=True)
    if not name is None:
        pass
        # print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    while(True):
        matches = positions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass
                    # print('timed out')
                return False
            # print('botão não encontrado')
            continue

        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        # mudar moveto pra w randomness
        moveToWithRandomness(pos_click_x,pos_click_y,0.1)
        pyautogui.click()
        return True
        print("THIS SHOULD NOT PRINT")

def printScreen(filename = None):
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img_pure = sct.grab(monitor)
        sct_img = np.array(sct_img_pure)
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}
        # Grab the data
        if filename is not None:
            output = "./logs/screenshots/" + filename
            # Save to the picture file
            mss.tools.to_png(sct_img_pure.rgb, sct_img_pure.size, output=output)
        return sct_img[:,:,:3]

def saveChestValue(filename):
    if clickBtn(images['chest']):
        time.sleep(1)
        printScreen(filename)
        time.sleep(1)
        clickBtn(images['x'])
        return "./logs/screenshots/" + filename
    else:
        return "fail"

def positions(target, threshold=ct['default'],img = None):
    if img is None:
        img = printScreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll():

    commoms = positions(images['commom-text'], threshold = ct['commom'])
    if (len(commoms) == 0):
        return
    x,y,w,h = commoms[len(commoms)-1]
#
    moveToWithRandomness(x,y,0.1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0,-c['click_and_drag_amount'],duration=1, button='left')


def clickButtons(acc):
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    if len(buttons) == 0:
        buttons = positions(images['go-work-pt'], threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x+(w/2),y+(h/2),0.1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold - acc %d' % acc)
            return
    return len(buttons)

def isHome(hero, buttons):
    y = hero[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            # if send-home button exists, the hero is not home
            return False
    return True

def isWorking(bar, buttons):
    y = bar[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True

def clickGreenBarButtons(acc):
    # ele clica em quem tá trabalhando, mas acho q não importa
    offset = 130

    green_bars = positions(images['green-bar'], threshold=ct['green_bar'])
    logger('🟩 %d green bars detected - acc %d' % (len(green_bars),acc))
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    if len(buttons) == 0:
        buttons = positions(images['go-work-pt'], threshold=ct['go_to_work_btn'])
    logger('🆗 %d buttons detected - acc %d' % (len(buttons),acc))


    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger('🆗 %d buttons with green bar detected - acc %d' % (len(not_working_green_bars),acc))
        logger('👆 Clicking in %d heroes - acc %d' % (len(not_working_green_bars),acc))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        moveToWithRandomness(x+offset+(w/2),y+(h/2),0.1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        if hero_clicks > 15:
            logger('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold - acc %d' % acc)
            return
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)

def clickFullBarButtons(acc):
    offset = 100
    full_bars = positions(images['full-stamina'], threshold=ct['default'])
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    if len(buttons) == 0:
        buttons = positions(images['go-work-pt'], threshold=ct['go_to_work_btn'])

    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        logger('👆 Clicking in %d heroes - acc %d' % (len(not_working_full_bars),acc))

    for (x, y, w, h) in not_working_full_bars:
        moveToWithRandomness(x+offset+(w/2),y+(h/2),0.1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1

    return len(not_working_full_bars)

def goToHeroes():
    if clickBtn(images['go-back-arrow']):
        global login_attempts
        login_attempts = 0
    #solveCaptcha(pause) # CAPTCHA HAS BEEN REMOVED -
    #TODO tirar o sleep quando colocar o pulling
    #time.sleep(1)
    found = clickBtn(images['hero-icon'])
    #time.sleep(1)
    #solveCaptcha(pause) # CAPTCHA HAS BEEN REMOVED - 
    return found

def goToGame():
    # in case of server overload popup
    clickBtn(images['x'])
    # time.sleep(3)
    clickBtn(images['x'])

    found = clickBtn(images['treasure-hunt-icon'])
    return found

def refreshHeroesPositions(acc):

    logger('🔃 Refreshing Heroes Positions - acc %d' % acc)
    clickBtn(images['go-back-arrow'])
    clickBtn(images['treasure-hunt-icon'])

    # time.sleep(3)
    clickBtn(images['treasure-hunt-icon'])

def login(acc):
    global login_attempts
    logger('😿 Checking if game has disconnected - acc %d' % acc)

    if login_attempts > 3:
        logger('🔃 Too many login attempts, refreshing - acc %d' % acc)
        login_attempts = 0
        pyautogui.hotkey('ctrl','f5')
        return

    if clickBtn(images['ok'], name='okBtn'):
        #pass
        time.sleep(15)
        logger('😬 OK button clicked - acc %d' % acc)

    if clickBtn(images['connect-wallet'], name='connectWalletBtn') or clickBtn(images['connect-wallet-pt'], name='connectWalletBtnPt'):
        logger('🎉 Connect wallet button detected, logging in! - acc %d' % acc)
        # CAPTCHA FOI REMOVIDO
        #solveCaptcha(pause)
        login_attempts = login_attempts + 1
        #TODO valor alto ele da erro e valor baixo o botao não abre
        # time.sleep(10)

        if clickBtn(images['select-wallet-2'], name='signBtn', timeout=8) or clickBtn(images['select-wallet-2-pt'], name='signBtnPt', timeout=8):
            # sometimes the sign popup appears imediately
            login_attempts = login_attempts + 1
            # print('sign button clicked')
            # print('{} login attempt'.format(login_attempts))
            if clickBtn(images['treasure-hunt-icon'], name='teasureHunt', timeout = 15):
                # print('sucessfully login, treasure hunt btn clicked')
                login_attempts = 0
            return
            # click ok button

        if not clickBtn(images['select-wallet-1-no-hover'], name='selectMetamaskBtn'):
            if clickBtn(images['select-wallet-1-hover'], name='selectMetamaskHoverBtn', threshold  = ct['select_wallet_buttons'] ):
                pass
                # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo 
                # print('sleep in case there is no metamask text removed')
                # time.sleep(20)
        else:
            pass
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)

        if clickBtn(images['select-wallet-2'], name='signBtn', timeout = 20) or clickBtn(images['select-wallet-2-pt'], name='signBtnPt', timeout = 20):
            login_attempts = login_attempts + 1
            # print('sign button clicked')
            # print('{} login attempt'.format(login_attempts))
            # time.sleep(25)
            if clickBtn(images['treasure-hunt-icon'], name='teasureHunt', timeout=25):
                # print('sucessfully login, treasure hunt btn clicked')
                login_attempts = 0
            # time.sleep(15)

def sendHeroesHome():
    if not ch['enable']:
        return
    heroes_positions = []
    for hero in home_heroes:
        hero_positions = positions(hero, threshold=ch['hero_threshold'])
        if not len (hero_positions) == 0:
            #TODO maybe pick up match with most wheight instead of first
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print('No heroes that should be sent home found.')
        return
    print(' %d heroes that should be sent home found' % n)
    # if send-home button exists, the hero is not home
    go_home_buttons = positions(images['send-home'], threshold=ch['home_button_threshold'])
    # TODO pass it as an argument for both this and the other function that uses it
    go_work_buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    if len(go_work_buttons) == 0:
        go_work_buttons = positions(images['go-work-pt'], threshold=ct['go_to_work_btn'])

    for position in heroes_positions:
        if not isHome(position,go_home_buttons):
            print(isWorking(position, go_work_buttons))
            if(not isWorking(position, go_work_buttons)):
                print ('hero not working, sending him home')
                moveToWithRandomness(go_home_buttons[0][0]+go_home_buttons[0][2]/2,position[1]+position[3]/2,0.1)
                pyautogui.click()
            else:
                print ('hero working, not sending him home(no dark work button)')
        else:
            print('hero already home, or home full(no dark home button)')


def refreshHeroes(acc):
    logger('🏢 Search for heroes to work - acc %d' % acc)

    found = goToHeroes()
    if not found:
        return False

    if c['select_heroes_mode'] == "full":
        logger('⚒️ Sending heroes with full stamina bar to work - acc %d' % acc, 'green')
    elif c['select_heroes_mode'] == "green":
        logger('⚒️ Sending heroes with green stamina bar to work - acc %d' % acc, 'green')
    else:
        logger('⚒️ Sending all heroes to work - acc %d' % acc, 'green')

    buttonsClicked = 1
    global hero_clicks 
    hero_clicks = 0 # this was missing here, so it was adding up heroes clicks to the infinity - 
    empty_scrolls_attempts = c['scroll_attemps']

    while(empty_scrolls_attempts >= 0): # changed to greater of equal so it checks for heroes one more time after last scroll
        if c['select_heroes_mode'] == 'full':
            buttonsClicked = clickFullBarButtons(acc)
        elif c['select_heroes_mode'] == 'green':
            buttonsClicked = clickGreenBarButtons(acc)
        else:
            buttonsClicked = clickButtons(acc)

        sendHeroesHome()

        if empty_scrolls_attempts > 0: # only scrolls if number of scrolls is greater than 0 - 
            scroll()
        
        #if buttonsClicked == 0: #not sure why we need this? - 
        if True:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
        time.sleep(1) #reduced from 2 to 1 as this part takes too long.. - 
    logger('💪 %d heroes sent to work - acc %d' % (hero_clicks, acc))
    returned = goToGame()
    if returned:
        return True
    else:
        return False


def main():
    time.sleep(5)
    t = c['time_intervals']

    last = {
    "login" : 0,
    "heroes" : 0,
    "new_map" : 0,
    "check_for_captcha" : 0,
    "refresh_heroes" : 0
    }

    while True:
        now = time.time()

        if now - last["check_for_captcha"] > addRandomness(t['check_for_captcha'] * 60):
            last["check_for_captcha"] = now
            solveCaptcha(pause)

        if now - last["heroes"] > addRandomness(t['send_heroes_for_work'] * 60):
            last["heroes"] = now
            refreshHeroes(0)

        if now - last["login"] > addRandomness(t['check_for_login'] * 60):
            sys.stdout.flush()
            last["login"] = now
            login()

        if now - last["new_map"] > t['check_for_new_map_button']:
            last["new_map"] = now

            if clickBtn(images['new-map']):
                loggerMapClicked()


        if now - last["refresh_heroes"] > addRandomness( t['refresh_heroes_positions'] * 60):
            solveCaptcha(pause)
            last["refresh_heroes"] = now
            refreshHeroesPositions(0)

        #clickBtn(teasureHunt)
        logger(None, progress_indicator=True)

        sys.stdout.flush()

        time.sleep(1)



#main() # Commented this as I'm now importing this file as a function file - 


#cv2.imshow('img',sct_img)
#cv2.waitKey()

# colocar o botao em pt
# soh resetar posiçoes se n tiver clickado em newmap em x segundos


