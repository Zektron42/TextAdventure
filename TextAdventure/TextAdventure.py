from os import system
import sys
import random
import readline

keywords = ['look_north', 'look_south', 'look_east', 'look_west', 'look_inventory', 'move_north', 'move_south', 'move_east', 'move_west', 'eat', 'quit']
roomChoices = ['monster', 'door', 'chest', 'wall', 'friendly stranger', 'enemy']
followerChoices = ['John', 'James', 'Kevin', 'Carl', 'Steve', 'Brian', 'Jack', 'Tom', 'Sean', 'Jim', 'Bill', 'Bob', 'Terry', 'Iisac', 'Ben']
itemChoices = ['torch', 'money', 'food', 'weapon', 'armor']


def complete(text, state):
    for cmd in keywords:
        if cmd.startswith(text):
            if not state:
                system('cls')
                return cmd
            else:
                state -= 1

readline.parse_and_bind('tab:complete')
readline.set_completer(complete)

class player():
    def __init__(self):
        self.inventory = {}
        self.followers = []
        self.health = 100
        self.maxHealth = 100
        self.hunger = 31
        self.exp = 0
        self.level = 0
        self.direction = {'north':random.choice(roomChoices),
                          'south':random.choice(roomChoices),
                          'east':random.choice(roomChoices),
                          'west':random.choice(roomChoices)}
        self.direction[random.choice(['north','south','east','west'])] = 'door'
    def makeRoom(self, iDirect):
        self.direction['north'] = random.choice(roomChoices)
        self.direction['south'] = random.choice(roomChoices)
        self.direction['west'] = random.choice(roomChoices)
        self.direction['east'] = random.choice(roomChoices)
        self.direction[random.choice(['north','south','east','west'])] = 'door'
    def eat(self):
        while True:
            try:
                amount = int(input('How much food do you want to eat?(num 1-{n})'.format(n=self.inventory['food'])))
                self.hunger += 7*amount
                self.inventory['food'] -= amount
                if self.health + 10*amount < self.maxHealth:
                    self.health += 10*amount
                elif self.health + 10*amount >= self.maxHealth:
                    self.health = self.maxHealth

            except ValueError:
                print('Use integer value')
            if self.inventory['food'] < 0:
                self.inventory['food'] += amount
                self.hunger -= 7*amount
                self.health -= 10*amount
                print('You don\'t have that much food')
            else:
                print('You gained {hg} hunger, and you gained {hp} HP'.format(hg=7*amount, hp=10*amount))
                break
    def look(self, iDirect):
        if iDirect == 'inventory' and self.inventory == {}:
            print('You have nothing in your inventory')
        elif iDirect == 'inventory' and self.inventory != {}:
            print('You have the following items in your inventory:\n', self.inventory)
        elif iDirect == 'around':
            print(self.direction['north']+' is north, '+self.direction['west']+' is west, '+self.direction['east']+' is east, '+self.direction['south']+' is south')
        elif iDirect == 'followers':
            print('Your followers:\n', self.followers)
        else:
            return self.direction[iDirect]
    def move(self, iDirect):
        if self.direction[iDirect] == 'door':
            self.makeRoom(iDirect)
            print('\nYou walked through the door')
        elif self.direction[iDirect] == 'chest':
            self.direction[iDirect] = 'opened chest'
            chestTemp = random.choice(itemChoices)
            try:
                self.inventory[chestTemp] += 1
            except KeyError:
                self.inventory[chestTemp] = 1
            if chestTemp == 'torch' and 'look_around' not in keywords:
                keywords.append('look_around')
                itemChoices.remove('torch')
            elif chestTemp == 'weapon':
                if self.inventory['weapon'] > 5:
                    print('Your weapon is already MAX level')
                    self.inventory['weapon'] -= 1
                elif self.inventory['weapon'] > 4:
                    print('Your weapon is now MAX level')
                    itemChoices.remove('weapon')
            print('\nYou opened the chest and found {ct} inside'.format(ct=chestTemp))
        elif self.direction[iDirect] == 'opened chest':
            print('\nChest already opened')
        elif self.direction[iDirect] == 'wall':
            print('\nIt\'s a wall...')
        elif self.direction[iDirect] == 'monster':
            dmg = random.randint(0,100)
            if 'weapon' in self.inventory.keys():
                limit = (self.inventory['weapon'] + 5)*10
                if limit == 100:
                    weap = 'MAX lvl sword'
                else:
                    weap = 'lvl{w} sword'.format(w=str(self.inventory['weapon']))
            else:
                limit = 50
                weap = 'fists'
            if dmg < limit:
                self.direction[iDirect] = random.choice(roomChoices)
                print('Your {w} cleave(s) your enemy in twine! You pick up some food from his carcass. There is a {r} behind him'.format(w = weap, r=self.direction[iDirect]))
                self.exp += 10
                try:
                    self.inventory['food'] += 1
                except KeyError:
                    self.inventory['food'] = 1
            else:
                if 'armor' in self.inventory.keys():
                    print('You made it out safe but your armor was damaged')
                    self.inventory['armor'] -= 1
                else:
                    self.health -= 20
                    print('You got hurt and lost 20 HP')
                if self.health <= 0:
                    print('You died')
                    sys.exit()
                else:
                    pass
        elif self.direction[iDirect] == 'friendly stranger':
            if 'money' in self.inventory.keys():
                sItem = random.choice(itemChoices)
                while sItem == 'money':
                    sItem = random.choice(itemChoices)
                tradeYN = input('He says "Would you like to trade one of your money for one of my {i}?"(y/n)'.format(i=sItem))
                if tradeYN == 'y':
                    print('"That\'s great! Here you go"')
                    self.inventory['money'] -= 1
                    try:
                        self.inventory[sItem] += 1
                    except KeyError:
                        self.inventory[sItem] = 1
                    if sItem == 'torch' and 'look_around' not in keywords:
                        keywords.append('look_around')
                        itemChoices.remove('torch')
                    elif sItem == 'weapon':
                        if self.inventory['weapon'] > 5:
                            print('Your weapon is already MAX level')
                            self.inventory['weapon'] -= 1
                        elif self.inventory['weapon'] > 4:
                            print('Your weapon is now MAX level')
                            itemChoices.remove('weapon')
                else:
                    print('"Oh... That\'s OK... I didn\'t need money for my kids or anything... come by later?"')
            elif 'food' in self.inventory.keys():
                folYN = input('He says "for five food I\ll join your party(y/n)" ')
                if folYN == 'y' and self.inventory['food'] > 4:
                    self.inventory['food'] -= 5
                    self.followers.append(random.choice(followerChoices))
            else:
                print('He says "If you stop by with some money you can trade it for some of my goods!"')
        elif self.direction[iDirect] == 'enemy':
            dmg = random.randint(0,100)
            if 'weapon' in self.inventory.keys():
                limit = (self.inventory['weapon'] + 5)*10
                if limit == 100:
                    weap = 'MAX lvl'
                else:
                    weap = 'lvl{w} sword'.format(w=str(self.inventory['weapon']))
            else:
                limit = 50
                weap = 'fists'
            if dmg < limit:
                self.direction[iDirect] = random.choice(roomChoices)
                eItem = random.choice(itemChoices)
                print('Your {w} cleave(s) your enemy in twine! You pick up some {e} from his carcass. There is a {r} behind him'.format(w = weap, e=eItem, r=self.direction[iDirect]))
                self.exp += 10
                if eItem == 'torch' and 'look_around' not in keywords:
                    keywords.append('look_around')
                    itemChoices.remove('torch')
                try:
                    self.inventory[eItem] += 1
                except KeyError:
                    self.inventory[eItem] = 1
                if eItem == 'weapon':
                    if self.inventory['weapon'] > 5:
                        print('Your weapon is already MAX level')
                        self.inventory['weapon'] -= 1
                    elif self.inventory['weapon'] > 4:
                        print('Your weapon is now MAX level')
                        itemChoices.remove('weapon')
            else:
                if 'armor' in self.inventory.keys():
                    print('You made it out safe but your armor was damaged')
                    self.inventory['armor'] -= 1
                else:
                    self.health -= 20
                    print('You got hurt and lost 20 HP')
                if self.health <= 0:
                    print('You died')
                    sys.exit()
                else:
                    pass
    def quit(self):
        qAns = input('Do you really wish to quit?(y/n) ')
        if qAns == 'y':
            sys.exit()
        else:
            system('cls')
    def cheat(*args):
        pass
    def noAction(*args):
        print('That is not a valid action')

