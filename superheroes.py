import random

class Hero:
    def __init__(self, name, starting_health=100):
        '''
        Initialize these values as instance variables:
        (Some of these values are passed in above, others will need to be set at a starting value.)
        abilities:List
        name:
        starting_health:
        current_health:
        '''
        self.name = name
        self.starting_health = starting_health
        self.current_health = starting_health
        self.abilities = []
        self.armors = []
        self.deaths = 0
        self.kills = 0

    def add_ability(self, ability):
        ''' Add ability to abilities list '''
        self.abilities.append(ability)

    def attack(self):
        '''
        Calculates damage from list of abilities.

        This method should call Ability.attack()
        on every ability in self.abilities and
        return the total.
        '''
        attack_sum = 0
        for ability in self.abilities:
            attack_sum += ability.attack()
        return attack_sum


    def take_damage(self, damage):
        '''
        This method should update self.current_health
        with the damage that is passed in.
        '''
        self.current_health -= damage - self.defend()

    def is_alive(self):
        '''
        This function will
        return true if the hero is alive
        or false if they are not.
        '''
        if self.current_health <= 0:
            return False
        return True

    def add_kill(self, num_kills):
        self.kills += num_kills

    def add_armor(self, armor):
        ''' Add armor to armors list.'''
        self.armors.append(armor)

    def defend(self):
        '''
        This method should run the block
        method on each piece of armor and
        calculate the total defense.

        If the hero's health is 0
        return 0
        '''
        if self.current_health <= 0:
            return 0
        else:
            block_sum = 0
            for armor in self.armors:
                block_sum += armor.block()
            return block_sum


    def fight(self, opponent):
        '''
        Runs a loop to attack the opponent until someone dies.
        '''
        while opponent.is_alive() and self.is_alive():
            # self attacks opponent
            opponent.take_damage(self.attack())
            self.take_damage(opponent.attack())
            if not opponent.is_alive():
                print(opponent.name, 'was destroyed!')
                opponent.deaths += 1
                self.kills += 1
            # opponent attacks self
            if not self.is_alive():
                print(self.name, 'was destroyed!')
                self.deaths += 1
                opponent.kills += 1


class Ability:
    def __init__(self, name, max_damage):
        '''
        Initialize the values passed into this
        method as instance variables.
         '''
        self.name = name
        self.max_damage = max_damage

    def attack(self):
        '''
        Return a random attack value
        between 0 and max_damage.
        '''
        return random.randint(0, self.max_damage)

