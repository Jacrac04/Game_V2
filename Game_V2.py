# Help me
# Class for Interactable
#   Class for NPC
#      Class for Good Guy
#      Class for Bad Guy
#   Class for Objects
# Class for Player 
# Class for Places

import random
import pickle

# Anythong the player can interact with
class Interactable():
    def __init__(self,name,description):
        self.name = name
        self.description = description
    
    def __str__(self):
        return f'{self.name}: {self.description}'

# class for objects inheriting from interactable
class Object(Interactable):
    def __init__(self,name,description,location):
        Interactable.__init__(self,name,description)
    def interact(self,player):
        print(f'You look at the {self.name}. {self.description}')
        if len(player.inventory) < 0:
            print(f'You can pick it up.')
        else:
            print(f'You cant pick it up.')
    

    

# NPC Class inheriting from Interactable
class NPC(Interactable):
    def __init__(self,name,description,friendly,inventory=[]):
        Interactable.__init__(self,name,description)
        self.friendly = friendly
        self.inventory = inventory

# class for Good Guy inheriting from NPC
class GoodGuy(NPC):
    def __init__(self,name,description):
        NPC.__init__(self,name,description,True)
    def interact(self,player):
        print(f'Hello I am {self.name} and I am friendly')

# class for Bad Guy inheriting from NPC
class BadGuy(NPC):
    def __init__(self,name,description):
        NPC.__init__(self,name,description,False)
    def interact(self,player):
        print(f'Hello I am {self.name} and I am not friendly')




class Player():
    name = ''
    strenght = 0
    knowledge = 0
    luck = 0
    inventory = []

    def __init__(self):
            print('What is your name?')
            self.name = input()
            print('Do you want to be strong(s) or knowledgeable(k)?')
            choice = input()
            if choice == 's':
                self.strenght = random.randint(70,100)
                self.knowledge = random.randint(50,90)
            elif choice == 'k':
                self.knowledge = random.randint(70,100)
                self.strenght = random.randint(50,90)
            else:
                print('Invalid choice, so you wil have random atributes')
                self.strenght = random.randint(50,80)
                self.knowledge = random.randint(50,80)
            print('Press enter to roll the dice to determine you luck...')
            input()
            self.luck = random.randint(1,10)
            print(f'Your name is {self.name} and you have {self.strenght} strenght, {self.knowledge} knowledge and {self.luck} luck')
    
    def __str__(self):
        return f'{self.name}'

# class for the Places 
class Place():
    def __init__(self,name,description,stroyline,interactables = []):
        self.name = name
        self.description = description
        self.stroyline = stroyline
        self.interactables = interactables

    # Methord used during creation of the map to add interactables to places
    def addInteractable(self,interactable):
        self.interactables.append(interactable)
    
    def __str__(self):
        return f'Place {self.name}: {self.description} where you can find {self.interactables}'

    @staticmethod
    def interactableOptions(interactables):
        possibleInteractables = []
        for interactable in interactables:
            possibleInteractables.append(interactable.name)
        toPrint = ', '.join(possibleInteractables)
        return toPrint
        
    def arrived(self,player):
        print(f'You have arrived at {self.name}')
        print(f'{self.stroyline}')
        print(f'You can see {self.interactableOptions(self.interactables)}')
        interact = True
        while interact:
            interacted = False
            print('What do you want to interact with, or you can pass(p)?')             
            choice = input()
            for interactable in self.interactables:
                if interactable.name == choice:
                    interactable.interact(player)
                    interacted = True
                    break
            if not interacted:
                interact = False

            



# class for maps containing places
class Map():
    def __init__(self,places):
        self.places = places
        
    def __str__(self):
        return f'Map: {self.places}'

    @classmethod
    def createMap(cls):
        # Create places
        start = Place('Start','You are at the start', 'You are at the start of the game')
        forest = Place('Forest','You are in the forest', 'You are in the forest')
        cave = Place('Cave','You are in the cave', 'You are in the cave')
        house = Place('House','You are in the house', 'You are in the house')
        # Create objects
        sword = Object('Sword','You found a sword',start)
        key = Object('Key','You found a key',cave)
        # Create NPCs
        badguy = BadGuy('Bad Guy','You have encountered a bad guy')
        goodguy = GoodGuy('Good Guy','You have encountered a good guy')
        # Add objects to places
        start.addInteractable(sword)
        cave.addInteractable(key)
        # Add NPCs to places
        forest.addInteractable(badguy)
        house.addInteractable(goodguy)
        # Create map
        map = Map([start,forest,cave,house])
        return map
    @classmethod
    def createMapFromFile(cls):
        with open('map.pickle','rb') as f:
            map = pickle.load(f)
        return map

# constructor for maps from file using pickle
def mapConstructorFromFile():
    pass

def mapConstructor():
    places = []
    place1 = Place('place1','This is place 1', 'This is the storyline for place 1')
    place2 = Place('place2','This is place 2', 'This is the storyline for place 2')
    place3 = Place('place3','This is place 3', 'This is the storyline for place 3')
    places.append(place1)
    places.append(place2)
    places.append(place3)
    friend = GoodGuy('Joe','He is friendly')
    friend2 = GoodGuy('Bob','He is friendly')
    friend3 = GoodGuy('Sally','She is friendly')
    badGuy = BadGuy('Bob2','He is not friendly')
    #print(friend)
    #friend.interact()
    place1.addInteractable(friend)
    place1.addInteractable(friend2)
    place1.addInteractable(friend3)
    place2.addInteractable(badGuy)

    return Map(places)

def savePlayerData(player:object):
    fileName = f'{player.name}.pickle'
    with open(f'saveFiles/{fileName}', 'wb') as f:
        pickle.dump(player,f)

def loadPlayerData(playerName:str):
    try:
        fileName = f'{playerName}.pickle'
        with open(f'saveFiles/{fileName}', 'rb') as f:
            player = pickle.load(f)
        return player
    except:
        print('No save file found')
        return None

class Game():
    player = None
    map = None
    def __init__(self):
        pass
    def createPlayer(self):
        print('Do you want to load a player(l) or create a new one(n)?')
        choice = input()
        if choice == 'l':
            print('What is the name of the player?')
            playerName = input()
            self.player = loadPlayerData(playerName)
        elif choice == 'n':
            self.player = Player()
            savePlayerData(self.player)
    def makeMap(self):
        #gameMap = mapConstructor()
        self.map = Map.createMap()
        self.map.places[0].arrived(self.player) 


game = Game()
game.createPlayer()
game.makeMap()





#print(mapConstructor().places[0].interactables[0].name)