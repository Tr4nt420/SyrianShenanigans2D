from Beings.Character import Character
import pygame, sys
import time
from Tools.Weapon import Weapon
import random as ra

from Layout.LayoutStuff import Layout
textConfig = {"font" : "dejavusans",
              "appearanceTime" : 0.7,
              "fontSize" : 15,
              "colour": (255,255,255)}
pygame.font.init()
class Player(Character):
    listOfPlayers = []

    def __init__(self, image: str, x: int, y: int, screen):
        super().__init__(image, x, y, screen)
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.currentWeapon = None
        self.health = 100
        self.speed = 75
        self.lastDropped = {}
        self.dropPickUpDelay = 3
        self.equipSlots = {1: None, 2: None, 3: None}
        self.currentEquipSlot = 1
        self.fillToAdd = 150

        Player.listOfPlayers.append(self)


    def keyChange(self, typeOfChange: str, key):
        isPressed = True if typeOfChange == "down" else False

        if key == pygame.K_w:
            self.up = isPressed

        if key == pygame.K_s:
            self.down = isPressed

        if key == pygame.K_a:
            self.left = isPressed

        if key == pygame.K_d:
            self.right = isPressed

        if isPressed:
            try:
                keyPressed = int(pygame.key.name(key))
                if keyPressed in self.equipSlots and keyPressed != self.currentEquipSlot:
                    if self.equipSlots[self.currentEquipSlot]:
                        self.equipSlots[self.currentEquipSlot].parent = None
                    self.currentEquipSlot = keyPressed
                    if self.equipSlots[self.currentEquipSlot]:
                        self.currentWeapon = self.equipSlots[self.currentEquipSlot]
                        self.equipSlots[self.currentEquipSlot].parent = self
                        nofText = f"Slot {keyPressed}: {self.currentWeapon.name}"
                    else:
                        self.currentWeapon = None
                        nofText = f"Slot {keyPressed}: Empty"

                    for i in Layout.listOfLayouts:
                        if i.textContent.startswith("Slot"):
                            Layout.remove(i)
                    noftificeSlotChange = Layout(0, self.sy*0.9, self.screen, nofText, **textConfig, noAdd=True)
                    noftificeSlotChange.x = (self.sx/2)-(noftificeSlotChange.get_size()[0]/2)
                    Layout.listOfLayouts.append(noftificeSlotChange)
            except ValueError:
                pass


    def equip(self, weapon, slot):
        # self.currentWeapon = weapon
        # weapon.parent = self

        self.equipSlots[slot] = weapon
        weapon.isDropped = False
        if slot == self.currentEquipSlot:
            self.currentWeapon = self.equipSlots[self.currentEquipSlot]
            self.currentWeapon.parent = self

    def drop(self):
        if self.currentWeapon:
            self.lastDropped[self.currentWeapon] = time.time()
            self.equipSlots[self.currentEquipSlot] = None
            self.currentWeapon.parent = None

            self.currentWeapon.isDropped = True
            self.currentWeapon = None

    def kill(self):
        if self in Player.listOfPlayers:

            Player.listOfPlayers.remove(self)
        super().kill()

    def update(self, dt):
        super().update(dt)
        listOfCollidedWeapons = pygame.sprite.spritecollide(self, Weapon.listOfWeapons, False)
        if not self.currentWeapon:
            for i in [i for i in listOfCollidedWeapons if i != self.currentWeapon and i.isDropped]:
                if isinstance(i, Weapon):
                    if i not in self.lastDropped or (time.time() - self.lastDropped[i]) >= self.dropPickUpDelay:
                        for sn in range(1, len(self.equipSlots)):
                            if self.equipSlots[sn] == None:
                                self.equip(i, sn)
                                notificePickup = notificePickup = Layout(0, self.sy*0.9, self.screen, f"You have picked up {i.name}", **textConfig, noAdd=True)
                                notificePickup.x = (self.sx/2)-(notificePickup.get_size()[0]/2)
                                Layout.listOfLayouts.append(notificePickup)

                                break
        if self.health <= 0:

            self.kill()
            for i in list(self.equipSlots):
                if self.equipSlots[i]:
                    weapon = self.equipSlots[i]
                    weapon.parent = None
                    weapon.isDropped = True
