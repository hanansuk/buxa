from boozelib import get_blood_alcohol_content, calculate_degradation
import sys
import random
import copy

class Customer:
    '''
    The main class. Contains player attributes as well as
    their main methods.
    '''
    def __init__(self, age=0, weight=140, height=5, sex=True, money = 0, location=None):
        "Initializes a player, and adjusts the attributes to the relevant formulas"
        self.age = int(age)
        self.weight = float(weight * 0.453592)
        self.height = float(height * 30.48)
        try:
            if sex.lower() == "male" or sex.lower() == "m":
                self.sex = False
            elif sex.lower() == "female" or sex.lower() == "f":
                self.sex = True
        except AttributeError:
            self.sex = True
        if location == None:
            self.location = "outside"
        else:
            self.location = location
        self.money = int(money)
        self.level = 0
        self.score = 0

    def enter(self):
        '''
        Determines whether the player can enter the BuXa or not,
        and declines in case the user is not outside or is not eligable
        to enter
        '''
        if self.location == "outside":
            if self.age < 21:
                sys.exit("You're too young, go home!")
            elif self.money < 5 and self.level > 0.4:
                sys.exit("\nYou're broke and drunk, go home!")
            elif self.level > 0.4:
                sys.exit("\nYou're drunk, go home!")
            elif self.money < 5:
                sys.exit("\nYou're broke, go home!")
            else:
                self.location = MainFloor
                print("\nYou're in! You just entered the main floor")
        else:
            print("\nYou're already inside. Are you drunk...?")

    def GoHome(self):
        '''
        Allows the player to go home, only in case they are outside.
        Returns an exception message and ends the game.
        '''
        if self.location == "outside":
            sys.exit("Bye Bye!")
        else:
            print("\nYou'll need to leave the BuXa first!")

    def leave(self):
        '''
        Leaves the BuXa to the outside. Player is only eligable if
        they are inside of the BuXa
        '''
        if self.location != "outside":
            print (f"You just left the BuXa. Hope you had a good time!!! "
            f"Here are some details about your status- "
            f"\nMoney left: {self.money} "
            f"\nBlood Alcohol Level: {round(self.level, 2)} "
            f"\nTotal Score: {self.score}")
            self.location = "outside"
        else:
            print("\nYou're already outside. Are you drunk...?")
            self.location = "outside"
            self.location.location = "outside"

    def MoveRoom(self):
        '''
        This is the method for players to switch rooms
        '''
        room = input('\nWhere would you like to go? \
                    \nOptions: Bar / Main Floor / Lounge / Art Gallery / Restroom\n')
        room = room.title()
        if len(room.split()) > 1:
            room = ''.join(room)
            room = room.replace(" ", "")
        try:
            Customer.location = eval(room)
            self.location = eval(room)
        except NameError:
            print("\nInvalid room")

    def hang(self, weight=None):
        '''
        A method allowing the player to "hang" wherever they currently
        are. Alcohol levels decrease accordingly during this time
        '''
        time = ""
        while not isinstance(time, int):
            time = int(input('\nHow long would you like to hang here? '))
        if weight == None:
            weight = self.weight
        self.time = time
        old_level = self.level
        degradation = calculate_degradation(weight, time) / 100
        if self.level-degradation <= 0:
            self.level = 0
        else:
            self.level -= degradation
        print(f'\nYour blood alcohol level went from {round(old_level, 2)} to {round(self.level, 2)}')

class Area(Customer):
    '''
    A parent class for all of the BuXa areas, and also a child class
    for Customer
    '''
    def __init__(self):
        super().__init__()

    def StealToy(self):
        '''
        This method allows the player to try and steal a toy. The higher the alcohol
        levels are, the bigger the chance is that the player will be caught. there
        is also a random element here
        '''
        if self.level > 0.2:
            alcohol_influence = self.level * 5
        else:
            alcohol_influence = 1
        chance = random.random() * alcohol_influence
        if chance > 0.95:
            sys.exit("\nYou just got caught and kicked out! Remember- stealing and drinking don't go together...")
        else:
            earned = random.randint(10, 100)
            self.score += earned
            print((f"\nSUCCESS! You managed to steal a toy and earned {earned} points."
            f" You now have {self.score} total points"))



