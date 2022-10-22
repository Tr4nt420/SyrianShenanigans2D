import Beings
from Beings.Instances import *

from Tools.Projectile import Projectile

import random as ran

from Utils.Utils import *

import math
import time

import pygame

class Weapon(Instance):
    listOfWeapons = []
    def __init__(self, image: str, x: int, y: int, screen, *args, **kwargs):
        super().__init__(image, x, y, screen)
        self.parent = None
        self.flippedImage = pygame.transform.flip(self.image, True, False)

        self.projectTileSpeed = kwargs["speed"]
        self.listOfProjectiles = []
        self.rateOfFire = kwargs["rateOfFire"]
        self.lastTimeFired = time.time()
        self.bullet_sprite = kwargs["bullet_sprite"]
        self.degree = kwargs["degree"]
        self.isDropped = False
        self.spread = kwargs["spread"]
        self.maxDistance = kwargs["maxDistance"]
        self.minDamage = kwargs["minDamage"]
        self.maxDamage = kwargs["maxDamage"]
        self.name = kwargs["name"]
        self.isFlipped = False
        Weapon.listOfWeapons.append(self)


    def shoot(self, pos: tuple):
        if (time.time()-self.lastTimeFired) >= (60/self.rateOfFire) and self.parent:
            x, y = pos[0], pos[1]
            spread = math.radians(ran.randint(-self.spread, self.spread))
            dx, dy = get_direction(x, self.rect.x, y, self.rect.y)
            angle = math.atan2(dx, dy)
            if not self.isFlipped:
                xPos = self.rect.x+(dx*(self.ix))
            else:
                xPos = self.rect.x+(dx*(self.ix/2))
            if math.degrees(angle) > -90 and math.degrees(angle) < 90:
                yPos = self.rect.y+(dy*2*self.iy)
            else:
                yPos = self.rect.y+(dy*self.iy)





            newProjectile = Projectile(self.bullet_sprite, xPos, yPos, self.screen,
                                       dx+spread, dy+spread, self.maxDistance)


            dir = math.degrees(math.atan2(dx+spread, dy+spread))

            newProjectile.image = pygame.transform.rotate(newProjectile.originalimage, self.degree+dir)
            self.listOfProjectiles.append(newProjectile)
            self.lastTimeFired = time.time()

    def update_projectiles(self, dt, collideGroup):
        for p in self.listOfProjectiles:
            p.x += p.dx*self.projectTileSpeed*dt
            p.y += p.dy*self.projectTileSpeed*dt
            p.update(dt)
            listOfCols = pygame.sprite.spritecollide(p, collideGroup, False)
            def removeBullet():
                self.listOfProjectiles.remove(p)
                p.kill()
            if len(listOfCols) > 0 or math.hypot(self.x-p.x, self.y-p.y) > p.maxDistance:
                removeBullet()

            for i in listOfCols:
                damage = ran.randint(self.minDamage, self.maxDamage)
                i.deal_damage(damage)

                if i.health <= 0:
                    collideGroup.remove(i)

    def update_to_parent(self):
        if self.parent:
            self.x = self.parent.rect.x
            self.y = self.parent.rect.y

            self.rotate_to_mouse(pygame.mouse.get_pos())

    def kill(self):
        if self in Weapon.listOfWeapons:
            Weapon.listOfWeapons.remove(self)

        super().kill()

    def update(self, dt):
        player = self.parent
        if player:
            currentSlotLoc = None
            for i in player.equipSlots:
                if player.equipSlots[i] and player.equipSlots[i] == self:
                    currentSlotLoc = i
                    break
            if player.currentEquipSlot == currentSlotLoc:
                super().update(dt)

        if self.isDropped:
            super().update(dt)



