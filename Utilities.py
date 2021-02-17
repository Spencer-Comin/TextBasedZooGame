import random


FPS = 5


def neighbours(pos, dist=1):
    x, y = pos
    if dist == 1:
        return {(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)}
    built = set()
    # obviously this is the absolute worst way to do this, but generally dist < 5
    for x in neighbours(pos, dist=dist-1):
        built |= neighbours(x)
    return built - {pos}


names = ['Abella', 'Anaïs', 'Astoria', 'Azura', 'Berlin', 'Blanca', 'Blue', 'Callista', 'Devina', 'Dove',
         'Eugenia', 'Fern', 'Fleur', 'Jessalyn', 'Juna', 'Kani', 'Keva', 'Lake', 'Lavender', 'Lira', 'Lotte',
         'Lourdes', 'Mariposa', 'Maude', 'Maven', 'Minerva', 'Moxie', 'Nairobi', 'Nella', 'Nikita', 'Oceana',
         'Olympia', 'Peace', 'Philomena', 'Psalm', 'Ravenna', 'Rebel', 'Rome', 'Rosella', 'Sahar', 'Starla',
         'Suzette', 'Terra', 'Thora', 'Uma', 'Venice', 'Victory', 'Vita', 'Zen', 'Zoelle', 'Art', 'Booker',
         'Brave', 'Buster', 'Camp', 'Chauncey', 'Ciel', 'Claude', 'Clinton', 'Cloud', 'Cornelius', 'Cyprus',
         'Darwin', 'Dex', 'Diogo', 'Echo', 'Emile', 'Everson', 'Fidel', 'Francois', 'Golden', 'Hamilton',
         'Hansel', 'Hasani', 'Holland', 'Indigo', 'Jovian', 'Judd', 'June', 'Jupiter', 'Keane', 'Leyton', 'Mace',
         'Mckinley', 'Navy', 'Niles', 'Octavius', 'Oden', 'Raven', 'Red', 'Rhythm', 'Snow', 'Stellan', 'Sven',
         'Tegan', 'Wellington', 'Wendell', 'Wolfe', 'Woodrow', 'Yanis']

animalNames = ['Boo-boo', 'Abby', 'Houdini', 'Dreamer', 'Amos', 'Maggie-mae', 'Tucker', 'Linus', 'Clover', 'Silky',
               'Lucky', 'Dallas', 'Luna', 'Stanley', 'Topaz', 'Yukon', 'Tara', 'Bogey', 'Sampson', 'Blondie', 'Lola',
               'Nickers', 'Diamond', 'Connor', 'Edsel', 'Amigo', 'Scooby-doo', 'Nikita', 'Nellie', 'Gracie', 'Bandit',
               'Bridgette', 'Andy', 'Alfie', 'Nero', 'Scottie', 'Pinto', 'Cujo', 'Julius', 'Apollo', 'Wrinkles',
               'Figaro', 'Kyra', 'Roxie', 'Lilly', 'Bullet', 'Nike', 'Puffy', 'Mugsy', 'Sierra', 'Yang', 'Luke',
               'Scooter', 'Pearl', 'Rebel', 'Savannah', 'Cleopatra', 'Benji', 'Whiskers', 'Rosy', 'Cheyenne', 'Happyt',
               'Mollie', 'Butchy', 'Ruger', 'Sissy', 'Laddie', 'Jags', 'Cody', 'Mittens', 'Gromit', 'Speedy', 'Dempsey',
               'Rico', 'Darcy', 'Faith', 'Oscar', 'Katie', 'Zorro', 'Daffy', 'Kobe', 'Humphrey', 'Josie', 'Norton',
               'Lily', 'Tori', 'Wiggles', 'Puck', 'Barnaby', 'Muffin', 'Fritz', 'Tracker', 'Tiger', 'Missy', 'Lexie',
               'Koba', 'Mister', 'Elvis', 'Mason', 'Brandi', 'Carley', 'Rosebud', 'Harpo', 'Tiki', 'Mojo', 'Mariah',
               'Buttercup', 'Gretel', 'Walter', 'Sonny', 'Patty', 'Punkin', 'Kira', 'Miasy', 'Elwood', 'Millie', 'Tank',
               'Mcduff', 'Newton', 'Klaus', 'Chewy', 'Twiggy', 'Freedom', 'Sunny', 'BB', 'Pooch', 'Basil', 'Rocket',
               'Nena', 'Jazz', 'Birdy', 'Harvey', 'Lili', 'Sheena', 'Timmy', 'Wilson', 'Biablo', 'Rexy', 'Napoleon',
               'Bailey', 'Budda', 'Bo', 'Pooh', 'Scarlett', 'Dutchess', 'Paris', 'Ember', 'Roland', 'Shorty', 'Dodger',
               'Mango', 'Skye', 'Georgie', 'Zeus', 'Winnie', 'Gidget', 'Franky', 'Lincoln', 'Isabelle', 'Doogie',
               'Marble', 'Rex', 'Judy', 'Guy', 'Jingles', 'Polly', 'Niko', 'Hooch', 'Bernie', 'Mimi', 'Thyme',
               'Tinkerbell', 'Monkey', 'Eddie', 'Fresier', 'Dusty', 'Snuffles', 'Indy', 'Dee Dee', 'Dolly', 'Mary Jane',
               'Sweet-pea', 'Starr', 'Sasha', 'Dee', 'Pixie', 'Garfield', 'Tipr', 'Reggie', 'Wrigley', 'Bizzy', 'KC',
               'Meggie', 'Presley', 'Piglet', 'Emily', 'May', 'Lizzy', 'Baxter', 'Ivy']

names_in_use = set()


def get_name(animal=False):
    if animal:
        name = random.choice(animalNames)
        while name in names_in_use:
            name = random.choice(animalNames)
    else:
        name = random.choice(names)
        while name in names_in_use:
            name = random.choice(names)
    names_in_use.add(name)
    return name


def add_name(name, animal=False):
    if animal:
        animalNames.append(name)
    else:
        names.append(name)
    if name in names_in_use:
        names_in_use.remove(name)
