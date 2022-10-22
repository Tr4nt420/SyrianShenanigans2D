import Beings
from Beings.Character import *
from Beings.Player import Player
from Utils.Utils import *
import math

import time

class Enemy(Character):
    listOfEnemies = []
    def __init__(self, image: str, x: int, y: int, screen):
        super().__init__(image, x, y, screen)
        self.speed = 50
        self.health = 500
        self.damage = 25
        self.damageDelayTime = 3
        self.lastTimeDealtDamage = 0
        Enemy.listOfEnemies.append(self)


    def move_towards_player(self, player, dt):
        group = [i for i in Enemy.listOfEnemies if i != self]
        listOfCols = pygame.sprite.spritecollide(self, group+Player.listOfPlayers, False)
        if player:
            if len(listOfCols) < 1:
                dx, dy = get_direction(player.x, self.x, player.y, self.y)
                self.x += dx*self.speed*dt
                self.y += dy*self.speed*dt
            else:
                for i in listOfCols:
                    if isinstance(i, Player):
                        if (time.time()-self.lastTimeDealtDamage) >= self.damageDelayTime:
                            i.deal_damage(self.damage)

                            self.lastTimeDealtDamage = time.time()

                    else:
                        ptcx, ptcy = get_direction(player.x ,i.x, player.y, i.y)
                        self.x += ptcx*self.speed*dt
                        self.y += ptcy*self.speed*dt
                # self.x += -dx*self.speed*dt
                # self.y += -dy*self.speed*dt

    def update(self, dt):
        super().update(dt)
        if self.health <= 0:
            self.kill()

    def kill(self):
        if self in Enemy.listOfEnemies:
            Enemy.listOfEnemies.remove(self)
        super().kill()



