" exercise #200 from PyBites, hasn't been refactored, a practice for webscraping to get sorted imformation one needs"
from pathlib import Path
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup

out_dir = "D://"
html_file = f"{out_dir}/enchantment_list_pc.html"

HTML_FILE = Path(html_file)
URL = "https://www.digminecraft.com/lists/enchantment_list_pc.php"


def get_soup(file=HTML_FILE):
    if isinstance(file, Path):
        if not HTML_FILE.is_file():
            urlretrieve(URL, HTML_FILE)

        with file.open() as html_source:
            soup = Soup(html_source, 'html.parser')
    else:
        soup = Soup(file, 'html.parser')

    return soup


class Enchantment:
    """Minecraft enchantment class
    """

    ROMAN_TO_INT = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5}
    TRICKY_ITEMS = {('fishing', 'rod'): 'fishing rod'}

    def __init__(self, id_name, name, max_level, description, items=[]):
        self.id_name = id_name
        self.name = name.rstrip(')').split('(')[0]
        self.max_level = self.ROMAN_TO_INT[max_level]
        self.description = description
        self.items = items

        try:
            for key in self.TRICKY_ITEMS.keys():
                for i in key:
                    self.items.remove(i)
                self.items.append(self.TRICKY_ITEMS[key])
        except ValueError:
            pass

    def __str__(self):
        return f'{self.id_name.capitalize()} ({self.max_level}): {self.description}'

class Item:
    """Minecraft enchantable item class
    """

    def __init__(self, name):
        self.name = name
        self.enchantments = []

    def __str__(self):
        return f'{self.name.title()}:\n' + '\n'.join(f'\t[{x.max_level}] {x.id_name}'
                        for x in sorted(self.enchantments, key=lambda x: x.id_name))


def generate_enchantments(soup):
    """Generates a dictionary of Enchantment objects

    With the key being the id_name of the enchantment.
    """
    import re
    NO_ITEMS = {'enchantments', 'sm', 'enchanted', 'iron'}
    pattern = re.compile(r"images/(?P<items>[^.]+)")
    match = lambda item: [x.replace(' ', '_') for x in re.search(pattern, item)['items'].split('_') if x not in NO_ITEMS]
    get_id_name = lambda item: item.em.get_text()
    return {get_id_name(item): Enchantment(get_id_name(item), *item.get_text().strip().split('\n')[:3], match(item.img['data-src'])) for item in soup.find_all('tr')[1:]}


def generate_items(data):
    """Generates a dictionary of Item objects

    With the key being the item name.
    """
    item_dict = {}
    for enc in data.values():
        for key in enc.items:
            if key not in item_dict:
                item_dict[key] = Item(key)

            item_dict[key].enchantments.append(enc)
    return {key: item_dict[key] for key in sorted(item_dict.keys())}


def main():
    """This function is here to help you test your final code.

    Once complete, the print out should match what's at the bottom of this file"""
    soup = get_soup()
    enchantment_data = generate_enchantments(soup)
    minecraft_items = generate_items(enchantment_data)
    for item in minecraft_items:
        print(minecraft_items[item], "\n")


main()




"""
output would be like this
Armor:
	[1] binding_curse
	[4] blast_protection
	[4] fire_protection
	[4] projectile_protection
	[4] protection
	[3] thorns 

Axe:
	[5] bane_of_arthropods
	[5] efficiency
	[3] fortune
	[5] sharpness
	[1] silk_touch
	[5] smite 

Boots:
	[3] depth_strider
	[4] feather_falling
	[2] frost_walker 

Bow:
	[1] flame
	[1] infinity
	[5] power
	[2] punch 

Chestplate:
	[1] mending
	[3] unbreaking
	[1] vanishing_curse 

Crossbow:
	[1] multishot
	[4] piercing
	[3] quick_charge 

Fishing Rod:
	[3] luck_of_the_sea
	[3] lure
	[1] mending
	[3] unbreaking
	[1] vanishing_curse 

Helmet:
	[1] aqua_affinity
	[3] respiration 

Pickaxe:
	[5] efficiency
	[3] fortune
	[1] mending
	[1] silk_touch
	[3] unbreaking
	[1] vanishing_curse 

Shovel:
	[5] efficiency
	[3] fortune
	[1] silk_touch 

Sword:
	[5] bane_of_arthropods
	[2] fire_aspect
	[2] knockback
	[3] looting
	[1] mending
	[5] sharpness
	[5] smite
	[3] sweeping
	[3] unbreaking
	[1] vanishing_curse 

Trident:
	[1] channeling
	[5] impaling
	[3] loyalty
	[3] riptide 


Process finished with exit code 0

"""