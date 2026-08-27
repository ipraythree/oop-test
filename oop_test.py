from abc import ABC, abstractmethod
import random

class Item(ABC):

    def __init__(self, name, value):
        self.name = name
        self.value = value

class Consumable(Item, ABC):
    @abstractmethod
    def use(self, user):
        pass


class Bandage(Consumable):

    def use(self, user):
        if user.hp == 100:
            print("Your health is already full!")
            return
        else:
            user.hp += 15
            print(f"{self.name} used! Hp: {user.hp}")
            user.remove_item(self)

class Weapon(ABC):

    def __init__(self, name, value, damage):
        self.name = name
        self.value = value
        self.damage = damage

class Guitar(Weapon):

    def __init__(self, name, value, damage):
        super().__init__(name, value, damage)

class Character:

    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp
        self.inventory = []
        self.selected_weapon = None

    def add_item(self, item):
        self.inventory.append(item)

    def use_item(self, index):
        try:
            self.inventory[index].use(self)
        except IndexError:
            print("You don't have this item!")

    def remove_item(self, item):
        try:
            self.inventory.remove(item)
        except ValueError:
            print("You don't have this item!")

    def show_inventory(self):
        print(f"--- INVENTORY ---")
        for index, item in enumerate(self.inventory, start=1):
            print(f"{index}. {item.name}: ${item.value}")

    def fight(self, target):

        damage = random.randint(5, 30)

        if self.selected_weapon:
            damage += self.selected_weapon.damage

        target.hp -= damage

        if target.hp <= 0:
            print(f"You dealt {damage}!")
            print(f"{target.name} died!")
        else:
            print(f"You dealt {damage} damage to {target.name}!")
            print(f"{target.name}'s Remaining hp: {target.hp}")

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, 100))

class Enemy(ABC):
    def __init__(self, name, hp, min_damage, max_damage):
        self.name = name
        self.hp = hp
        self.min_damage = min_damage
        self.max_damage = max_damage

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, 100))

    @abstractmethod
    def attack(self, target):
        pass

class Zombie(Enemy):

    def attack(self, target):
        damage = random.randint(self.min_damage, self.max_damage)
        target.hp -= damage
        print(f"{self.name} attacked you! Remaining health: {target.hp}")

class Skeleton(Enemy):

    def attack(self, target):
        damage = random.randint(self.min_damage, self.max_damage)
        target.hp -= damage
        print(f"{self.name} attacked you! Remaining health: {target.hp}")

class Bandit(Enemy):

    def attack(self, target):
        damage = random.randint(self.min_damage, self.max_damage)
        target.hp -= damage
        print(f"{self.name} attacked you! Remaining health: {target.hp}")

zombie = Zombie("Zombie", 100, 5, 20)
skeleton = Skeleton("Skeleton", 100 ,3 ,15)
bandit = Bandit("Bandit", 100, 9, 35)

player = Character("Alexi Laiho")

guitar = Guitar("ESP LTD Alexi Laiho Signature", 500, 20)
bandage = Bandage("Bandage", 10)

player.add_item(guitar)
player.add_item(bandage)

def item_use():
    player.show_inventory()
    try:
        item_choice = int(input("Which item do you want to use?: "))
        item_choice -= 1
        player.use_item(item_choice)

    except ValueError:
        print("Please choose from the list!")

def equip_item():
    if player.inventory:
        for index, item in enumerate(player.inventory, start=1):
            if isinstance(item, Weapon):
                print(f"{index}. {item.name}: ${item.value}, Damage: {item.damage}")
            else:
                print(f"{index}. {item.name}: ${item.value}")

        try:
            choice = int(input("Which item do you want to equip?: "))
            choice -= 1
            selected_item = player.inventory[choice]

            if isinstance(selected_item, Weapon):
                player.selected_weapon = selected_item
                print(f"{selected_item.name} equipped!")
            else:
                print("You can't equip this item!")

        except (ValueError, IndexError):
            print("Please choose a valid item!")
    else:
        print("You don't have any items!")

def unequip_item():
    if player.selected_weapon:
        print(f"Successfully unequipped {player.selected_weapon.name}!")
        player.selected_weapon = None
    else:
        print("You don't have any equipped item!")


def show_options():
    print("1. Use item\n2. Fight\n3- Equip Item\n4- Unequip Item")

enemies = [
    zombie,
    skeleton,
    bandit
]

def choose_enemy():
    print("--- ENEMIES ---")

    for index, enemy in enumerate(enemies, start=1):
        print(f"{index}. {enemy.name}: {enemy.hp} HP")

    try:
        choice = int(input("Which enemy do you want to attack?: "))
        choice -= 1

        return enemies[choice]

    except (ValueError, IndexError):
        print("Please choose a valid enemy!")
        return None

while True:
    if player.hp > 0:

        show_options()

        choice = input("Enter your choice: ")

        if choice == "1":
            item_use()

        elif choice == "2":

            enemy = choose_enemy()
            if enemy:
                player.fight(enemy)

                if enemy.hp > 0:
                    enemy.attack(player)

                    if player.hp <= 0:
                        print("You are dead, game over!")
                        break

                else:
                    print(f"{enemy.name} is dead!")
                    enemies.remove(enemy)

                    if not enemies:
                        print("All enemies defeated!")
                        print("You won!")
                        break

        elif choice == "3":
            equip_item()
        elif choice == "4":
            unequip_item()

    else:
        print("You are dead, game over!")
        break
