import pygame, sys
import time
from pygame.locals import QUIT

import Beings
import Tools

from Beings.Instances import Instance
from Beings.Player import Player
from Beings.Enemy import Enemy
from Tools.Weapon import Weapon
from Layout.LayoutStuff import Layout
from Tools.Pickup import PickupItem
import random as ra

import math

DEBUG = False
clock = pygame.time.Clock()

pygame.init()
pygame.font.init()

DISPLAYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN) if not DEBUG else pygame.display.set_mode((600,400))

allowedInput = {"movementKeys": [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], 
                "spawnNewEnemy": pygame.K_f,
               "dropWeapon": pygame.K_q,
               "changeEquipSlot": [pygame.K_1, pygame.K_2, pygame.K_3]}

x, y = DISPLAYSURF.get_size()

#Weapons
Weapons = {}
Weapons["WeirdGun"] = lambda: Weapon("Weapons/WeirdGun/weapon.png", 0, 0, DISPLAYSURF , 
                bullet_sprite="Weapons/WeirdGun/bullet.png", 
                degree = 90, 
                rateOfFire= 860,
                maxDistance = 1000,
                spread = 8 if not DEBUG else 0,
                minDamage = 35,
                maxDamage = 50,
                speed = 3000,
                name="SomethingSomething")

pygame.display.set_caption('Syrian Shenanigans 2D')
icon = pygame.image.load("enemy.png")
pygame.display.set_icon(icon)

               
running = True
def spawnEnemy():
    enemy = Enemy("enemy.png", 999, 999, DISPLAYSURF)
    enemy.x = ra.randint(0, x-enemy.ix)
    enemy.y = ra.randint(0, y-enemy.iy*2)
#kill Count related
enemyCount = 0
scoreCount = pygame.font.SysFont("dejavusans", 16)
lastCount = 0
#healt related
healthCount = pygame.font.SysFont("dejavusans", 16)




#gameState

isMouseDown = False
isEndless = False
isClassic = False
isStarted = False
isMenuOn = False
isSpawnedInitialEnemies = False
isDead = False
textConfig = {"font" : "dejavusans",
              "appearanceTime" : 3,
              "fontSize" : 15,
              "colour": (255,255,255)}
fps = 0
              
chancesOfMultiplying = 0.10             

listOfPotions = ["Healing Potion", "Speed Potion", "Damage Potion"]
def healingPotionPickup(self, player):
    player.health += 50
    return True
    
def speedPotionPickup(self, player):
    player.speed += 20
    return True
    
def damagePotionPickup(self, player):
    if player.currentWeapon:
        player.currentWeapon.minDamage+=10
        player.currentWeapon.maxDamage+=10
        return True
    else:
        return False
    
    
def spawnItem(picture, name, onPickup):
    item = PickupItem(picture, 0,0, DISPLAYSURF, name)
    item .x= ra.randint(0, x-item.ix)
    item.y = ra.randint(0, y-(item.iy*2))
    item.onPickup = onPickup

def Start():
    global isStarted
    player = Player("player.png", 9999, 9999, DISPLAYSURF)
    
    player.equip(Weapons["WeirdGun"](), 1)
    player.x = ra.randint(0, x-player.ix)
    player.y = ra.randint(0, y-(player.iy*2))
    elText = f"Chances of enemies multiplying on killed: {int(chancesOfMultiplying*100)}%"
    elTextConf = textConfig.copy()
    elTextConf["appearanceTime"] = math.inf
    elTextConf["colour"] = (0,0,0)
    elTextConf["description"] = "Chance"
    Layout("topright",y*0.03, DISPLAYSURF, elText, **elTextConf)
    elTextConf['description'] = "FramePerSec"
    Layout("topright", y*0.06, DISPLAYSURF, f"FPS: {int(fps)}", **elTextConf)
    isStarted = True
    
def Menu():
    
    global isMenuOn
    global isDead
    isMenuOn = True
    menuConfig = textConfig.copy()
    menuConfig["appearanceTime"] = math.inf
    menuConfig["description"] = "Menu buttons"
    menuConfig["colour"] = (0,0,0)
    #Text
    bigTextConfig = menuConfig
    bigTextConfig["fontSize"] = 32
    bigText = Layout("center", y*0.30, DISPLAYSURF, "Syrian Shenanigans 2D", **bigTextConfig)

     
    #Classic
    buttonConfig = bigTextConfig
    
    buttonConfig["fontSize"] = 24
    buttonConfig["colour"] = (0,255,0)
    classicButton = Layout("center", y*0.45, DISPLAYSURF, "Play", **buttonConfig)
    global isClassic
    def classic(self):
        Start()
        global isClassic
        isClassic = True
    classicButton.onClicked = classic
    
    
    
    