class Weapon(Ability):
    def attack(self):
        """
        This method should should return a random value
        between one half to the full attack power of the weapon.
        Hint: The attack power is inherited.
        """
        return random.randint(self.max_damage // 2, self.max_damage)


class Armor:
    def __init__(self, name, max_block):
        '''Instantiate name and defense strength.'''
        self.name = name
        self.max_block = max_block

    def block(self):
        '''
        Return a random value between 0 and the
        initialized max_block strength.
        '''
        return random.randint(0, self.max_block)


class Team:
    def __init__(self, team_name):
        '''Instantiate resources.'''
        self.name = team_name
        self.heroes = []
        self.team_kills = 0


    def add_hero(self, hero):
        '''Add Hero object to heroes list.'''
        self.heroes.append(hero)

    def remove_hero(self, name):
        '''
        Remove hero from heroes list.
        If Hero isn't found return 0.
        '''
        for hero in self.heroes:
            if hero.name == name:
                self.heroes.remove(hero)
                return
        return 0

    def view_all_heroes(self):
        '''Print out all heroes to the console.'''
        for hero in self.heroes:
            print(hero.name)

    def team_alive(self):
        total_health = 0
        for hero in self.heroes:
            if hero.is_alive():
                return True
        return False

    def attack(self, other_team):
        '''
        This function should randomly select
        a living hero from each team and have
        them fight until one or both teams
        have no surviving heroes.

        Hint: Use the fight method in the Hero
        class.
        '''
        one_dead_heroes = []
        two_dead_heroes = []
        while self.team_alive() and other_team.team_alive():
            random.choice(self.heroes).fight(random.choice(other_team.heroes))
            for hero in self.heroes:
                if not hero.is_alive:
                    one_dead_heroes.append(hero)
                    self.heroes.remove(hero)
            for hero in other_team.heroes:
                if not hero.is_alive:
                    two_dead_heroes.append(hero)
                    other_team.remove(hero)
        self.heroes += one_dead_heroes
        other_team.heroes += two_dead_heroes

    def revive_heroes(self):
        '''
        This method should reset all heroes
        health to their
        original starting value.
        '''
        for hero in self.heroes:
            hero.current_health = 100

    def stats(self):
        '''
        This method should print the ratio of
        kills/deaths for each member of the
        team to the screen.

        This data must be output to the console.
        '''
        print("{} stats: ".format(self.name))
        for hero in self.heroes:
            print("{} had kills: {} / deaths: {}".format(hero.name, hero.kills, hero.deaths))
        kills = 0
        deaths = 0
        for hero in self.heroes:
            kills += hero.kills
            deaths += hero.deaths
        print("Total...kills: {} / deaths: {}".format(kills, deaths))

        print("Total kills: " + str(self.team_kills))
class Arena:
    def __init__(self, name):
        """
        Declare variables
        """
        self.team_one = None
        self.team_two = None

    # def data(self):
    #     for hero in self.team_two.heroes:
    #         print(hero.name, hero.current_health)
    #         for ability in hero.abilities:
    #             print(ability.name, ability.max_damage)




    def create_ability(self):
        '''
        This method will allow a user to create an ability.

        Prompt the user for the necessary information to create a new ability object.

        return the new ability object.
        '''
        new_ability_name = input("Enter ability name: ")
        new_ability_strength = input("Enter {}'s strength: ".format(new_ability_name))
        if str(new_ability_strength) != new_ability_strength:
            while int(new_ability_strength) == new_ability_strength:
                new_ability_strength = input("Enter valid strength for {} (int): ".format(new_ability_name))
        new_ability = Ability(new_ability_name, int(new_ability_strength))
        return new_ability

    def create_weapon(self):
        new_weapon_name = input("Enter weapon name: ")
        new_weapon_strength = input("Enter {}'s strength: ".format(new_weapon_name))
        if str(new_weapon_strength) != new_weapon_strength:
            while int(new_weapon_strength) == new_weapon_strength:
                new_weapon_strength = input("Enter valid strength for {} (int): ".format(new_weapon_name))
        new_weapon = Ability(new_weapon_name, int(new_weapon_strength))
        return new_weapon


    def create_armor(self):
        '''
        This method will allow a user to create a piece of armor.

        Prompt the user for the necessary information to create a new armor object.

        return the new armor object.
        '''

        new_armor_name = input("Enter armor name: ")
        new_armor_strength = input("Enter {}'s block strength: ".format(new_armor_name))
        if str(new_armor_strength) != new_armor_strength:
            while int(new_armor_strength) == new_armor_strength:
                new_armor_strength = input("Enter valid block strength for {} (int): ".format(new_armor_name))
        new_armor = Armor(new_armor_name, int(new_armor_strength))
        return new_armor

    def create_hero(self):
        '''
        This method should allow a user to create a hero.

        User should be able to specify if they want armors, weapons, and abilites. Call the methods you made above and use the return values to build your hero.

        return the new hero object
        '''

        hero_name = input("Enter your hero's name: ")
        hero = Hero(hero_name)

        if self.yesNo("Would you like to add an ability to {}?".format(hero_name)):
            ability = self.create_ability()
            hero.add_ability(ability)
        if self.yesNo("Would you like to add a weapon to {}?".format(hero_name)):
            weapon = self.create_weapon()
            hero.add_ability(weapon)

        if self.yesNo("Would you like to add an armor to {}?".format(hero_name)):
            armor = self.create_armor()
            hero.add_armor(armor)
        return hero


    def yesNo(self, prompt):
        inp = input(prompt)
        if inp in "YyNn":
            if inp in "Yy":
                return True
            else:
                return False
        else:
            print("Invalid input")
            return self.yesNo(prompt)

    def build_team_one(self):
        '''
        This method should allow a user to create team one.
        Prompt the user for the number of Heroes on team one and
        call self.create_hero() for every hero that the user wants to add to team one.

        Add the created hero to team one.
        '''
        print("Building team one...")
        team_name = input("Enter your teams name: ")
        team_one = Team(team_name)
        continue_adding = True
        while continue_adding:
            new_hero = self.create_hero()
            team_one.add_hero(new_hero)
            continue_adding = self.yesNo("Would you like to add another hero to {}? (y/n)".format(team_name))
        self.team_one = team_one
        return team_one

    def build_team_two(self):
        '''
        This method should allow a user to create team two.
        Prompt the user for the number of Heroes on team two and
        call self.create_hero() for every hero that the user wants to add to team two.

        Add the created hero to team two.
        '''

        print("Building team two...")
        team_name = input("Enter your teams name: ")
        team_two = Team(team_name)
        continue_adding = True
        while continue_adding:
            new_hero = self.create_hero()
            team_two.add_hero(new_hero)
            continue_adding = self.yesNo("Would you like to add another hero to {}? (y/n)".format(team_name))
        self.team_two = team_two
        return team_two

    def team_battle(self):
        '''
        This method should battle the teams together.
        Call the attack method that exists in your team objects to do that battle functionality.
        '''
        self.team_one.attack(self.team_two)






    def show_stats(self):
        '''
        This method should print out battle statistics
        including each team's average kill/death ratio.

        Required Stats:
        Declare winning team
        Show both teams average kill/death ratio.
        Show surviving heroes.
        '''


        kills = 0
        deaths = 0
        for hero in self.team_one.heroes:
            print("{} had {} kill(s) and {} death(s).".format(hero.name, hero.kills, hero.deaths))
            kills += hero.kills
            deaths += hero.deaths
        print("{} had a total of {} kill(s) and {} death(s).".format(self.team_one.name, kills, deaths))

        kills = 0
        deaths = 0
        for hero in self.team_two.heroes:
            print("{} had {} kill(s) and {} death(s).".format(hero.name, hero.kills, hero.deaths))
            kills += hero.kills
            deaths += hero.deaths
        print("{} had a total of {} kill(s) and {} death(s).".format(self.team_two.name, kills, deaths))






if __name__ == "__main__":
    game_is_running = True

    # Instantiate Game Arena
    arena = Arena("name")
    #Build Teams
    arena.build_team_one()
    arena.build_team_two()

    while game_is_running:


        arena.team_battle()
        arena.show_stats()
        play_again = input("Play Again? Y or N: ")

        #Check for Player Input
        if play_again.lower() == "n":
            game_is_running = False

        else:
            #Revive heroes to play again
            arena.team_one.revive_heroes()
            arena.team_two.revive_heroes()
