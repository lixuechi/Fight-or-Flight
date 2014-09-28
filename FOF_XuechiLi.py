# Fight or Flight
# author: Xuechi Li

import pygame, sys, random
import math
from pygame.locals import *

# constant variables here
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

PLAYER_WIDTH = 110
PLAYER_HEIGHT = 75

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'
SPEED  = 5
FPS = 50

# enemy traits:
yellow = 'yellow'
blue = 'blue'
green = 'green'
purple = 'purple'
cyan = 'cyan'
pink = 'pink'
relaxed = 'relaxed'
sad = 'sad'
cruel = 'cruel'
rational = 'rational'
carried_away = 'carried away'
scared = 'scared'

def main():
    # global variables here
    global DISPLAYSURF, playerImg, fightImg, flightImg, enemy1Obj, enemy2Obj, enemy3Obj, enemy4Obj, enemy5Obj, enemy6Obj, enemy6X, enemy6Y, enemy5X, enemy5Y, enemy4X, enemy4Y, enemy3X, enemy3Y, enemy2X, enemy2Y, enemy1X, enemy1Y, playerObj, playerX, playerY, fpsClock

    #used to test the random function
    #print random.randint(1, 6)

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Fight or Flight')
    fpsClock = pygame.time.Clock()

    playerImg = pygame.image.load('bat2.png')
    STARTSIZE = 50
    playerX = 400
    playerY = 300
    enemyImg = pygame.image.load('enemy1.png')
    enemyImg2 = pygame.image.load('enemy5.png')
    enemyImg3 = pygame.image.load('enemy2.png')
    enemyImg4 = pygame.image.load('enemy3.png')
    enemyImg5 = pygame.image.load('enemy4.png')
    enemyImg6 = pygame.image.load('enemy6.png')

    #enemies' initial coords
    enemy1X = 0
    enemy1Y = 0
    enemy2X = 800
    enemy2Y = 600
    enemy3X = 800
    enemy3Y = 0
    enemy4X = 0
    enemy4Y = 660
    enemy5X = 400
    enemy5Y = -80
    enemy6X = 400
    enemy6Y = 600
    
    # maybe randomize enemies' attributes
    # not implemented yet
    
    # for testing purpose
    #fightImg = pygame.image.load('ri.png')
    #flightImg = pygame.image.load('yue.png')

    playerObj = {'surface': playerImg,
                 'direction': UP,
                 'x': playerX,
                 'y': playerY,
                 'width': 110,
                 'height': 75,
                 'weight': 300,
                 'strength': 70,
                 'health': 250 }

    enemy1Obj = {'surface': enemyImg,
                 'direction': RIGHT,
                 'x': enemy1X,
                 'y': enemy1Y,
                 'width': 40,
                 'height': 40,
                 'weight': 40,
                 'color': yellow,
                 'mood': relaxed, #proceed slowly
                 'dice': 1,
                 'strength': 2,
                 'defense': 0.1,
                 'health': 100 }

    enemy2Obj = {'surface': enemyImg2,
                 'direction': RIGHT,
                 'x': enemy2X,
                 'y': enemy2Y,
                 'width': 75,
                 'height': 75,
                 'weight': 80,
                 'color': cyan,
                 'mood': sad, # tend to suicide
                 'dice': 2,
                 'strength': 10,
                 'defense': 0.2,
                 'health': 300 }

    enemy3Obj = {'surface': enemyImg3,
                 'direction': RIGHT,
                 'x': enemy3X,
                 'y': enemy3Y,
                 'width': 50,
                 'height': 50,
                 'weight': 40,
                 'color': blue,
                 'mood': scared, # tend to flee
                 'dice': 3,
                 'strength': 20,
                 'defense': 0.6,
                 'health': 100 }

    enemy4Obj = {'surface': enemyImg4,
                 'direction': RIGHT,
                 'x': enemy4X,
                 'y': enemy4Y,
                 'width': 30,
                 'height': 30,
                 'weight': 40,
                 'color': pink,
                 'mood': carried_away, # too dumb to escape nor attack
                 'dice': 4,
                 'strength': 20,
                 'defense': 0.1,
                 'health': 100 }

    enemy5Obj = {'surface': enemyImg5,
                 'direction': RIGHT,
                 'x': enemy5X,
                 'y': enemy5Y,
                 'width': 60,
                 'height': 60,
                 'weight': 40,
                 'color': green,
                 'mood': cruel, # keep attacking fiercely
                 'dice': 5,
                 'strength': 10,
                 'defense': 0.7,
                 'health': 400 }

    # under construction, not shown currently
    enemy6Obj = {'surface': enemyImg6,
                 'direction': RIGHT,
                 'x': enemy6X,
                 'y': enemy6Y,
                 'width': 100,
                 'height': 100,
                 'weight': 40,
                 'color': purple,
                 'mood': rational, # only attack when winPerc >= 80%
                 'dice': 6,
                 'strength': 20,
                 'defense': 0.9,
                 'health': 100 }               

    while True:
        runGame()



