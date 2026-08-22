from abc import ABC, abstractmethod

class Item(ABC):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @abstractmethod
    def use(self, user):
        pass

class Bandage(Item):

    def use(self, user):
        user.hp += 20
        print(f"{user.name} used {self.name}!")

class Weapon(Item):

    def __init__(self, name, value, damage):
        super().__init__(name, value)
        self.damage = damage

    def use(self, user):
        print(f"{self.name} equipped! Damage: {self.damage}")

class Character:

    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)

    def use_item(self, index):
        try:
            self.inventory[index].use(self)
        except IndexError:
            print("You don't have this item!")

    def remove_item(self, index):
        try:
            self.inventory.pop(index)
        except IndexError:
            print("You don't have this item!")

    def show_inventory(self):
        print(f"--- INVENTORY ---")
        for index, item in enumerate(self.inventory, start=1):
            print(f"{index}. {item.name}: ${item.value}")

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, 100))

player = Character("Alexi Laiho")

weapon = Weapon("ESP LTD Alexi Laiho Signature", 500, 50)
bandage = Bandage("Bandage", 10)

player.add_item(bandage)
player.add_item(weapon)

player.show_inventory()