percentageAdded = 0
while True:
    if not isMenuOn and not isStarted:
        Menu()
        player = None
    
    
    if isStarted:
        if isMenuOn:
            listOfCraps = [i for i in Layout.listOfLayouts if i.description and i.description == "Menu buttons"]
            for i in listOfCraps:
                Layout.remove(i)
            isMenuOn = False
        if not isSpawnedInitialEnemies:
            for i in range(5 if not DEBUG else 0):
                spawnEnemy()
            isSpawnedInitialEnemies = True
        if len(Player.listOfPlayers) > 0:
            player = Player.listOfPlayers[0]
        else:
            isDead = True
            
            
    if isDead:
        for i in Instance.listOfInstances:
            Instance.listOfInstances.remove(i)
            i.kill()
        for i in Layout.listOfLayouts:
            Layout.remove(i)
        
        lastCount = 0
        if len(Instance.listOfInstances) == 0:
            isDead = False
            isEndless = False
            isClassic = False
            isStarted = False
            isSpawnedInitialEnemies = False
            enemyCount = 0
            chancesOfMultiplying = 0.10           
            percentageAdded = 0  


        
    
    DISPLAYSURF.fill((112,128,144))
    dt = clock.tick()/1000
    differenceInECount = lastCount-len(Enemy.listOfEnemies)
    if differenceInECount > 0:
        enemyCount += differenceInECount
        if ra.random() < chancesOfMultiplying:
            differenceInECount*=2
        if enemyCount%5 == 0:
            percentageToAdd = (enemyCount/5/10/10)
            chancesOfMultiplying += percentageToAdd-percentageAdded
            percentageAdded = percentageToAdd
        if enemyCount%10==0:
            choice = ra.choice(listOfPotions)
            if choice == "Healing Potion":
                spawnItem("Pickups/healingpotion.png", "Healing Potion", healingPotionPickup)
            elif choice == "Speed Potion":
                spawnItem("Pickups/speedpotion.png", "Speed Potion", speedPotionPickup)
            elif choice == "Damage Potion":
                spawnItem("Pickups/damagepotion.png", "Damage Potion", damagePotionPickup)

        for i in range(differenceInECount):
            spawnEnemy()
    lastCount = len(Enemy.listOfEnemies)
        
        
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key in allowedInput["movementKeys"] or event.key in allowedInput["changeEquipSlot"]:
                if player:
                    
                    player.keyChange("down" if event.type == pygame.KEYDOWN else "up", event.key)            
            if event.type == pygame.KEYDOWN:
                if event.key == allowedInput["spawnNewEnemy"] and isEndless:
                    spawnEnemy()
                elif event.key == allowedInput["dropWeapon"]:
                    player.drop()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            isLeftclicked = pygame.mouse.get_pressed()[0]
            if isLeftclicked:
                
                for i in Layout.listOfLayouts:
                    if i.onClicked:
                        if i.is_clicked(pygame.mouse.get_pos()):
                            i.click()
                isMouseDown = True
            else:
                isMouseDown = False
       
                
    #player controller
    if isStarted and player:
        if player.up:
            player.y -= player.speed*dt
        if player.down:
            player.y += player.speed*dt
    
        if player.left :
            player.x -= player.speed*dt

        if player.right:
            player.x += player.speed*dt
        
        if isMouseDown:     
            if player.currentWeapon:
                player.currentWeapon.shoot(pygame.mouse.get_pos())

    if not running:
        pygame.quit()
        sys.exit()
    
        
    #Update
    for i in Instance.listOfInstances:
        
        if isinstance(i, Weapon):
            i.update_to_parent()
            i.update_projectiles(dt, Enemy.listOfEnemies)
        elif isinstance(i, Enemy):
            i.move_towards_player(player, dt)
            for tl in i.textList:
                txtsurf = tl.copy()
                text_alpha = pygame.Surface(txtsurf.get_size(), pygame.SRCALPHA)

                text_alpha.fill((255,255,255,int(i.textList[tl]["alpha"])))
                txtsurf.blit(text_alpha, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                DISPLAYSURF.blit(txtsurf, (i.x, i.y-i.textList[tl]["pos"]))
            
        i.update(dt)

    for t in Layout.listOfLayouts:
        if t.description == "Chance":
            t.textContent = f"Chances of enemies multiplying on killed: {int(chancesOfMultiplying*100)}%"
        elif t.description == "FramePerSec":
            t.textContent = f"FPS: {int(fps)}"
        #print(t.textContent)
        t.update()
    #health and enemy counter
    if isStarted and player:
        label = scoreCount.render(f"Amount of enemies killed: {str(enemyCount)}", True, (0,0,0))
        lx, ly = label.get_size()
        DISPLAYSURF.blit(label, (x-lx,0))
        healthLabel = healthCount.render(f"Health: {player.health}", True, (255,0,0))
        DISPLAYSURF.blit(healthLabel, (0,0))

        
    fps = clock.get_fps()  
    pygame.display.update()
    
