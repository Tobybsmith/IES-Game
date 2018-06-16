#import here:
import pygame
import random
import math
import time
import sys
from pygame.locals import *

pygame.init()

fps = pygame.time.Clock()

moonwalk = False
bh = False
done = False
suddendeath = False
ai = False

while not done:
    code = raw_input("Input a cheat code, type done or leave blank when done:")
    if code == "moonwalk" or code == "mw":
        moonwalk = True
    if code == "big head" or code == "bh":
        bh = True
    if code == "done" or code == "":
        done = True
    if code == "sd" or code == "sudden death":
        suddendeath = True
    if code == "rob" or code == "robot" or code == "codsworth" or code == "skynet" or code == "ai" or code == "singleplayer" or code == "single" or code == "1" or code == "c3po" or code == "r2d2":
        ai = True

#screen
(width, height) = (1360, 736)
reschange = raw_input("Do you want to change game's resolution?")
if reschange == "yes" or reschange == "y":
    width = input("screen width")
    height = input("screen height")
screen = pygame.display.set_mode((width, height))

#colors
#randomly generated, but with lighter background
groundgreyrand1 = random.randint(60,120)
groundgreyrand2 = random.randint(40,60)
groundgreyrand3 = random.randint(60,120)
groundgrey = (groundgreyrand2,groundgreyrand2,groundgreyrand3)

backgroundgreyrand1 = groundgreyrand1 + random.randint(40,135)
backgroundgreyrand2 = groundgreyrand2 + random.randint(40,135)
backgroundgreyrand3 = groundgreyrand3 + random.randint(40,135)
backgroundgrey = (backgroundgreyrand1,backgroundgreyrand2,backgroundgreyrand3)
backgroundgreyavg = (backgroundgreyrand1 + backgroundgreyrand2 + backgroundgreyrand3)/3

barback = (96, 96, 96)
barout = (160, 160, 160)
healthbar = (255, 51, 51)
shieldbar = (51, 153, 255)
snipershot = (0, 255, 0)
#tracer = (186, 186, 186)
if backgroundgreyavg >= 166 and backgroundgreyavg <= 206:
    tracer = (0, 0, 0)
else:
    tracer = (186, 186, 186)
#generate random terrain
ground = []
x = 1
y = random.randint(200, 400)
while x<(width + 200):
    #this is where it makes the randomly generated terrain
    direction=random.randint(-1,1)
    flat = random.randint(1,10)
    if flat == 10:
        direction = 0
    length=random.randint(20,80)
    end=x+length
    for z in range(x,end):
        add=random.randint(0,2)
        y=y+direction*add
        if y < height - 600:
            y = height - 600
        if y > 500:
            y = 500
        #puts where the ground is into the list ground
        ground.append(y)
    x=x+length

#spritesheet code
class spritesheet:
	def __init__(self, filename, cols, rows):
		self.sheet = pygame.image.load(filename).convert_alpha()
		
		self.cols = cols
		self.rows = rows
		self.totalCellCount = cols * rows
		
		self.rect = self.sheet.get_rect()
		w = self.cellWidth = self.rect.width / cols
		h = self.cellHeight = self.rect.height / rows
		hw, hh = self.cellCenter = (w / 2, h / 2)
		
		self.cells = list([(index % cols * w, index / cols * h, w, h) for index in range(self.totalCellCount)])
		self.handle = list([
			(0, 0), (-hw, 0), (-w, 0),
			(0, -hh), (-hw, -hh), (-w, -hh),
			(0, -h), (-hw, -h), (-w, -h),])
		
	def draw(self, surface, cellIndex, x, y, handle = 0):
		surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellIndex])

#variables for player
#player 1
play1x = 50 #player x value
play1y = 0 #player y value
play1lr = "r" #direction player is pointing
walking1 = False #is player walking?
walk1frame = 0 #which walking frame
framecount1 = 0 #ticker so frame doesn't change every frame
frame1 = 0 #final calculation of frame
#
shooting1 = False #is player shooting any weapon
shootingwep1 = 0 #which weapon is player shooting
wepframe1 = 0 #frame of weapon animation
wepphase1 = 0 #phase, so weapons can go back
mortarshot1 = False
#
mortarx1 = 0 #mortar x coordinate
mortary1 = 0 #mortar y coordinate
mortarchange1 = 0 #mortar change, for arch
mortardirection1 = 0 #mortar direction
play1health = 100 #player health
sniperx1 = 0 #Sniper laser x value
snipery1 = 0 #Sniper laser y value
underground1 = False #checks if sniper shot was underground
#
arb1x1 = 0 #player 1 bullet 1 x
arb1y1 = 0 #player 1 bullet 1 y
arb1x2 = 0 #player 1 bullet 2 x
arb1y2 = 0 #player 1 bullet 2 y
arb1x3 = 0 #player 1 bullet 3 x
arb1y3 = 0 #player 1 bullet 3 y
arshot11 = False #if bullets have been shot
arshot12 = False
arshot13 = False
bulletspread1 = 0 #bullet spread
arb11 = 0 #counter so bullets stay for a little more
arb12 = 0
arb13 = 0
arb1x1f = 0 #held values
arb1y1f = 0 #
arb1x2f = 0 #
arb1y2f = 0 #
arb1x3f = 0 #
arb1y3f = 0 #
#
shield1 = 60 #amount of shields
shielded1 = False #is shield up, prevents damage
shielddelay1 = 0 #delays shield regen after use
#
mortarexploded1 = False
mortarexplodedframe1 = 0