class Menu:
    '''
    A class for food, drink and art menus, as well as methods to pull
    items from those menus
    '''
    food_menu = {"Vietnamese_Spring_Roll":(21, 0.8), "Spicy_Vietnamese_Salad":(31, 0.82), "Gyoza":(29, 0.77), "Lettuce_Boats":(29, 0.9),
                      "Mushroom_Bun":(26, 0.75), "Sweet_Bun":(23, 0.95)}
    drink_menu = {"Junmai_Sake":(26, 150, 13), "Goldstar_Beer":(25, 500, 4.7), "Stella_Beer":(29, 330, 5.2), "Merlot_Wine":(32, 180, 13),
                        "Chardonnay_Wine":(31, 180, 14), "Vodka":(35, 40, 40), "Whiskey":(38, 40, 38), "Gin":(36, 40, 42)}
    art_menu = {"Daniel_Donner":80, "Tom_Benado":42, "Guy_Wegner":120, "Tzlil_Dahan":51}

    def buy_food(food_item):
        if Menu.food_menu.get(food_item) == None:
                food_item = food_item.capitalize()
                food_item = food_item.title()
                food_item = food_item.replace(" ", "_")
                food_item = Menu.food_menu.get(food_item)
                return food_item
        else:
            food_item = Menu.food_menu.get(food_item)
            return food_item

    def buy_drink(drink_item):
        if Menu.drink_menu.get(drink_item) == None:
                drink_item = drink_item.capitalize()
                drink_item = drink_item.title()
                drink_item = drink_item.replace(" ", "_")
                drink_item = Menu.drink_menu.get(drink_item)
                return drink_item
        else:
            drink_item = Menu.drink_menu.get(drink_item)
            return drink_item

    def buy_art(art_item):
        if Menu.art_menu.get(art_item) == None:
            art_item = art_item.capitalize()
            art_item = art_item.title()
            art_item = art_item.replace(" ", "_")
            art_item = Menu.art_menu.get(art_item)
            return art_item
        else:
            art_item = Menu.art_menu.get(art_item)
            return art_item

class Bar(Area):
    '''
    Subclass of "Area", containing the methods unique to the bar, such as "drink"
    and "eat"
    '''
    def __init__(self):
        super().__init__()

    def drink(self):
        for key, value in Menu.drink_menu.items():
            print(f'\nItem: {key}, Price: {value[0]}, Volume(ml): {value[1]}, Alcohol Percentage: {value[2]}%')
        item = input('\nWhat would you like to drink?')
        if Menu.buy_drink(item) == None:
            print("\nInvalid item")
            return
        else:
            item = Menu.buy_drink(item)
        cost = item[0]
        volume = item[1]
        percentage = item[2]
        self.level += get_blood_alcohol_content(self.age, self.weight, self.height, self.sex, volume, percentage)
        self.money -= cost
        if self.money <= 0 and self.level >= 1:
                sys.exit("\nYou're broke and drunk - GAME OVER!")
        elif self.level >= 1:
                sys.exit("\nYou're drunk - GAME OVER!")
        elif self.money < 5:
                sys.exit("\nYou're broke - GAME OVER!")
        else:
            print(f"\nCheers! Your blood alcohol level just increased to {round(self.level, 2)}. You have {self.money} dollars left.")

    def eat(self):
        for key, value in Menu.food_menu.items():
            print(f'\nItem: {key}, Price: {value[0]}, Will decrease alcohol by: {round(1 - value[1], 2)}%')
        item = input('\nWhat would you like to eat?')
        if Menu.buy_food(item) == None:
            print("\nInvalid item")
            return
        else:
            item = Menu.buy_food(item)
        decrease = item[1]
        cost = item [0]
        self.level = self.level * decrease
        self.money -= cost
        if self.money <= 0:
                sys.exit("\nYou're broke, - GAME OVER!")
        else:
            print(f"\nBon Appétit! Your blood alcohol level just decreased to {round(self.level, 2)}. You have {self.money} dollars left.")

class MainFloor(Area):
    '''
    Subclass of Area. This is the main room the player enter from the outside
    '''
    def __init__(self):
        super().__init__()

    def dance(self, weight = None):
        '''
        The only unique method for this room is "dance". Allows the user to spend
        some time on the dance floor and decrease alcohol levels
        '''
        time = ""
        while not isinstance(time, int):
            time = int(input('\nHow long would you like to dance? '))
        old_level = self.level
        if weight == None:
            weight = self.weight
        degradation = calculate_degradation(weight, time) / 100
        if self.level-degradation <= 0:
            self.level = 0
        else:
            self.level -= degradation
        print(f"\nHaving a good time, aren't you? Your blood alcohol level just went from {round(old_level, 2)} to {round(self.level, 2)}!")

class Lounge(MainFloor):
    '''
    Subclass of MainFloor. Has the same methods
    '''
    def __init__(self):
        super().__init__()
        self.location = Lounge

class ArtGallery(Area):
    '''
    Subclass of Area. The unique method here allows the player to buy a piece
    of art
    '''
    def __init__(self):
        super().__init__()
        self.location = ArtGallery

    def BuyArt(self):
        for key, value in Menu.art_menu.items():
            print(f'\nItem: {key}, Price: {value}')
        item = input('\nWhich art item would you like to buy? ')
        if Menu.buy_art(item) == None:
            print("\nInvalid item")
            return
        else:
            item = Menu.buy_art(item)
        cost = item
        self.money -= cost
        if self.money <= 0:
                sys.exit("You're broke, - GAME OVER!")
        else:
            print(f"\nEnjoy your piece of art! You have {self.money} dollars left.")