inp = ''
nPlayer = player()
system('cls')

def in2():
    kw = input('Hunger |Health |Level  |Exp\n{hg}{hgs}{hp}{hps}{lvl}{lvls}{exp}\nPick an Action: '.format(hg=nPlayer.hunger,
                                                                                     hgs=' '*(7-len(str(nPlayer.hunger)))+'|',
                                                                                     hp=nPlayer.health,
                                                                                     hps=' '*(7-len(str(nPlayer.health)))+'|',
                                                                                     lvl=nPlayer.level,
                                                                                     lvls=' '*(7-len(str(nPlayer.level)))+'|',
                                                                                     exp=nPlayer.exp))
    kw1 = ''
    system('cls')
    if kw == 'cheat':
        cChoice = input('inventory, room, or command? ')
        if cChoice == 'inventory':
            iAdd = input('what do you want to add?')
            try:
                nPlayer.inventory[iAdd] += 1
            except KeyError:
                nPlayer.inventory[iAdd] = 1
        elif cChoice == 'room':
            rChoice = input('Which direction?(north={n}, east={e}, south={s}, west={w})'.format(n=nPlayer.direction['north'], 
                                                                                                e=nPlayer.direction['east'], 
                                                                                                s=nPlayer.direction['south'], 
                                                                                                w=nPlayer.direction['west']))
            nChoice = input('What do you want to change it to? ')
            nPlayer.direction[rChoice] = nChoice
        elif cChoice == 'command':
            comChoice = input('what command do you want to add? ')
            keywords.append(comChoice)
        return 'cheat()'
    elif kw in keywords and kw != 'quit' and kw != 'eat':
        kw, kw1 = kw.split('_')
        return kw+'("'+kw1+'")'
    elif kw == 'eat':
        return kw+'()'
    elif kw == 'quit':
        return kw+'()'
    else:
        return 'noAction()'

while True:
    try:
        if 'eat' in keywords and nPlayer.inventory['food'] > 0:
            pass
        elif 'eat' not in keywords and nPlayer.inventory['food'] > 0:
            keywords.append('eat')
    except KeyError:
        if 'eat' in keywords:
            keywords.remove('eat')
    if 0 < len(nPlayer.followers):
        keywords.append('look_followers')
    elif 0 == len(nPlayer.followers):
        if 'look_followers' in keywords:
            keywords.remove('look_followers')
    if nPlayer.exp >= 100:
        nPlayer.exp -= 100
        nPlayer.maxHealth += 10
        nPlayer.health = nPlayer.maxHealth
        nPlayer.level += 1
    if nPlayer.hunger == 0:
        print('You died of hunger')
        sys.exit()
    else:
        nPlayer.hunger -= 1
    inp = in2()
    if eval('nPlayer.'+inp):
        print('\n'+eval('nPlayer.'+inp))
    else:
        pass
    newKeys = []
    for x in nPlayer.inventory.keys():
        if nPlayer.inventory[x] == 0:
            newKeys.append(x)
    for x in newKeys:
        nPlayer.inventory.pop(x, None)