#player 2
play2x = width - 50
play2y = 0
play2lr = "l"
walking2 = False
walk2frame = 0
framecount2 = 0
frame2 = 0
#
shooting2 = False
shootingwep2 = 0
wepframe2 = 0
wepphase2 = 0
mortarshot2 = False
#
mortarx2 = 0
mortary2 = 0
mortarchange2 = 0
mortardirection2 = 0
play2health = 100
sniperx2 = 0
snipery2 = 0
underground2 = False
#
arb2x1 = 0
arb2y1 = 0
arb2x2 = 0
arb2y2 = 0
arb2x3 = 0
arb2y3 = 0
arshot21 = False
arshot22 = False
arshot23 = False
bulletspread2 = 0
arb21 = 0
arb22 = 0
arb23 = 0
arb2x1f = 0
arb2y1f = 0
arb2x2f = 0
arb2y2f = 0
arb2x3f = 0
arb2y3f = 0
#
shield2 = 60
shielded2 = False
shielddelay2 = 0
#
mortarexploded2 = False
mortarexplodedframe2 = 0
#
underground3 = False #ai checking if it can shoot player 1
randomnumber = 0 #ai random number
bootup = 10 #ai bootup time
firewall = 0 #ai shield time (randomized)
shellshocked = False #ai running from mortars
shellshockeddir = "l" #direction ai is running
mortarspot = 0 #place mortar will hit
shellshockedish = False #stops ai from running back into mortars

tie = False

#preparation for main loop
running = True
clock = pygame.time.Clock()
pygame.display.set_caption("IES Game")
FPS = 60

#load spritesheet(s)
if not bh:
    walkblue = spritesheet("walk_ani_blu.png", 4, 4)
    walkred = spritesheet("walk_ani_red.png", 4, 4)
    arblue = spritesheet("ar_blu.png", 3, 4)
    arred = spritesheet("ar_red.png", 3, 4)
    mortarblue = spritesheet("mortar_blu.png", 4, 5)
    mortarred = spritesheet("mortar_red.png", 4, 5)
    shieldblue = spritesheet("shield_blu.png", 3, 4)
    shieldred = spritesheet("shield_red.png", 3, 4)
    sniperblue = spritesheet("sniper_blu.png", 3, 4)
    sniperred = spritesheet("sniper_red.png", 3, 4)
    mortar = spritesheet("mortar.png", 2, 3)
else:
    walkblue = spritesheet("walk_ani_blu_bh.png", 4, 4)
    walkred = spritesheet("walk_ani_red_bh.png", 4, 4)
    arblue = spritesheet("ar_blu_bh.png", 3, 4)
    arred = spritesheet("ar_red_bh.png", 3, 4)
    mortarblue = spritesheet("mortar_blu_bh.png", 4, 5)
    mortarred = spritesheet("mortar_red_bh.png", 4, 5)
    shieldblue = spritesheet("shield_blu_bh.png", 3, 4)
    shieldred = spritesheet("shield_red_bh.png", 3, 4)
    sniperblue = spritesheet("sniper_blu_bh.png", 3, 4)
    sniperred = spritesheet("sniper_red_bh.png", 3, 4)
mortar = spritesheet("mortar.png", 2, 3)