class Restroom(Customer):
    '''
    Subclass of Customer- allows the player to spend some time in the restroom
    and decrease alcohol levels
    '''
    def __init__(self):
        super().__init__()

    def UseRestroom(self, weight = None):
        time = ""
        while not isinstance(time, int):
            time = int(input('How long would you be in the restroom? '))
        old_level = self.level
        if weight == None:
            weight = self.weight
        degradation = calculate_degradation(weight, time) / 100
        if self.level-degradation <= 0:
            self.level = 0
        else:
            self.level -= degradation
        print(f"\nGood job there, I guess... Your blood alcohol level just went from {round(old_level, 2)} to {round(self.level, 2)}!")

class Outside(Customer):
    def __init__(self):
        super().__init__()
        return "outside"

class MainMenu:
    def GameMenu(player):
        '''
        This is the only function that is not inside a class. This is the actual game menu
        that communicates with the player and allows the player to walk through the game
        '''
        print('''\n--------------------------------------------------------\
              \n--------------------------------------------------------\
              \n\nWhat would you like to do next?\
              \nThe options are:''')
        location = player.location
        if location == "outside":
            print('\nEnter / Leave / GoHome')
            object_methods = [method_name for method_name in dir(player) if (callable(getattr(player, method_name)) and method_name[0] != "_")]
        else:
            object_methods_capital = []
            object_methods = [method_name for method_name in dir(location) if (callable(getattr(location, method_name)) and method_name[0] != "_")]
            object_methods_print = copy.copy(object_methods)
            for i in range(0, len(object_methods_print)):
                if object_methods_print[i][0].islower():
                    object_methods_print[i] = object_methods_print[i].capitalize()
            print(" / ".join([i for i in object_methods_print if i.lower() != "location"]))
        action = input('\nEnter action:')
        if location == "outside":
            try:
                getattr(player, action)()
                MainMenu.GameMenu(player)
            except (NameError, AttributeError):
                try:
                    action= action.title()
                    action = action.replace(" ", "")
                    getattr(player, action)()
                    MainMenu.GameMenu(player)
                except (NameError, AttributeError):
                    try:
                        action = action.lower()
                        getattr(location, action)()
                        MainMenu.GameMenu(player)
                    except (NameError, AttributeError):
                            print("\nInvalid action, please enter another action: ")
                            MainMenu.GameMenu(player)
        else:
            if location not in ("outside", "MainFloor") and location.__class__.__name__ != "MainFloor":
                if action in object_methods:
                    getattr(location, action)(player)
                    MainMenu.GameMenu(player)
                else:
                    while action not in object_methods:
                        try:
                            action= action.title()
                            action = action.replace(" ", "")
                            getattr(location, action)(player)
                            MainMenu.GameMenu(player)
                        except (NameError, AttributeError):
                            try:
                                action= action.lower()
                                getattr(location, action)(player)
                                MainMenu.GameMenu(player)
                            except (NameError, AttributeError):
                                print("\nInvalid action, please enter another action: ")
                                MainMenu.GameMenu(player)
            else:
                if action in object_methods:
                    getattr(player.location, action)()
                    MainMenu.GameMenu(player)
                else:
                    while action not in object_methods:
                        try:
                            action= action.title()
                            action = action.replace(" ", "")
                            getattr(player, action)()
                            MainMenu.GameMenu(player)
                        except (NameError, AttributeError):
                            try:
                                action= action.lower()
                                getattr(location, action)(player)
                                MainMenu.GameMenu(player)
                            except (NameError, AttributeError):
                                print("\nInvalid action, please enter another action: ")
                                MainMenu.GameMenu(player)

#The section below starts the actual game

class Initiate:
    def start():
        print('Good night! Welcome to the BuXa. Your goal is to get the highest possible score, \
while not getting too drunk or too broke. You get scored for stealing toys. Keep in mind \
that the more drunk you are, the harder it is to steal!\
\n\nPlease enter some details about yourself:')
#         age, weight, height, money = 30, 170, 5, 500
#         sex = 'male'
        age, weight, height, money = -1, -1, -1, -1
        sex = 'blah'
        while age < 1 or age > 120:
            try:
                age = int(input('\nWhat is your age? '))
            except ValueError:
                print('Please enter a valid age: ')
        while weight < 10 or weight > 1000:
            try:
                weight = float(input('What is your weight? (Lbs.) '))
            except ValueError:
                print('Please enter a valid weight (in Lbs.): ')
        while height < 1 or height > 8:
            try:
                height = float(input('What is your height? (Ft.) '))
            except ValueError:
                print('Please enter a valid height (in Ft.): ')
        while sex.lower() not in ('female', 'male', 'm', 'f'):
            try:
                sex = input('What is your sex? (male/female) ')
            except ValueError:
                print('Please enter a valid sex: ')
        while money < 0 or money >= 1000:
            try:
                money = int(input('How much money you have on you? (5 - 1,000, no dollar sign please) '))
            except ValueError:
                print('Not a valid amount, please enter again: ')
        player = Customer(age, weight, height, sex, money)
        print('\nYou are right outside of the BuXa.')
        MainMenu.GameMenu(player)

Initiate.start()
