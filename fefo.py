from index import *

import pygetwindow

from src.logger import sendTelegramLog, sendTelegramImg, logger
from src.date import dateFormatted

#                    AGORA FUNCIONA ESSA PORRA AÍ 
#=========================================================================
#====================== foda-seeeeeeeeeeeeeeeeeeeeeeeeeeee ===============
#=========================================================================
#=========================================================================

captcha = False # mudar pra true se adicionarem captcha novamente - 

def mainfefo():
    
    t = c['time_intervals']

    last = {
    "login" : 0,
    "heroes" : 0,
    "new_map" : 0,
    "check_for_captcha" : 0,
    "refresh_heroes" : 0,
    "telegram_sent" : 0
    }
    lasttelegram = dateFormatted()
    logger("INICIANDO...")

    accounts = []
    multiacc = True
    for acc in pygetwindow.getWindowsWithTitle('Bombcrypto - Google Chrome'):
        accounts.append(acc)
    if len(accounts) == 0:
        print("Nenhuma janela do Bombcrypto foi encontrada no Google Chrome! Iniciando modo de conta única...\
            \nAbra a janela do jogo manualmente agora.") #
        i=0
        time.sleep(5)
        multiacc = False
    else:
        print("Número de Janelas do Bombcrypto encontradas:", len(accounts))
        time.sleep(2)
    
    while True:

        now = time.time()

        if now - last["check_for_captcha"] > addRandomness(t['check_for_captcha'] * 60) and captcha:
            if multiacc:
                i=1
                for acc in accounts:
                    acc.activate()
                    time.sleep(1)
                    solveCaptcha(pause)
                    i=i+1
            else:
                solveCaptcha(pause)
            last["check_for_captcha"] = now

        if now - last["login"] > addRandomness(t['check_for_login'] * 60):
            if multiacc:
                i=1
                for acc in accounts:
                    acc.activate()
                    time.sleep(1)
                    login(i)
                    i=i+1
            else:
                login(i)
            sys.stdout.flush()
            last["login"] = now

        if now - last["heroes"] > addRandomness(t['send_heroes_for_work'] * 60):
            if multiacc:
                i=1
                for acc in accounts:
                    acc.activate()
                    time.sleep(1)
                    result = refreshHeroes(i)
                    i=i+1
            else:
                result = refreshHeroes(i)
            if result:
                last["heroes"] = now
                last["refresh_heroes"] = now # sem necessidade de refresh de posição dos heróis se eles foram trampar agora - 

        if now - last["new_map"] > t['check_for_new_map_button']:
            if multiacc:
                i=1
                for acc in accounts:
                    acc.activate()
                    time.sleep(1)
                    if clickBtn(images['new-map']) or clickBtn(images['new-map-pt']):
                        logger("Finished a map! - acc %d" % i)
                        loggerMapClicked()
                        last["refresh_heroes"] = now # sem necessidade de refresh de posição dos heróis se eles acabaram de entrar em um mapa novo - 
                    i=i+1
            else:
                if clickBtn(images['new-map']) or clickBtn(images['new-map-pt']):
                    logger("Finished a map!")
                    loggerMapClicked()
                    last["refresh_heroes"] = now # sem necessidade de refresh de posição dos heróis se eles acabaram de entrar em um mapa novo - 
            last["new_map"] = now

        if now - last["refresh_heroes"] > addRandomness( t['refresh_heroes_positions'] * 60):
            if multiacc:
                i=1
                for acc in accounts:
                    acc.activate()
                    time.sleep(1)
                    if captcha: # CAPTCHA HAS BEEN REMOVED - 
                        solveCaptcha(pause)
                    refreshHeroesPositions(i)
                    i=i+1
            else:
                if captcha: # CAPTCHA HAS BEEN REMOVED - 
                    solveCaptcha(pause)
                refreshHeroesPositions(i) 
            last["refresh_heroes"] = now

        if (now - last["telegram_sent"] > (t['send_telegram_time'] * 60)) and (c['send_telegram_log'] or c['telegram_send_chest']):
            if c['send_telegram_log']:
                sendTelegramLog(lasttelegram)
            if c['telegram_send_chest']:
                if multiacc:
                    i=1
                    for acc in accounts:
                        acc.activate()
                        time.sleep(1)
                        img = saveChestValue(dateFormatted('%d-%m-%Y_%H-%M-%S') + '_acc%d.png' % i)
                        if img.endswith('.png'):
                            sendTelegramImg(img, "acc %d" % i)
                        i=i+1
                else:
                    img = saveChestValue(dateFormatted('%d-%m-%Y_%H-%M-%S') + '.png')
                    if img.endswith('.png'):
                        sendTelegramImg(img)
            lasttelegram = dateFormatted()
            logger("Telegram Sent!")
            last["telegram_sent"] = now

        #clickBtn(teasureHunt)
        logger(None, progress_indicator=True)
        sys.stdout.flush()
        time.sleep(1)


#main()
while 1:
    try:
        mainfefo()
    except KeyboardInterrupt:
        answer = input("\nDeseja parar o bot? (y/N) ")
        if answer == 'y' or answer == 'Y':
            sys.exit()
        else:
            continue
    except Exception as e:
        logger(e)
        continue