#main loop
while running:
    #clear screen and re-fill with background color
    screen.fill(groundgrey)

    #draws sky
    for x in range(1400):
        #REMEMBER: program draws land and then turns chunks of it into the sky
        pygame.draw.rect(screen,backgroundgrey, (x,0,1,ground[x]),0)

    #looks for key inputs
    keystate = pygame.key.get_pressed()

    #weapon inputs
    #if keystate[K_t] and shooting1 == False: #hand rocket
        #shooting1 = True
        #shootingwep1 = 1
        #wepframe1 = 0
        #framecount1 = 0
        #wepphase1 = 0
        #if play1lr == "l":
            #wepframe1 = 9
    if keystate[K_s] and shooting1 == False: #shield
        shooting1 = True
        shootingwep1 = 1
        wepframe1 = 0
        framecount1 = 0
        wepphase1 = 0
        if play1lr == "l":
            wepframe1 = 6
    if keystate[K_f] and shooting1 == False: #sniper rifle
        shooting1 = True
        shootingwep1 = 2
        wepframe1 = 0
        framecount1 = 0
        wepphase1 = 0
        underground1 = False
        if play1lr == "l":
            wepframe1 = 6
    if keystate[K_g] and shooting1 == False and mortarshot1 == False: #mortar
        shooting1 = True
        shootingwep1 = 3
        wepframe1 = 0
        framecount1 = 0
        wepphase1 = 0
        randomnumber = random.randint(1,100)
        if randomnumber <= 50:
            shellshocked = True
            shellshockedish = True
            if play2x - play1x + 600 > 0:
                shellshockeddir = "r"
                mortarspot = play1x + 725
            if play2x - play1x + 600 < 0:
                shellshockeddir = "l"
                mortarspot = play1x + 475
            if play2x - play1x + 600 == 0:
                randomnumber = random.randint(1,100)
                if randomnumber <= 50:
                    shellshockeddir = "l"
                else:
                    shellshockeddir = "r"
        if play1lr == "l":
            wepframe1 = 9
    if keystate[K_h] and shooting1 == False: #assault rifle
        shooting1 = True
        shootingwep1 = 4
        wepframe1 = 0
        framecount1 = 0
        wepphase1 = 0
        underground1 = False
        if play1lr == "l":
            wepframe1 = 6

    #if keystate[K_l] and shooting2 == False: #hand rocket
        #shooting2 = True
        #shootingwep2 = 1
        #wepframe2 = 0
        #framecount2 = 0
        #wepphase2 = 0
        #if play2lr == "l":
            #wepframe2 = 9
    if not ai:
        if keystate[K_DOWN] and shooting2 == False: #shield
            shooting2 = True
            shootingwep2 = 1
            wepframe2 = 0
            framecount2 = 0
            wepphase2 = 0
            if play2lr == "l":
                wepframe2 = 6
        if keystate[K_COMMA] and shooting2 == False: #sniper rifle
            shooting2 = True
            shootingwep2 = 2
            wepframe2 = 0
            framecount2 = 0
            wepphase2 = 0
            underground2 = False
            if play2lr == "l":
                wepframe2 = 6
        if keystate[K_PERIOD] and shooting2 == False and mortarshot2 == False: #mortar
            shooting2 = True
            shootingwep2 = 3
            wepframe2 = 0
            framecount2 = 0
            wepphase2 = 0
            if play2lr == "l":
                wepframe2 = 9
        if keystate[K_SLASH] and shooting2 == False: #assault rifle
            shooting2 = True
            shootingwep2 = 4
            wepframe2 = 0
            framecount2 = 0
            wepphase2 = 0
            underground2 = False
            if play2lr == "l":
                wepframe2 = 6

    #movement inputs
    if shooting1 == False:
        if keystate[K_a] or [K_d]:
            walking1 = True
            if keystate[K_a]:
                play1x = play1x - 8
                if play1x <= 0:
                    play1x = 0
                if not moonwalk:
                    play1lr = "l"
                else:
                    play1lr = "r"
            if keystate[K_d]:
                play1x = play1x + 8
                if play1x >= width:
                    play1x = width
                if not moonwalk:
                    play1lr = "r"
                else:
                    play1lr = "l"
        if keystate[K_a] and keystate[K_d]:
            walking1 = False
    else:
        walking1 = False
    if not keystate[K_a]:
        if not keystate[K_d]:
            walking1 = False
    if not ai:
        if shooting2 == False:
            if keystate[K_LEFT] or [K_RIGHT]:
                walking2 = True
                if keystate[K_LEFT]:
                    play2x = play2x - 8
                    if play2x <= 0:
                        play2x = 0
                    if not moonwalk:
                        play2lr = "l"
                    else:
                        play2lr = "r"
                if keystate[K_RIGHT]:
                    play2x = play2x + 8
                    if play2x >= width:
                        play2x = width
                    if not moonwalk:
                        play2lr = "r"
                    else:
                        play2lr = "l"
            if keystate[K_LEFT] and keystate[K_RIGHT]:
                walking2 = False
        else:
            walking2 = False
        if not keystate[K_LEFT]:
            if not keystate[K_RIGHT]:
                walking2 = False
    #AI DOES THINGS 010101001000101010101010001000101010100001001010000010110101
    #101000101001110100100101001011010000100001010101100001010111000101010010010
    #101010100100000110110111010100010100101000000101010101101011100101010100111
    #010100110111010101000101000010001010100101010101110100101010000010101011100
    #011110101011111101010101001010101010001010011010000111010010010101010101001
    if ai:
        if not shooting2 and bootup <= 0:
            underground3 = False
            for numb in range(play2x + 45, width):
                if play2y - 5 >= ground[numb]:
                    underground3 = True
            if play1y > play2y - 50 and play1y < play2y + 50 and not underground3 and not shellshocked:
                walking2 = False
                if play1x < play2x:
                    play2lr = "l"
                if play1x > play2x:
                    play2lr = "r"
                if abs(play2x - play1x) <= 200:
                    randomnumber = random.randint(1, 100)
                    if randomnumber <= 50:
                        shootingwep2 = 1
                        shooting2 = True
                        wepframe2 = 0
                        framecount2 = 0
                        wepphase2 = 0
                        firewall = random.randint(5,15)
                        if play2lr == "l":
                            wepframe2 = 6
                    else:
                        shootingwep2 = 4
                        shooting2 = True
                        wepframe2 = 0
                        framecount2 = 0
                        wepphase2 = 0
                        underground2 = False
                        if play2lr == "l":
                            wepframe2 = 6
                if abs(play2x - play1x) >= 201 and abs(play2x - play1x) <= 550:
                    randomnumber = random.randint(1, 100)
                    if randomnumber <= 25:
                        shootingwep2 = 1
                        shooting2 = True
                        wepframe2 = 0
                        framecount2 = 0
                        wepphase2 = 0
                        firewall = random.randint(5,15)
                        if play2lr == "l":
                            wepframe2 = 6
                    if randomnumber >= 26 and randomnumber <= 50:
                        shootingwep2 = 2
                        shooting2 = True
                        wepframe2 = 0
                        framecount2 = 0
                        wepphase2 = 0
                        underground2 = False
                        if play2lr == "l":
                            wepframe2 = 6
                    if randomnumber >= 51:
                        shootingwep2 = 4
                        shooting2 = True
                        wepframe2 = 0
                        framecount2 = 0
                        wepphase2 = 0
                        underground2 = False
                        if play2lr == "l":
                            wepframe2 = 6
                if abs(play2x - play1x) >= 551 and abs(play2x - play1x) <= 650:
                    randomnumber = random.randint(1,100)
                    if randomnumber <= 75 and mortarshot2 == False:
                        shootingwep2 = 3
                        shooting2 = True
                        wepframe2 = 0
                        framecount2 = 0
                        wepphase2 = 0
                        if play2lr == "l":
                            wepframe2 = 9
                    if randomnumber >= 76 and randomnumber <= 90:
                        shootingwep2 = 1
                        shooting2 = True
                        wepframe2 = 0
                        framecount2 = 0
                        wepphase2 = 0
                        firewall = random.randint(5,15)
                        if play2lr == "l":
                            wepframe2 = 6
                    if randomnumber >= 91:
                        shootingwep2 = 2
                        shooting2 = True
                        wepframe2 = 0
                        framecount2 = 0
                        wepphase2 = 0
                        underground2 = False
                        if play2lr == "l":
                            wepframe2 = 6
                if abs(play2x - play1x) >= 651:
                    shootingwep2 = 2
                    shooting2 = True
                    wepframe2 = 0
                    framecount2 = 0
                    wepphase2 = 0
                    underground2 = False
                    if play2lr == "l":
                        wepframe2 = 6
            else:
                walking2 = True
                if not shellshockedish:
                    if play2x > play1x:
                        play2x = play2x - 8
                        if play2x <= 0:
                            play2x = 0
                        if not moonwalk:
                            play2lr = "l"
                        else:
                            play2lr = "r"
                    if play2x < play1x:
                        play2x = play2x + 8
                        if play2x >= width:
                            play2x = width
                        if not moonwalk:
                            play2lr = "r"
                        else:
                            play2lr = "l"
                    if play2x == play1x:
                        walking2 = False
                        
                if shellshocked:
                    if shellshockeddir == "l":
                        play2x = play2x - 8
                        if play2x <= mortarspot:
                            shellshocked = False
                        if play2x <= 0:
                            play2x = 0
                        if not moonwalk:
                            play2lr = "l"
                        else:
                            play2lr = "r"
                    if shellshockeddir == "r":
                        play2x = play2x + 8
                        if play2x >= mortarspot:
                            shellshocked = False
                        if play2x >= width:
                            play2x = width
                        if not moonwalk:
                            play2lr = "r"
                        else:
                            play2lr = "l"
                        
        else:
            if bootup >= 0:
                bootup -= 1
                

    #processes weapon inputs, draws player when shooting
    play1y = ground[play1x]-47
    play2y = ground[play2x]-47
    if shooting1 == True:
        if shootingwep1 == 1: #shield
            if shield1 >= 1:
                shieldblue.draw(screen, wepframe1, play1x, play1y, 4)
                if wepphase1 == 0:
                    wepframe1 += 1
                    if wepframe1 == 2 or wepframe1 == 8:
                        shielded1 = True
                    if wepframe1 == 5 or wepframe1 == 11:
                        wepphase1 = 1
                        shield1 -= 5
                if wepphase1 == 1:
                    if shield1 >= 0 and keystate[K_s]:
                        shield1 -= 2
                    else:
                        wepphase1 = 2
                if wepphase1 == 2:
                    wepframe1 -= 1
                    if wepframe1 == 1 or wepframe1 == 7:
                        shielded1 = False
                    if wepframe1 == 0 or wepframe1 == 6:
                        shielddelay1 = 5
                        shooting1 = False
            else: shooting1 = False
                
        if shootingwep1 == 2: #sniper rifle
            sniperblue.draw(screen, wepframe1, play1x, play1y, 4)
            if wepphase1 == 0:
                wepframe1 += 1
                if wepframe1 == 5 or wepframe1 == 11:
                    wepphase1 = 1
                    snipery1 = play1y - 5
            if wepphase1 == 1:
                if framecount1 >= 15:
                    wepphase1 = 2
                if framecount1 == 5:
                    if play1lr == "r":
                        sniperx1 = play1x + 45
                        pygame.draw.rect(screen, snipershot, (sniperx1, snipery1, width - sniperx1, 2), 0)
                        for numb in range(sniperx1, width):
                            if snipery1 >= ground[numb]:
                                underground1 = True
                            if numb == play2x and underground1 == False:
                                if snipery1 <= play2y + 50 and snipery1 >= play2y - 50:
                                    if shielded2 == False:
                                        play2health = play2health - 100
                            sniperx1 += 1
                    else:
                        sniperx1 = play1x - 45
                        pygame.draw.rect(screen, snipershot, (sniperx1, snipery1, - sniperx1, 2), 0)
                        for numb in range(0, sniperx1):
                            if snipery1 >= ground[numb]:
                                underground1 = True
                            if numb == play2x and underground1 == False:
                                if snipery1 <= play2y + 50 and snipery1 >= play2y - 50:
                                    if shielded2 == False:
                                        play2health = play2health - 100
                            sniperx1 -= 1
                framecount1 += 1
            if wepphase1 == 2:
                if wepframe1 == 0 or wepframe1 == 6:
                    shooting1 = False
                wepframe1 -= 1
                
        if shootingwep1 == 3: #mortar
            mortarblue.draw(screen, wepframe1, play1x, play1y, 4)
            if wepphase1 == 0:
                if wepframe1 == 8 or wepframe1 == 17:
                    wepphase1 = 1
                    if play1lr == "r":
                        wepframe1 = 5
                    else:
                        wepframe1 = 14
            if wepphase1 == 1:
                if wepframe1 == 0 or wepframe1 == 9:
                    shooting1 = False
            if shooting1 == True and framecount1 == 2:
                if wepphase1 == 0:
                    wepframe1 = wepframe1 + 1
                if wepphase1 == 1:
                    wepframe1 = wepframe1 - 1
                framecount1 = 0
            framecount1 = framecount1 + 1
            if wepframe1 == 5 or wepframe1 == 14:
                if wepphase1 == 1:
                    mortarshot1 = True
                    if play1lr == "r":
                        mortarx1 = play1x + 20
                    else:
                        mortarx1 = play1x - 20
                    mortary1 = play1y
                    mortarchange1 = 36
                    if play1lr == "l":
                        mortardirection1 = -15
                    else:
                        mortardirection1 = 15
                        
        if shootingwep1 == 4: #assault rifle
            arblue.draw(screen, wepframe1, play1x, play1y, 4)
            if wepphase1 == 0:
                wepframe1 += 1
                if wepframe1 == 5 or wepframe1 == 11:
                    wepphase1 = 1
                    if play1lr == "r":
                        wepframe1 = 5
                    else:
                        wepframe1 = 11
            if wepphase1 == 1:
                if framecount1 == 1:
                    arshot11 = True
                if framecount1 == 2:
                    arshot12 = True
                if framecount1 == 3:
                    arshot13 = True
                if framecount1 >= 5:
                    wepphase1 = 2
                framecount1 += 1
            if wepphase1 == 2:
                wepframe1 -= 1
                if wepframe1 == 0 or wepframe1 == 6:
                    shooting1 = False

    if shooting2 == True:
        if shootingwep2 == 1: #shield
            if shield2 >= 1:
                shieldred.draw(screen, wepframe2, play2x, play2y, 4)
                if wepphase2 == 0:
                    wepframe2 += 1
                    if wepframe2 == 2 or wepframe2 == 8:
                        shielded2 = True
                    if wepframe2 == 5 or wepframe2 == 11:
                        wepphase2 = 1
                        shield2 -= 5
                if wepphase2 == 1:
                    if shield2 >= 0:
                        if not ai:
                            if keystate[K_DOWN]:
                                shield2 -= 2
                            else:
                                wepphase2 = 2
                        if ai:
                            if firewall > 0:
                                shield2 -= 2
                                firewall -= 1
                            else:
                                wepphase2 = 2
                    else:
                        wepphase2 = 2
                if wepphase2 == 2:
                    wepframe2 -= 1
                    if wepframe2 == 1 or wepframe2 == 7:
                        shielded2 = False
                    if wepframe2 == 0 or wepframe2 == 6:
                        shielddelay2 = 5
                        shooting2 = False
            else: shooting2 = False
            
        if shootingwep2 == 4: #assault rifle
            arred.draw(screen, wepframe2, play2x, play2y, 4)
            if wepphase2 == 0:
                wepframe2 += 1
                if wepframe2 == 5 or wepframe2 == 11:
                    wepphase2 = 1
                    if play2lr == "r":
                        wepframe2 = 5
                    else:
                        wepframe2 = 11
            if wepphase2 == 1:
                if framecount2 == 1:
                    arshot21 = True
                if framecount2 == 2:
                    arshot22 = True
                if framecount2 == 3:
                    arshot23 = True
                if framecount2 >= 5:
                    wepphase2 = 2
                framecount2 += 1
            if wepphase2 == 2:
                wepframe2 -= 1
                if wepframe2 == 0 or wepframe2 == 6:
                    shooting2 = False

        if shootingwep2 == 3: #mortar
            mortarred.draw(screen, wepframe2, play2x, play2y, 4)
            if wepphase2 == 0:
                if wepframe2 == 8 or wepframe2 == 17:
                    wepphase2 = 1
                    if play2lr == "r":
                        wepframe2 = 5
                    else:
                        wepframe2 = 14
            if wepphase2 == 1:
                if wepframe2 == 0 or wepframe2 == 10:
                    shooting2 = False
            if shooting2 == True and framecount2 == 2:
                if wepphase2 == 0:
                    wepframe2 = wepframe2 + 1
                if wepphase2 == 1:
                    wepframe2 = wepframe2 - 1
                framecount2 = 0
            framecount2 = framecount2 + 1
            if wepframe2 == 5 or wepframe2 == 14:
                if wepphase2 == 1:
                    mortarshot2 = True
                    if play2lr == "r":
                        mortarx2 = play2x + 20
                    else:
                        mortarx2 = play2x - 20
                    mortary2 = play2y
                    mortarchange2 = 36
                    if play2lr == "l":
                        mortardirection2 = -15
                    else:
                        mortardirection2 = 15

        if shootingwep2 == 2: #sniper rifle
            sniperred.draw(screen, wepframe2, play2x, play2y, 4)
            if wepphase2 == 0:
                wepframe2 += 1
                if wepframe2 == 5 or wepframe2 == 11:
                    wepphase2 = 1
                    snipery2 = play2y - 5
            if wepphase2 == 1:
                if framecount2 >= 15:
                    wepphase2 = 2
                if framecount2 == 5:
                    if play2lr == "r":
                        sniperx2 = play2x + 45
                        pygame.draw.rect(screen, snipershot, (sniperx2, snipery2, width - sniperx2, 2), 0)
                        for numb in range(sniperx2, width):
                            if snipery2 >= ground[numb]:
                                underground2 = True
                            if numb == play1x and underground2 == False:
                                if snipery2 <= play1y + 50 and snipery2 >= play1y - 50:
                                    if shielded1 == False:
                                        play1health = play1health - 100
                            sniperx2 += 1
                    else:
                        sniperx2 = play2x - 45
                        pygame.draw.rect(screen, snipershot, (sniperx2, snipery2, - sniperx2, 2), 0)
                        for numb in range(0, sniperx2):
                            if snipery2 >= ground[numb]:
                                underground2 = True
                            if numb == play1x and underground2 == False:
                                if snipery2 <= play1y + 50 and snipery2 >= play1y - 50:
                                    if shielded1 == False:
                                        play1health = play1health - 100
                            sniperx2 -= 1
                framecount2 += 1
            if wepphase2 == 2:
                if wepframe2 == 0 or wepframe2 == 6:
                    shooting2 = False
                wepframe2 -= 1

    #deals with projectiles
    arb1y1 = arb1y2 = arb1y3 = play1y - 5
    if play1lr  == "r":
        arb1x1 = arb1x2 = arb1x3 = play1x + 45
    else:
        arb1x1 = arb1x2 = arb1x3 = play1x - 45

    arb2y1 = arb2y2 = arb2y3 = play2y - 5
    if play2lr  == "r":
        arb2x1 = arb2x2 = arb2x3 = play2x + 45
    else:
        arb2x1 = arb2x2 = arb2x3 = play2x - 45
        
    if mortarshot1 == True:
        mortar.draw(screen, 0, mortarx1, mortary1, 4)
        mortarx1 = mortarx1 + mortardirection1
        mortary1 = mortary1 - mortarchange1
        mortarchange1 = mortarchange1 - 2
        if mortarx1 <= 0 or mortarx1 >= width:
            mortarshot1 = False
        if mortary1 >= ground[mortarx1]:
            mortarshot1 = False
            shellshocked = False
            shellshockedish = False
            mortarexploded1 = True
            mortarexplodedframe1 = 1
            if play2x <= mortarx1 + 125 and play2x >= mortarx1 - 125:
                if play2x <= mortarx1:
                    hpchange = mortarx1 - play2x
                else:
                    hpchange = play2x - mortarx1
                hpchange = 125 - hpchange
                if hpchange >= 75:
                    hpchange = 100
                if shielded2 == False:
                    play2health = play2health - hpchange
                

    if mortarshot2 == True:
        mortar.draw(screen, 0, mortarx2, mortary2, 4)
        mortarx2 = mortarx2 + mortardirection2
        mortary2 = mortary2 - mortarchange2
        mortarchange2 = mortarchange2 - 2
        if mortarx2 <= 0 or mortarx2 >= width:
            mortarshot2 = False
        if mortary2 >= ground[mortarx2]:
            mortarshot2 = False
            mortarexploded2 = True
            mortarexplodedframe2 = 1
            if play1x <= mortarx2 + 125 and play1x >= mortarx2 - 125:
                if play1x <= mortarx2:
                    hpchange = mortarx2 - play1x
                else:
                    hpchange = play1x - mortarx2
                hpchange = 125 - hpchange
                if hpchange >= 75:
                    hpchange = 100
                if shielded1 == False:
                    play1health = play1health - hpchange

    if mortarexploded1:
        mortar.draw(screen, mortarexplodedframe1, mortarx1, mortary1 - 40, 4)
        mortarexplodedframe1 += 1
        if mortarexplodedframe1 >= 5:
            mortarexploded1 = False

    if mortarexploded2:
        mortar.draw(screen, mortarexplodedframe2, mortarx2, mortary2 - 40, 4)
        mortarexplodedframe2 += 1
        if mortarexplodedframe2 >= 5:
            mortarexploded2 = False

    if arshot11:
        underground1 = False
        bulletspread1 = random.randint(0,1)
        if bulletspread1 == 0:
            bulletspread1 = -1
        #arb1y1 += bulletspread1
        if play1lr == "r":
            for numb in range(arb1x1, width):
                arb1x1f = numb
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb1y1 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground1:
                    pygame.draw.rect(screen, tracer, (arb1x1f, arb1y1, 3, 3), 0)
                if arb1y1 >= ground[numb] and not underground1:
                    underground1 = True
                    #bullet.draw(screen, 0, numb, arb1y1, 4)
                    #arb1x1f = arb1x1
                    #arb1y1f = arb1x1
                if numb == play2x and not underground1:
                    if arb1y1 <= play2y + 50 and arb1y1 >=play2y - 50:
                        if shielded2 == False:
                            play2health -= 40
                        underground1 = True
        else:
            while arb1x1 >= 0:
                arb1x1 -= 1
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb1y1 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground1:
                    pygame.draw.rect(screen, tracer, (arb1x1, arb1y1, 3, 3), 0)
                if arb1y1 >= ground[arb1x1] and not underground1:
                    underground1 = True
                    #bullet.draw(screen, 0, arb1x1, arb1y1, 4)
                    #arb1x1f = arb1x1
                    #arb1y1f = arb1x1
                if arb1x1 == play2x and not underground1:
                    if arb1y1 <= play2y + 50 and arb1y1 >=play2y - 50:
                        if shielded2 == False:
                            play2health -= 40
                        underground1 = True
        arb11 = 1
        arshot11 = False

    if arshot12:
        underground1 = False
        bulletspread1 = random.randint(0,1)
        #arb1y2 += bulletspread1
        if play1lr == "r":
            for numb in range(arb1x2, width):
                arb1x2 = numb
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb1y2 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground1:
                    pygame.draw.rect(screen, tracer, (arb1x2, arb1y2, 3, 3), 0)
                if arb1y2 >= ground[numb] and not underground1:
                    underground1 = True
                    #bullet.draw(screen, 0, arb1x2, arb1y2, 4)
                    #arb1x2f = arb1x2
                    #arb1y2f = arb1x2
                if numb == play2x and not underground1:
                    if arb1y2 <= play2y + 50 and arb1y2 >=play2y - 50:
                        if shielded2 == False:
                            play2health -= 40
                        underground1 = True
        else:
            while arb1x2 >= 0:
                arb1x2 -= 1
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb1y2 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground1:
                    pygame.draw.rect(screen, tracer, (arb1x2f, arb1y2, 3, 3), 0)
                if arb1y2 >= ground[arb1x2] and not underground1:
                    underground1 = True
                    #bullet.draw(screen, 0, arb1x2, arb1y2, 4)
                    #arb1x2f = arb1x2
                    #arb1y2f = arb1x2
                if arb1x2 == play2x and not underground1:
                    if arb1y2 <= play2y + 50 and arb1y2 >=play2y - 50:
                        if shielded2 == False:
                            play2health -= 40
                        underground1 = True
        arb12 = 1
        arshot12 = False

    if arshot13:
        underground1 = False
        bulletspread1 = random.randint(0,1)
        if bulletspread1 == 0:
            bulletspread1 = -1
        #arb1y3 += bulletspread1
        
        if play1lr == "r":
            for numb in range(arb1x3, width):
                arb1x3f = numb
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb1y3 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground1:
                    pygame.draw.rect(screen, tracer, (arb1x3f, arb1y3, 3, 3), 0)
                if arb1y3 >= ground[numb] and not underground1:
                    underground1 = True
                    #bullet.draw(screen, 0, arb1x3, arb1y3, 4)
                    #arb1x3f = arb1x3
                    #arb1y3f = arb1x3
                if numb == play2x and not underground1:
                    if arb1y3 <= play2y + 50 and arb1y3 >=play2y - 50:
                        if shielded2 == False:
                            play2health -= 40
                        underground1 = True
        else:
            while arb1x3 >= 0:
                arb1x3 -= 1
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb1y3 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground1:
                    pygame.draw.rect(screen, tracer, (arb1x3, arb1y3, 3, 3), 0)
                if arb1y3 >= ground[arb1x3] and not underground1:
                    underground1 = True
                    #bullet.draw(screen, 0, arb1x3, arb1y3, 4)
                    #arb1x3f = arb1x3
                    #arb1y3f = arb1x3
                if arb1x3 == play2x and not underground1:
                    if arb1y3 <= play2y + 50 and arb1y3 >=play2y - 50:
                        if shielded2 == False:
                            play2health -= 40
                        underground1 = True
        arb13 = 1
        arshot13 = False

    if arshot21:
        underground2 = False
        bulletspread1 = random.randint(0,1)
        if bulletspread1 == 0:
            bulletspread1 = -1
        #arb1y1 += bulletspread1
        if play2lr == "r":
            for numb in range(arb2x1, width):
                arb2x1f = numb
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb2y1 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground2:
                    pygame.draw.rect(screen, tracer, (arb2x1f, arb2y1, 3, 3), 0)
                if arb2y1 >= ground[numb] and not underground2:
                    underground2 = True
                    #bullet.draw(screen, 0, numb, arb2y1, 4)
                    #arb2x1f = arb2x1
                    #arb2y1f = arb2x1
                if numb == play1x and not underground2:
                    if arb2y1 <= play1y + 50 and arb2y1 >=play1y - 50:
                        if shielded1 == False:
                            play1health -= 40
                        underground2 = True
        else:
            while arb2x1 >= 0:
                arb2x1 -= 1
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb2y1 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground2:
                    pygame.draw.rect(screen, tracer, (arb2x1, arb2y1, 3, 3), 0)
                if arb2y1 >= ground[arb2x1] and not underground2:
                    underground2 = True
                    #bullet.draw(screen, 0, arb1x1, arb1y1, 4)
                    #arb1x1f = arb1x1
                    #arb1y1f = arb1x1
                if arb2x1 == play1x and not underground2:
                    if arb2y1 <= play1y + 50 and arb2y1 >=play1y - 50:
                        if shielded1 == False:
                            play1health -= 40
                        underground2 = True
        arb21 = 1
        arshot21 = False

    if arshot22:
        underground2 = False
        bulletspread1 = random.randint(0,1)
        #arb1y2 += bulletspread1
        if play2lr == "r":
            for numb in range(arb2x2, width):
                arb2x2 = numb
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb2y2 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground2:
                    pygame.draw.rect(screen, tracer, (arb2x2, arb2y2, 3, 3), 0)
                if arb2y2 >= ground[numb] and not underground2:
                    underground2 = True
                    #bullet.draw(screen, 0, arb1x2, arb1y2, 4)
                    #arb1x2f = arb1x2
                    #arb1y2f = arb1x2
                if numb == play1x and not underground2:
                    if arb2y2 <= play1y + 50 and arb2y2 >=play1y - 50:
                        if shielded1 == False:
                            play1health -= 40
                        underground2 = True
        else:
            while arb2x2 >= 0:
                arb2x2 -= 1
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb2y2 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground2:
                    pygame.draw.rect(screen, tracer, (arb2x2f, arb2y2, 3, 3), 0)
                if arb2y2 >= ground[arb2x2] and not underground2:
                    underground2 = True
                    #bullet.draw(screen, 0, arb1x2, arb1y2, 4)
                    #arb1x2f = arb1x2
                    #arb1y2f = arb1x2
                if arb2x2 == play1x and not underground2:
                    if arb2y2 <= play1y + 50 and arb2y2 >=play1y - 50:
                        if shielded1 == False:
                            play1health -= 40
                        underground2 = True
        arb22 = 1
        arshot22 = False

    if arshot23:
        underground2 = False
        bulletspread1 = random.randint(0,1)
        if bulletspread1 == 0:
            bulletspread1 = -1
        #arb1y3 += bulletspread1
        
        if play2lr == "r":
            for numb in range(arb2x3, width):
                arb2x3f = numb
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb2y3 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground2:
                    pygame.draw.rect(screen, tracer, (arb2x3f, arb2y3, 3, 3), 0)
                if arb2y3 >= ground[numb] and not underground2:
                    underground2 = True
                    #bullet.draw(screen, 0, arb1x3, arb1y3, 4)
                    #arb1x3f = arb1x3
                    #arb1y3f = arb1x3
                if numb == play1x and not underground2:
                    if arb2y3 <= play1y + 50 and arb2y3 >=play1y - 50:
                        if shielded1 == False:
                            play1health -= 40
                        underground2 = True
        else:
            while arb2x3 >= 0:
                arb2x3 -= 1
                change = random.randint(1,15)
                if change == 1:
                    change = 1
                else:
                    change = 0
                arb2y3 += bulletspread1*change
                change1 = random.randint(0,50)
                if change1 == 50 and not underground2:
                    pygame.draw.rect(screen, tracer, (arb2x3, arb2y3, 3, 3), 0)
                if arb2y3 >= ground[arb2x3] and not underground2:
                    underground2 = True
                    #bullet.draw(screen, 0, arb1x3, arb1y3, 4)
                    #arb1x3f = arb1x3
                    #arb1y3f = arb1x3
                if arb2x3 == play1x and not underground2:
                    if arb2y3 <= play1y + 50 and arb2y3 >=play1y - 50:
                        if shielded1 == False:
                            play1health -= 40
                        underground2 = True
        arb23 = 1
        arshot23 = False

    #draws players
    walk1frame = walk1frame + 1
    if walk1frame >= 7:
        walk1frame = 0
    frame1 = 0
    if walking1 == True:
        frame1 = frame1 + walk1frame
    if play1lr == "l":
        frame1 = frame1 + 7
    if walking1 == True:
        walkblue.draw(screen, frame1, play1x, play1y, 4)
    else:
        if shooting1 == False:
            if play1lr == "l":
                walkblue.draw(screen, 7, play1x, play1y, 4)
            else:
                walkblue.draw(screen, 0, play1x, play1y, 4)

    walk2frame = walk2frame + 1
    if walk2frame >= 7:
        walk2frame = 0
    frame2 = 0
    if walking2 == True:
        frame2 = frame2 + walk2frame
    if play2lr == "l":
        frame2 = frame2 + 7
    if walking2 == True:
        walkred.draw(screen, frame2, play2x, play2y, 4)
    else:
        if shooting2 == False:
            if play2lr == "l":
                walkred.draw(screen, 7, play2x, play2y, 4)
            else:
                walkred.draw(screen, 0, play2x, play2y, 4)

    if shooting1 == True and shootingwep1 == 1:
        shielddelay1 = 5
    else:
        if shielddelay1 <= 0:
            shielddelay1 = 0
            shield1 += 1
        else:
            shielddelay1 -= 1

    if shooting2 == True and shootingwep2 == 1:
        shielddelay2 = 5
    else:
        if shielddelay2 <= 0:
            shielddelay2 = 0
            shield2 += 1
        else:
            shielddelay2 -= 1          

    if shield1 <= 0:
        shield1 = 0
        shielded1 = False
    if shield1 >= 60:
        shield1 = 60

    if shield2 <= 0:
        shield2 = 0
        shielded2 = False
    if shield2 >= 60:
        shield2 = 60

    if suddendeath == True:
        if play1health < 100:
            play1health = 0
        if play2health < 100:
            play2health = 0
    
    #draws health and shield bars:
    #player 1 health bar
    pygame.draw.rect(screen, barout, (20, 20, 110, 35), 0)
    pygame.draw.rect(screen, barback, (25, 25, 100, 25), 0)
    if play1health >= 1:
        pygame.draw.rect(screen, healthbar, (25, 25, play1health, 25), 0)

    #player 1 shield bar
    pygame.draw.rect(screen, barout, (20, 60, 70, 25), 0)
    pygame.draw.rect(screen, barback, (25, 65, 60, 15), 0)
    if shield1 >= 1:
        pygame.draw.rect(screen, shieldbar, (25, 65, shield1, 15), 0)

    #player 2 health bar
    pygame.draw.rect(screen, barout, (width - 20, 20, -110, 35), 0)
    pygame.draw.rect(screen, barback, (width - 25, 25, -100, 25), 0)
    if play2health >= 1:
        pygame.draw.rect (screen, healthbar, (width - 25, 25, -play2health, 25), 0)

    #player 2 shield bar
    pygame.draw.rect(screen, barout, (width - 20, 60, -70, 25), 0)
    pygame.draw.rect(screen, barback, (width - 25, 65, -60, 15), 0)
    if shield2 >= 1:
        pygame.draw.rect(screen, shieldbar, (width - 25, 65, -shield2, 15), 0)
        

    #checks if someone lost
    if play1health <= 0 and play2health <= 0:
        print "Tie!"
        tie = True
        running = False
    if play1health <= 0 and not tie:
        print "Red Wins!"
        running = False
    if play2health <= 0 and not tie:
        print "Blue Wins!"
        running = False
        #checks if the player chose to exit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fps.tick(60)

    #update screen, draw all shapes
    pygame.display.update()
pygame.quit()
sys.exit()