def gameOver():
    pygame.quit()
    sys.exit()


def runGame():

    # initialize move direction
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    
    flight1 = False    
    flight2 = False
    flight3 = False
    flight4 = False
    flight5 = False
    flight6 = False
    
    runToPlayer1 = True
    runToPlayer2 = True
    runToPlayer3 = True
    runToPlayer4 = True
    runToPlayer5 = True
    runToPlayer6 = True
    
    fight1 = False
    fight2 = False
    fight3 = False
    fight4 = False
    fight5 = False
    fight6 = False
    
    idle1 = False
    idle2 = False
    idle3 = False
    idle4 = False
    idle5 = False
    idle6 = False

    wander4 = False
    
    e1AttackEnable = True
    e2AttackEnable = True
    e3AttackEnable = True
    e4AttackEnable = True
    e5AttackEnable = True
    e6AttackEnable = True

    e1Dead = False
    e2Dead = False
    e3Dead = False
    e4Dead = False
    e5Dead = False
    e6Dead = False

    shoot = False

    #each time at the beginning, roll the dice
    # 1 - 6 corresponds to enemy1 to enemy6
    # the selected enemy won't attack the player
    rollDice = random.randint(1, 6)
    if rollDice == enemy1Obj['dice']:
        e1AttackEnable = False
    elif rollDice == enemy2Obj['dice']:
        e2AttackEnable = False
    elif rollDice == enemy3Obj['dice']:
        e3AttackEnable = False
    elif rollDice == enemy4Obj['dice']:
        e4AttackEnable = False
    elif rollDice == enemy5Obj['dice']:
        e5AttackEnable = False
    elif rollDice == enemy6Obj['dice']:
        e6AttackEnable = False

    while True: # main game loop
        DISPLAYSURF.fill(WHITE)

        # display the text "hit space to attack"
        spaceAlert()

        # draw the player
        playerObj['rect'] = pygame.Rect( (playerObj['x'],
                                          playerObj['y'],
                                          playerObj['width'],
                                          playerObj['height']) )
        
        DISPLAYSURF.blit(playerObj['surface'], playerObj['rect'])

        # draw the enemy
        #________________enemy1 block________________________________________#
        
        #draw enemy1
        enemy1Obj['rect'] = pygame.Rect( (enemy1Obj['x'],
                                          enemy1Obj['y'],
                                          enemy1Obj['width'],
                                          enemy1Obj['height']) )                                          
        DISPLAYSURF.blit(enemy1Obj['surface'], enemy1Obj['rect'])

        #draw enemy1's health
        if enemy1Obj['health'] <= 0:
            e1Health = '0'
        elif enemy1Obj['health'] > 0:
            e1Health = str(enemy1Obj['health'])
        statusFontObj2 = pygame.font.Font('arial.ttf', 18)
        if e1Dead == True:
            textSurfaceObj2 = statusFontObj2.render(e1Health, True, RED, WHITE)
        elif e1Dead == False:
            textSurfaceObj2 = statusFontObj2.render(e1Health, True, GREEN, WHITE)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (enemy1Obj['x']+enemy1Obj['width']/2, enemy1Obj['y']-20)
        DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)

        # enemy1 running to the player
        #calculate the distance between enemy1 and player
        e1X = enemy1Obj['x']        
        pX = playerObj['x']
        e1Y = enemy1Obj['y']        
        pY = playerObj['y']
        distance1 = math.sqrt((e1X - pX)**2 + (e1Y - pY)**2)

        #state1: running to the player until distance <= 100
        if distance1 > 100 and runToPlayer1:
            if e1X < pX:
                enemy1Obj['x'] += 2
            elif e1X > pX:
                enemy1Obj['x'] -= 2
            if e1Y < pY:
                enemy1Obj['y'] += 2
            elif e1Y > pY:
                enemy1Obj['y'] -= 2

        #state2: determine fight or flight when distance reaches 100
        if distance1 <= 100:
            # calculate the chance of winning
            runToPlayer1 = False

            #if it's selected by rolling the dice, it cannot attack
            if e1AttackEnable == False:
                # further consider its mood
                # 'relaxed' in this case, so not really care
                # idle == 50%, flight == 50%
                twoChooseOne = random.randint(0, 1)
                if twoChooseOne == 0: # fight
                    idle1 = True
                elif twoChooseOne == 1: # flight
                    flight1 = True
            elif e1AttackEnable == True:
                # further consider its strength and health
                # NOTICE: ENEMY'S STRENGTH IS XXX PER FRAME (== XXX * FPS)
                #         PLAYER'S STRENGTH IS XXX PER TIME HITTING THE SPACE
                e1Strength = enemy1Obj['strength'] * FPS
                # the real hurt for enemy1 each time:
                e1Hurt = (1 - enemy1Obj['defense']) * playerObj['strength']
                # the number of times of attack needed to beat enemy1
                e1BeatenNum = enemy1Obj['health'] / e1Hurt + 1
                # the number of times of attack needed to beat player
                p1BeatenNum = playerObj['health'] / e1Strength + 1
                # compare the two beaten numbers:
                if e1BeatenNum > p1BeatenNum:
                    # player more likely to win
                    # the bigger e1BeatenNum is, the less likely enemy1 to win
                    winPercent1 = 50 / (e1BeatenNum - p1BeatenNum)
                    #further consider the mood 'relaxed'
                    if winPercent1 >= 20: # fight
                        fight1 = True
                    elif winPercent1 < 20: # flight
                        flight1 = True
                elif e1BeatenNum <= p1BeatenNum:
                    # enemy1 more likely to win
                    # the smaller e1BeatenNum is, the more likely enemy1 win
                    winPercent1 = 50 * (p1BeatenNum - e1BeatenNum)
                    if winPercent1 >= 50: # fight
                        fight1 = True
                    elif winPercent1 == 0: # when they equal
                        fight1 = True
                    # there's no flight possibility in this case.

        if flight1 == True:
            if pX != e1X:
                slope1 = (pY - e1Y)/(pX - e1X)
                if pY >= e1Y:
                    enemy1Obj['y'] -= 5
                    enemy1Obj['x'] -= 5 * slope1
                elif pY < e1Y:
                    enemy1Obj['y'] += 5
                    enemy1Obj['x'] += 5 * slope1
            elif pX == e1X:
                if pY > e1Y:
                    enemy1Obj['y'] += 5
                elif pY <= e1Y:
                    enemy1Obj['y'] -= 5
            if e1X <= -20 or e1Y <= -20:
                # if enemy out of screen, delete enemy
                flight1 = False

        if fight1 == True and e1Dead == False:
            #fight
            #shoot from enemy to player
            enemyShoot(enemy1Obj['x'], enemy1Obj['y'], playerObj['x']+PLAYER_WIDTH/2, playerObj['y']+PLAYER_HEIGHT/2)
            if playerObj['health'] > 0:
                playerObj['health'] -= enemy1Obj['strength']
            elif playerObj['health'] <= 0:
                gameOver()

        if enemy1Obj['health'] <= 0:
            e1Dead = True

        ################################################################

        #________________enemy2 block________________________________________#
        
        #draw enemy2
        enemy2Obj['rect'] = pygame.Rect( (enemy2Obj['x'],
                                          enemy2Obj['y'],
                                          enemy2Obj['width'],
                                          enemy2Obj['height']) )                                          
        DISPLAYSURF.blit(enemy2Obj['surface'], enemy2Obj['rect'])

        #draw enemy2's health
        if enemy2Obj['health'] <= 0:
            e2Health = '0'
        elif enemy2Obj['health'] > 0:
            e2Health = str(enemy2Obj['health'])
        statusFontObj3 = pygame.font.Font('arial.ttf', 18)
        if e2Dead == True:
            textSurfaceObj3 = statusFontObj3.render(e2Health, True, RED, WHITE)
        elif e2Dead == False:
            textSurfaceObj3 = statusFontObj3.render(e2Health, True, GREEN, WHITE)
        textRectObj3 = textSurfaceObj3.get_rect()
        textRectObj3.center = (enemy2Obj['x']+enemy1Obj['width']/2, enemy2Obj['y']-20)
        DISPLAYSURF.blit(textSurfaceObj3, textRectObj3)

        # enemy2 running to the player
        #calculate the distance between enemy2 and player
        e2X = enemy2Obj['x']        
        pX = playerObj['x']
        e2Y = enemy2Obj['y']        
        pY = playerObj['y']
        distance2 = math.sqrt((e2X - pX)**2 + (e2Y - pY)**2)

        #state1: running to the player until distance <= 100
        if distance2 > 100 and runToPlayer2:
            if e2X < pX:
                enemy2Obj['x'] += 3
            elif e2X > pX:
                enemy2Obj['x'] -= 3
            if e2Y < pY:
                enemy2Obj['y'] += 3
            elif e2Y > pY:
                enemy2Obj['y'] -= 3

        #state2: determine fight or flight when distance reaches 100
        if distance2 <= 100:
            # calculate the chance of winning
            runToPlayer2 = False

            #if it's selected by rolling the dice, it cannot attack
            if e2AttackEnable == False: #selected by the DICE
                # further consider its mood
                # 'sad' in this case, so unlikely to flee and fight
                # idle == 90%, flight == 10%
                tenChooseOne = random.randint(0, 9)
                if tenChooseOne == 0 : # flight
                    flight2 = True
                else: # remain idle
                    idle2 = True
            elif e2AttackEnable == True: # normal scripted mode
                # further consider its strength and health
                # NOTICE: ENEMY'S STRENGTH IS XXX PER FRAME (== XXX * FPS)
                #         PLAYER'S STRENGTH IS XXX PER TIME HITTING THE SPACE
                e2Strength = enemy2Obj['strength'] * FPS
                # the real hurt for enemy2 each time:
                e2Hurt = (1 - enemy2Obj['defense']) * playerObj['strength']
                # the number of times of attack needed to beat enemy2
                e2BeatenNum = enemy2Obj['health'] / e2Hurt + 1
                # the number of times of attack needed to beat player
                p2BeatenNum = playerObj['health'] / e2Strength + 1
                # compare the two beaten numbers:
                
               
                # the bigger e2BeatenNum is, the more likely enemy2 win
                winPercent2 = 50 + e2BeatenNum - p2BeatenNum
                if winPercent2 >= 55: # fight
                    fight2 = True
                elif winPercent2 == 50: # when e2BeatenNum and p2BeatenNum equal
                    idle2 = True
                elif winPercent2 <= 40:
                    #further consider the mood 'sad'
                    flight2 = True
                                       
        if flight2 == True:
            if pX != e2X:
                slope2 = (pY - e2Y)/(pX - e2X)
                if pY >= e2Y:
                    enemy2Obj['y'] -= 5
                    enemy2Obj['x'] -= 5 * slope2
                elif pY < e2Y:
                    enemy2Obj['y'] += 5
                    enemy2Obj['x'] += 5 * slope2
            elif pX == e2X:
                if pY > e2Y:
                    enemy2Obj['y'] += 5
                elif pY <= e2Y:
                    enemy2Obj['y'] -= 5
            if e2X <= -20 or e2Y <= -20:
                # if enemy out of screen, delete enemy
                flight2 = False

        if fight2 == True and e2Dead == False:
            #fight
            #shoot from enemy to player
            enemyShoot(enemy2Obj['x'], enemy2Obj['y'], playerObj['x']+PLAYER_WIDTH/2, playerObj['y']+PLAYER_HEIGHT/2)
            if playerObj['health'] > 0:
                playerObj['health'] -= enemy2Obj['strength']
            elif playerObj['health'] <= 0:
                gameOver()

        if enemy2Obj['health'] <= 0:
            e2Dead = True

        #________________end of enemy2___________________________________
        #################################################################


        #________________enemy3 block________________________________________#
        
        #draw enemy3
        enemy3Obj['rect'] = pygame.Rect( (enemy3Obj['x'],
                                          enemy3Obj['y'],
                                          enemy3Obj['width'],
                                          enemy3Obj['height']) )                                          
        DISPLAYSURF.blit(enemy3Obj['surface'], enemy3Obj['rect'])

        #draw enemy3's health
        if enemy3Obj['health'] <= 0:
            e3Health = '0'
        elif enemy3Obj['health'] > 0:
            e3Health = str(enemy3Obj['health'])
        statusFontObj4 = pygame.font.Font('arial.ttf', 18)
        if e3Dead == True:
            textSurfaceObj4 = statusFontObj4.render(e3Health, True, RED, WHITE)
        elif e3Dead == False:
            textSurfaceObj4 = statusFontObj4.render(e3Health, True, GREEN, WHITE)
        textRectObj4 = textSurfaceObj4.get_rect()
        textRectObj4.center = (enemy3Obj['x']+enemy3Obj['width']/2, enemy3Obj['y']-20)
        DISPLAYSURF.blit(textSurfaceObj4, textRectObj4)

        # enemy3 running to the player
        #calculate the distance between enemy3 and player
        e3X = enemy3Obj['x']        
        pX = playerObj['x']
        e3Y = enemy3Obj['y']        
        pY = playerObj['y']
        distance3 = math.sqrt((e3X - pX)**2 + (e3Y - pY)**2)

        #state1: running to the player until distance <= 100
        if distance3 > 100 and runToPlayer3:
            if e3X < pX:
                enemy3Obj['x'] += 3
            elif e3X > pX:
                enemy3Obj['x'] -= 3
            if e3Y < pY:
                enemy3Obj['y'] += 3
            elif e3Y > pY:
                enemy3Obj['y'] -= 3

        #state2: determine fight or flight when distance reaches 100
        if distance3 <= 100:
            # calculate the chance of winning
            runToPlayer3 = False

            #if it's selected by rolling the dice, it cannot attack
            if e3AttackEnable == False: #selected by the DICE
                # further consider its mood
                # 'scared' in this case, so very likely to flee
                # idle == 20%, flight == 80%
                fiveChooseOne = random.randint(0, 4)
                if fiveChooseOne == 0 : # remain idle
                    idle3 = True
                else: # flight
                    flight3 = True
            elif e3AttackEnable == True: # normal scripted mode
                # further consider its strength and health
                # NOTICE: ENEMY'S STRENGTH IS XXX PER FRAME (== XXX * FPS)
                #         PLAYER'S STRENGTH IS XXX PER TIME HITTING THE SPACE
                e3Strength = enemy3Obj['strength'] * FPS
                # the real hurt for enemy3 each time:
                e3Hurt = (1 - enemy3Obj['defense']) * playerObj['strength']
                # the number of times of attack needed to beat enemy3
                e3BeatenNum = enemy3Obj['health'] / e3Hurt + 1
                # the number of times of attack needed to beat player
                p3BeatenNum = playerObj['health'] / e3Strength + 1
                # compare the two beaten numbers:
                
               
                # the bigger e3BeatenNum is, the more likely enemy3 win
                winPercent3 = 50 + e3BeatenNum - p3BeatenNum
                if winPercent3 >= 56: # fight
                    fight3 = True
                elif winPercent3 < 56: # when e3BeatenNum and p3BeatenNum equal
                    flight3 = True
                                       
        if flight3 == True:
            if pX != e3X:
                slope3 = (pY - e3Y)/(pX - e3X)
                if pY >= e3Y:
                    enemy3Obj['y'] -= 5
                    enemy3Obj['x'] -= 5 * slope3
                elif pY < e3Y:
                    enemy3Obj['y'] += 5
                    enemy3Obj['x'] += 5 * slope3
            elif pX == e3X:
                if pY > e3Y:
                    enemy3Obj['y'] += 5
                elif pY <= e3Y:
                    enemy3Obj['y'] -= 5
            if e3X <= -20 or e3Y <= -20:
                # if enemy out of screen, delete enemy
                flight3 = False

        if fight3 == True and e3Dead == False:
            #fight
            #shoot from enemy to player
            enemyShoot(enemy3Obj['x'], enemy3Obj['y'], playerObj['x']+PLAYER_WIDTH/2, playerObj['y']+PLAYER_HEIGHT/2)
            if playerObj['health'] > 0:
                playerObj['health'] -= enemy3Obj['strength']
            elif playerObj['health'] <= 0:
                gameOver()

        if enemy3Obj['health'] <= 0:
            e3Dead = True

        #________________end of enemy3___________________________________
        #################################################################

        #________________enemy4 block________________________________________#
        
        #draw enemy4
        enemy4Obj['rect'] = pygame.Rect( (enemy4Obj['x'],
                                          enemy4Obj['y'],
                                          enemy4Obj['width'],
                                          enemy4Obj['height']) )                                          
        DISPLAYSURF.blit(enemy4Obj['surface'], enemy4Obj['rect'])

        #draw enemy4's health
        if enemy4Obj['health'] <= 0:
            e4Health = '0'
        elif enemy4Obj['health'] > 0:
            e4Health = str(enemy4Obj['health'])
        statusFontObj5 = pygame.font.Font('arial.ttf', 18)
        if e4Dead == True:
            textSurfaceObj5 = statusFontObj5.render(e4Health, True, RED, WHITE)
        elif e4Dead == False:
            textSurfaceObj5 = statusFontObj5.render(e4Health, True, GREEN, WHITE)
        textRectObj5 = textSurfaceObj5.get_rect()
        textRectObj5.center = (enemy4Obj['x']+enemy4Obj['width']/2, enemy4Obj['y']-20)
        DISPLAYSURF.blit(textSurfaceObj5, textRectObj5)

        # enemy4 running to the player
        #calculate the distance between enemy4 and player
        e4X = enemy4Obj['x']        
        pX = playerObj['x']
        e4Y = enemy4Obj['y']        
        pY = playerObj['y']
        distance4 = math.sqrt((e4X - pX)**2 + (e4Y - pY)**2)

        #state1: running to the player until distance <= 100
        if distance4 > 100 and runToPlayer4:
            if e4X < pX:
                enemy4Obj['x'] += 3
            elif e4X > pX:
                enemy4Obj['x'] -= 3
            if e4Y < pY:
                enemy4Obj['y'] += 3
            elif e4Y > pY:
                enemy4Obj['y'] -= 3

        #state2: determine fight or flight when distance reaches 100
        if distance4 <= 100:
            # calculate the chance of winning
            runToPlayer4 = False

            #if it's selected by rolling the dice, it cannot attack
            if e4AttackEnable == False: #selected by the DICE
                # further consider its mood
                # 'carried_away' in this case, so either remain idle or wander around
                # idle == 30%, wander == 60%, null == 10%
                threeChooseOne = random.randint(0, 2)
                if threeChooseOne == 0 : # remain idle
                    idle4 = True
                else: # wander
                    wander4 = True
            elif e4AttackEnable == True: # normal scripted mode
                # further consider its strength and health
                # NOTICE: ENEMY'S STRENGTH IS XXX PER FRAME (== XXX * FPS)
                #         PLAYER'S STRENGTH IS XXX PER TIME HITTING THE SPACE
                e4Strength = enemy4Obj['strength'] * FPS
                # the real hurt for enemy4 each time:
                e4Hurt = (1 - enemy4Obj['defense']) * playerObj['strength']
                # the number of times of attack needed to beat enemy4
                e4BeatenNum = enemy4Obj['health'] / e4Hurt + 1
                # the number of times of attack needed to beat player
                p4BeatenNum = playerObj['health'] / e4Strength + 1
                # compare the two beaten numbers:
                
               
                # the bigger e4BeatenNum is, the more likely enemy4 win
                winPercent4 = 50 + e4BeatenNum - p4BeatenNum
                if winPercent4 >= 56: # fight
                    fight4 = True
                elif winPercent4 < 56: # when e4BeatenNum and p4BeatenNum equal
                    flight4 = True
                                       
        if flight4 == True:
            if pX != e4X:
                slope4 = (pY - e4Y)/(pX - e4X)
                if pY >= e4Y:
                    enemy4Obj['y'] -= 5
                    enemy4Obj['x'] -= 5 * slope4
                elif pY < e4Y:
                    enemy4Obj['y'] += 5
                    enemy4Obj['x'] += 5 * slope4
            elif pX == e4X:
                if pY > e4Y:
                    enemy4Obj['y'] += 5
                elif pY <= e4Y:
                    enemy4Obj['y'] -= 5
            if e4X <= -20 or e4Y <= -20:
                # if enemy out of screen, delete enemy
                flight4 = False

        if fight4 == True and e4Dead == False:
            #fight
            #shoot from enemy to player
            enemyShoot(enemy4Obj['x'], enemy4Obj['y'], playerObj['x']+PLAYER_WIDTH/2, playerObj['y']+PLAYER_HEIGHT/2)
            if playerObj['health'] > 0:
                playerObj['health'] -= enemy4Obj['strength']
            elif playerObj['health'] <= 0:
                gameOver()

        if wander4 == True and e4Dead == False:
            # roll another round of DICE to determine moving direction!
            wanderDir = random.randint(1, 4)
            if wanderDir == 1: # move left
                enemy4Obj['x'] -= 6
            elif wanderDir == 2: # move right
                enemy4Obj['x'] += 6
            elif wanderDir == 3: # move up
                enemy4Obj['y'] -= 6
            elif wanderDir == 4: # move down
                enemy4Obj['y'] += 6

        if enemy4Obj['health'] <= 0:
            e4Dead = True

        #________________end of enemy4___________________________________
        #################################################################


        #________________enemy5 block________________________________________#
        
        #draw enemy5
        enemy5Obj['rect'] = pygame.Rect( (enemy5Obj['x'],
                                          enemy5Obj['y'],
                                          enemy5Obj['width'],
                                          enemy5Obj['height']) )                                          
        DISPLAYSURF.blit(enemy5Obj['surface'], enemy5Obj['rect'])

        #draw enemy5's health
        if enemy5Obj['health'] <= 0:
            e5Health = '0'
        elif enemy5Obj['health'] > 0:
            e5Health = str(enemy5Obj['health'])
        statusFontObj6 = pygame.font.Font('arial.ttf', 18)
        if e5Dead == True:
            textSurfaceObj6 = statusFontObj6.render(e5Health, True, RED, WHITE)
        elif e5Dead == False:
            textSurfaceObj6 = statusFontObj6.render(e5Health, True, GREEN, WHITE)
        textRectObj6 = textSurfaceObj6.get_rect()
        textRectObj6.center = (enemy5Obj['x']+enemy5Obj['width']/2, enemy5Obj['y']-20)
        DISPLAYSURF.blit(textSurfaceObj6, textRectObj6)

        # enemy5 running to the player
        #calculate the distance between enemy5 and player
        e5X = enemy5Obj['x']        
        pX = playerObj['x']
        e5Y = enemy5Obj['y']        
        pY = playerObj['y']
        distance5 = math.sqrt((e5X - pX)**2 + (e5Y - pY)**2)

        #state1: running to the player until distance <= 100
        if distance5 > 100 and runToPlayer5:
            if e5X < pX:
                enemy5Obj['x'] += 3
            elif e5X > pX:
                enemy5Obj['x'] -= 3
            if e5Y < pY:
                enemy5Obj['y'] += 3
            elif e5Y > pY:
                enemy5Obj['y'] -= 3

        #state2: determine fight or flight when distance reaches 100
        if distance5 <= 100:
            # calculate the chance of winning
            runToPlayer5 = False

            #if it's selected by rolling the dice, it cannot attack
            if e5AttackEnable == False: #selected by the DICE
                # further consider its mood
                # 'cruel' in this case, so a very high chance of flight
                # idle == 5%, flight == 50%, (null == 45%)
                elevenChooseOne = random.randint(0, 10)
                if threeChooseOne == 0 : # remain idle
                    idle5 = True
                else: # flight
                    flight5 = True
            elif e5AttackEnable == True: # normal scripted mode
                # further consider its strength and health
                # NOTICE: ENEMY'S STRENGTH IS XXX PER FRAME (== XXX * FPS)
                #         PLAYER'S STRENGTH IS XXX PER TIME HITTING THE SPACE
                e5Strength = enemy5Obj['strength'] * FPS
                # the real hurt for enemy5 each time:
                e5Hurt = (1 - enemy5Obj['defense']) * playerObj['strength']
                # the number of times of attack needed to beat enemy5
                e5BeatenNum = enemy5Obj['health'] / e5Hurt + 1
                # the number of times of attack needed to beat player
                p5BeatenNum = playerObj['health'] / e5Strength + 1
                # compare the two beaten numbers:
                
               
                # the bigger e5BeatenNum is, the more likely enemy5 win
                winPercent5 = 50 + e5BeatenNum - p5BeatenNum
                if winPercent5 >= 30: # fight
                    fight5 = True
                elif winPercent5 < 30: # when e5BeatenNum and p5BeatenNum equal
                    flight5 = True
                                       
        if flight5 == True:
            if pX != e5X:
                slope5 = (pY - e5Y)/(pX - e5X)
                if pY >= e5Y:
                    enemy5Obj['y'] -= 5
                    enemy5Obj['x'] -= 5 * slope5
                elif pY < e5Y:
                    enemy5Obj['y'] += 5
                    enemy5Obj['x'] += 5 * slope5
            elif pX == e5X:
                if pY > e5Y:
                    enemy5Obj['y'] += 5
                elif pY <= e5Y:
                    enemy5Obj['y'] -= 5
            if e5X <= -20 or e5Y <= -20:
                # if enemy out of screen, delete enemy
                flight5 = False

        if fight5 == True and e5Dead == False:
            #fight
            #shoot from enemy to player
            enemyShoot(enemy5Obj['x'], enemy5Obj['y'], playerObj['x']+PLAYER_WIDTH/2, playerObj['y']+PLAYER_HEIGHT/2)
            if playerObj['health'] > 0:
                playerObj['health'] -= enemy5Obj['strength']
            elif playerObj['health'] <= 0:
                gameOver()

        if enemy5Obj['health'] <= 0:
            e5Dead = True

        #________________end of enemy5___________________________________
        #################################################################

        #show everyone's status
        pHealth = str(playerObj['health'])
        statusFontObj = pygame.font.Font('arial.ttf', 18)
        textSurfaceObj1 = statusFontObj.render(pHealth, True, GREEN, WHITE)
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (playerObj['x']+PLAYER_WIDTH/2, playerObj['y']-20)
        DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)

   	
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    playerObj['direction'] = LEFT
                    moveLeft = True
                    moveRight = False

                elif event.key == K_RIGHT:
                    playerObj['direction'] = RIGHT
                    moveRight = True
                    moveLeft = False

                elif event.key == K_UP:
                    playerObj['direction'] = UP
                    moveUp = True
                    moveDown = False

                elif event.key == K_DOWN:
                    playerObj['direction'] = DOWN
                    moveDown = True
                    moveUp = False

                elif event.key == K_SPACE:
                    playerAttackAnimation(playerObj['x'] + PLAYER_WIDTH/2, playerObj['y'] + PLAYER_HEIGHT/2)
                    shoot = True

            elif event.type == KEYUP:
                # stop moving the player
                if event.key == K_LEFT:
                    moveLeft = False

                elif event.key == K_RIGHT:
                    moveRight = False

                elif event.key == K_UP:
                    moveUp = False

                elif event.key == K_DOWN:
                    moveDown = False

                elif event.key == K_SPACE:
                    shoot = False

        if moveLeft:
            playerObj['x'] -= SPEED

        if moveRight:
            playerObj['x'] += SPEED

        if moveUp:
            playerObj['y'] -= SPEED

        if moveDown:
            playerObj['y'] += SPEED

        if shoot:
            #detect if there's a collision to enemies:
            # draw player's attack area
            playerObj['attackRange'] = pygame.Rect( (playerObj['x'] - 100,
                                          playerObj['y'] - 100,
                                          playerObj['width'] + 200,
                                          playerObj['height'] + 200) )
            #detect enemy1:           
            if 'rect' in enemy1Obj and playerObj['attackRange'].colliderect(enemy1Obj['rect']):
                if enemy1Obj['health'] > 0:
                    enemy1Obj['health'] -= playerObj['strength']
                elif enemy1Obj['health'] <= 0:
                    enemy1Obj['health'] = 0
                    e1Dead = True

            #detect enemy2:
            if 'rect' in enemy2Obj and playerObj['attackRange'].colliderect(enemy2Obj['rect']):
                if enemy2Obj['health'] > 0:
                    enemy2Obj['health'] -= playerObj['strength']
                elif enemy2Obj['health'] <= 0:
                    enemy2Obj['health'] = 0
                    e2Dead = True

            #detect enemy3:
            if 'rect' in enemy3Obj and playerObj['attackRange'].colliderect(enemy3Obj['rect']):
                if enemy3Obj['health'] > 0:
                    enemy3Obj['health'] -= playerObj['strength']
                elif enemy3Obj['health'] <= 0:
                    enemy3Obj['health'] = 0
                    e3Dead = True

            #detect enemy4:
            if 'rect' in enemy4Obj and playerObj['attackRange'].colliderect(enemy4Obj['rect']):
                if enemy4Obj['health'] > 0:
                    enemy4Obj['health'] -= playerObj['strength']
                elif enemy4Obj['health'] <= 0:
                    enemy4Obj['health'] = 0
                    e4Dead = True

            #detect enemy5:
            if 'rect' in enemy5Obj and playerObj['attackRange'].colliderect(enemy5Obj['rect']):
                if enemy5Obj['health'] > 0:
                    enemy5Obj['health'] -= playerObj['strength']
                elif enemy5Obj['health'] <= 0:
                    enemy5Obj['health'] = 0
                    e5Dead = True

            #detect enemy6:
            if 'rect' in enemy6Obj and playerObj['attackRange'].colliderect(enemy6Obj['rect']):
                if enemy6Obj['health'] > 0:
                    enemy6Obj['health'] -= playerObj['strength']
                elif enemy6Obj['health'] <= 0:
                    enemy6Obj['health'] = 0
                    e6Dead = True
            

        pygame.display.update()
        fpsClock.tick(FPS)

def playerAttackAnimation(posX, posY):
    circleSize = 1
    while (circleSize <= 200):
        pygame.draw.circle(DISPLAYSURF, BLUE, (posX, posY), circleSize, 1)
        pygame.display.update()
        circleSize += 10
        fpsClock.tick(FPS)


def spaceAlert():
    fontObj = pygame.font.Font('arial.ttf', 32)
    textSurfaceObj = fontObj.render('hit space to attack', True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (450, 150)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    #pygame.display.update()
    #fpsClock.tick(FPS)


def enemyShoot(eX, eY, pX, pY):
    pygame.draw.line(DISPLAYSURF, BLUE, (eX, eY), (pX, pY), 2)



    
if __name__ == '__main__':
    main()
