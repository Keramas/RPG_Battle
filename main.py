from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Spells usable by the player
# Offensive spells:
staticBurst = Spell("Static Burst", 25, 600, "black")
gravitonCannon = Spell("Graviton Cannon", 250, 600, "black")
bash = Spell("Bash", 25, 600, "black")
electromagneticWave = Spell("Electromagnetic Wave", 40, 1200, "black")
systemOverload = Spell("System Overload", 14, 140, "black")

# Healing spells:
refresh = Spell("Refresh", 25, 620, "white")
refresh2 = Spell("Refresh II", 32, 1500, "white")
refresh3 = Spell("Refresh III", 50, 6000, "white")

# Spells usable by enemies
# Offensive spells:
sixShot = Spell("Static Burst", 25, 600, "black")
quickDraw = Spell("Graviton Cannon", 250, 600, "black")
chargedShot = Spell("Bash", 25, 600, "black")
dustEye = Spell("Electromagnetic Wave", 40, 1200, "black")
hackTech = Spell("System Overload", 14, 140, "black")

# Create items
potion = Item("Tonic", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-tonic", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Tonic", "potion", "Heals 1000 HP", 1000)
elixir = Item("Nano Lubricant", "elixir", "Fully restores HP/MP of one party member", 9999)
megaelixir = Item("Super Nano Lubricant", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Thermobomb", "attack", "Deals 500 damage", 500)

player_spells = [staticBurst, gravitonCannon, bash, electromagneticWave, systemOverload, refresh, refresh2, refresh3]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixir, "quantity": 5},
                {"item": megaelixir, "quantity": 2},
                {"item": grenade, "quantity": 5}]

enemy_spells = [sixShot, quickDraw, chargedShot, dustEye, hackTech]
boss_spells = [sixShot, quickDraw, chargedShot, dustEye, hackTech]

# Instantiate People
player1 = Person("Talos", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Rose ", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Jin  ", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person("Goon ", 1250, 999999, 560, 325, enemy_spells, [])
enemy2 = Person("Vex  ", 18200, 999999, 525, 25, enemy_spells, [])
enemy3 = Person("Goon ", 1250, 999999, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print("==================================================================================")
print("           01010100 01110010 01110101 01100101  01000010 01101001 01110100")
print("                          _____                ______ _ _ ")
print("                         |_   _|               | ___ (_) | ")
print("                           | |_ __ _   _  ___  | |_/ /_| |_")
print("                           | | '__| | | |/ _ \ | ___ \ | __|")
print("                           | | |  | |_| |  __/ | |_/ / | |_")
print("                           \_/_|   \__,_|\___| \____/|_|\__|")
print("           01010100 01110010 01110101 01100101  01000010 01101001 01110100")
print("                                                                                  ")
print("==================================================================================")

print("\n")
print("==================================================================================")
print(bcolors.FAIL + bcolors.BOLD + "Add story text here"
      + bcolors.ENDC)
print(bcolors.FAIL + bcolors.BOLD + "Add story text here!"
      + bcolors.ENDC)
print("==================================================================================")

print("\n")

# Player character stat UI
while running:
    print("PARTY MEMBERS")
    print("===========================================================================================================")

    print("NAME                 HP                                                                 MP")
    for player in players:
        player.get_stats()

    print("===========================================================================================================")
    print("\n")

    print("ENEMIES")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("\n" + "You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print("\n" + enemies[enemy].name.replace(" ", "") + " has been defeated.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name, " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " +
                      enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print("\n" + enemies[enemy].name.replace(" ", "") + " has been defeated.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_items()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixir":

                if item.name == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " +
                      enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print("\n" + enemies[enemy].name.replace(" ", "") + " has been defeated.")
                    del enemies[enemy]

    print("\n")

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, (len(players)))
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print("\n" + enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for",
                  enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print("\n" + bcolors.OKBLUE + spell.name + " heals " + enemy.name + " for", str(magic_dmg),
                      "HP." + bcolors.ENDC)
            elif spell.type == "black":

                target = random.randrange(0, (len(players)))

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals",
                      str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print("\n" + players[target].name.replace(" ", "") + " has died.")
                    del players[target]

    print("\n")

    # Check is battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    # Check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False
