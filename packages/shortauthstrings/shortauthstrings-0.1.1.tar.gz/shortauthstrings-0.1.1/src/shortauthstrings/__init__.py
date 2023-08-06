"""
This package implements rendering of short authenticated strings, which you
can use in your application after an unauthenticated exchange such as a
Diffie-Hellman process.  The usual way in which this works is, both sides
of the exchange display (hopefully) the same sequence based on the shared
key (or a derivative of it), indicating that the shared key is, in fact,
shared.

All functions in this package take:

1. A key or some other secret shared between the parties, in bytes form.
2. A length of glyphs / words / pictograms you'll get.

No cryptography is done in this package.
"""

from typing import Optional

__version__ = "0.1.1"

# From https://github.com/urbit/urbit/blob/7ce50ad75e23fcec0c8cb6ad60369b2515657a89/pkg/arvo/sys/hoon.hoon#L4038-L4053

URBIT_PREFIXES = """dozmarbinwansamlitsighidfidlissogdirwacsabwissib
rigsoldopmodfoglidhopdardorlorhodfolrintogsilmir
holpaslacrovlivdalsatlibtabhanticpidtorbolfosdot
losdilforpilramtirwintadbicdifrocwidbisdasmidlop
rilnardapmolsanlocnovsitnidtipsicropwitnatpanmin
ritpodmottamtolsavposnapnopsomfinfonbanmorworsip
ronnorbotwicsocwatdolmagpicdavbidbaltimtasmallig
sivtagpadsaldivdactansidfabtarmonranniswolmispal
lasdismaprabtobrollatlonnodnavfignomnibpagsopral
bilhaddocridmocpacravripfaltodtiltinhapmicfanpat
taclabmogsimsonpinlomrictapfirhasbosbatpochactid
havsaplindibhosdabbitbarracparloddosbortochilmac
tomdigfilfasmithobharmighinradmashalraglagfadtop
mophabnilnosmilfopfamdatnoldinhatnacrisfotribhoc
nimlarfitwalrapsarnalmoslandondanladdovrivbacpol
laptalpitnambonrostonfodponsovnocsorlavmatmipfip"""
URBIT_PREFIXES = "".join(URBIT_PREFIXES.splitlines())

URBIT_SUFFIXES = """zodnecbudwessevpersutletfulpensytdurwepserwylsun
rypsyxdyrnuphebpeglupdepdysputlughecryttyvsydnex
lunmeplutseppesdelsulpedtemledtulmetwenbynhexfeb
pyldulhetmevruttylwydtepbesdexsefwycburderneppur
rysrebdennutsubpetrulsynregtydsupsemwynrecmegnet
secmulnymtevwebsummutnyxrextebfushepbenmuswyxsym
selrucdecwexsyrwetdylmynmesdetbetbeltuxtugmyrpel
syptermebsetdutdegtexsurfeltudnuxruxrenwytnubmed
lytdusnebrumtynseglyxpunresredfunrevrefmectedrus
bexlebduxrynnumpyxrygryxfeptyrtustyclegnemfermer
tenlusnussyltecmexpubrymtucfyllepdebbermughuttun
bylsudpemdevlurdefbusbeprunmelpexdytbyttyplevmyl
wedducfurfexnulluclennerlexrupnedlecrydlydfenwel
nydhusrelrudneshesfetdesretdunlernyrsebhulryllud
remlysfynwerrycsugnysnyllyndyndemluxfedsedbecmun
lyrtesmudnytbyrsenwegfyrmurtelreptegpecnelnevfes"""
URBIT_SUFFIXES = "".join(URBIT_SUFFIXES.splitlines())


EMOJIS = """🍇 Grapes
🍈 Melon
🍉 Watermelon
🍊 Tangerine
🍋 Lemon
🍌 Banana
🍍 Pineapple
🥭 Mango
🍎 Red Apple
🍏 Green Apple
🍐 Pear
🍑 Peach
🍒 Cherries
🍓 Strawberry
🫐 Blueberries
🥝 Kiwi Fruit
🍅 Tomato
🫒 Olive
🥥 Coconut
🥑 Avocado
🍆 Eggplant
🥔 Potato
🥕 Carrot
🌽 Ear of Corn
🌶️ Hot Pepper
🫑 Bell Pepper
🥒 Cucumber
🥬 Leafy Green
🥦 Broccoli
🧄 Garlic
🧅 Onion
🍄 Mushroom
🥜 Peanuts
🫘 Beans
🌰 Chestnut
🍞 Bread
🥐 Croissant
🥖 Baguette Bread
🫓 Flatbread
🥨 Pretzel
🥯 Bagel
🥞 Pancakes
🧇 Waffle
🧀 Cheese Wedge
🍖 Meat on Bone
🍗 Poultry Leg
🥩 Cut of Meat
🥓 Bacon
🍔 Hamburger
🍟 French Fries
🍕 Pizza
🌭 Hot Dog
🥪 Sandwich
🌮 Taco
🌯 Burrito
🫔 Tamale
🥙 Stuffed Flatbread
🧆 Falafel
🥚 Egg
🍳 Cooking
🥘 Shallow Pan of Food
🍲 Pot of Food
🫕 Fondue
🥣 Bowl with Spoon
🥗 Green Salad
🍿 Popcorn
🧈 Butter
🧂 Salt
🥫 Canned Food
🍱 Bento Box
🍘 Rice Cracker
🍙 Rice Ball
🍚 Cooked Rice
🍛 Curry Rice
🍜 Steaming Bowl
🍝 Spaghetti
🍠 Roasted Sweet Potato
🍢 Oden
🍣 Sushi
🍤 Fried Shrimp
🍥 Fish Cake with Swirl
🥮 Moon Cake
🍡 Dango
🥟 Dumpling
🥠 Fortune Cookie
🥡 Takeout Box
🦪 Oyster
🍦 Soft Ice Cream
🍧 Shaved Ice
🍨 Ice Cream
🍩 Doughnut
🍪 Cookie
🎂 Birthday Cake
🍰 Shortcake
🧁 Cupcake
🥧 Pie
🍫 Chocolate Bar
🍬 Candy
🍭 Lollipop
🍮 Custard
🍯 Honey Pot
🍼 Baby Bottle
🥛 Glass of Milk
☕ Hot Beverage
🫖 Teapot
🍵 Teacup Without Handle
🍾 Bottle with Popping Cork
🍷 Wine Glass
🍸 Cocktail Glass
🍹 Tropical Drink
🍺 Beer Mug
🍻 Clinking Beer Mugs
🥂 Clinking Glasses
🥃 Tumbler Glass
🥤 Cup with Straw
🧋 Bubble Tea
🧃 Beverage Box
🧊 Ice
🐒 Monkey
🦍 Gorilla
🦧 Orangutan
🐶 Dog Face
🐺 Wolf
🦊 Fox
🦝 Raccoon
🐱 Cat Face
🐈‍⬛ Black Cat
🦁 Lion
🐯 Tiger Face
🐆 Leopard
🐴 Horse Face
🦄 Unicorn
🦓 Zebra
🦌 Deer
🦬 Bison
🐮 Cow Face
🐂 Ox
🐃 Water Buffalo
🐄 Cow
🐷 Pig Face
🐗 Boar
🐏 Ram
🐑 Ewe
🐐 Goat
🐪 Camel
🦙 Llama
🦒 Giraffe
🐘 Elephant
🦣 Mammoth
🦏 Rhinoceros
🦛 Hippopotamus
🐭 Mouse Face
🐹 Hamster
🐰 Rabbit Face
🐿️ Chipmunk
🦫 Beaver
🦔 Hedgehog
🦇 Bat
🐻 Bear
🐻‍❄️ Polar Bear
🐨 Koala
🐼 Panda
🦥 Sloth
🦦 Otter
🦨 Skunk
🦘 Kangaroo
🦡 Badger
🦃 Turkey
🐔 Chicken
🐓 Rooster
🐥 Front-Facing Baby Chick
🐦 Bird
🐧 Penguin
🕊️ Dove
🦅 Eagle
🦆 Duck
🦢 Swan
🦉 Owl
🪶 Feather
🦩 Flamingo
🦚 Peacock
🦜 Parrot
🐸 Frog
🐊 Crocodile
🐢 Turtle
🦎 Lizard
🐍 Snake
🦕 Sauropod
🦖 T-Rex
🐳 Spouting Whale
🐋 Whale
🐬 Dolphin
🦭 Seal
🐟 Fish
🐠 Tropical Fish
🐡 Blowfish
🦈 Shark
🐙 Octopus
🐚 Spiral Shell
🐌 Snail
🦋 Butterfly
🐛 Bug
🐜 Ant
🐝 Honeybee
🪲 Beetle
🐞 Lady Beetle
🦗 Cricket
🕷️ Spider
🕸️ Spider Web
🦂 Scorpion
🦟 Mosquito
🪰 Fly
🪱 Worm
🦠 Microbe
💐 Bouquet
🌸 Cherry Blossom
🏵️ Rosette
🌹 Rose
🥀 Wilted Flower
🌺 Hibiscus
🌻 Sunflower
🌼 Blossom
🌷 Tulip
🌱 Seedling
🪴 Potted Plant
🌳 Deciduous Tree
🌴 Palm Tree
🌵 Cactus
🌾 Sheaf of Rice
🌿 Herb
☘️ Shamrock
🍁 Maple Leaf
🍂 Fallen Leaf
🍃 Leaf Fluttering in Wind
🍄 Mushroom
🌰 Chestnut
🦀 Crab
🦞 Lobster
🦐 Shrimp
🦑 Squid
💦 Sweat Droplets
🌒 Waxing Crescent Moon
🌓 First Quarter Moon
🌔 Waxing Gibbous Moon
🌕 Full Moon
🌖 Waning Gibbous Moon
🌗 Last Quarter Moon
🌘 Waning Crescent Moon
🌞 Sun with Face
⭐ Star
🌠 Shooting Star
☁️ Cloud
🌪️ Tornado
🌈 Rainbow
☂️ Umbrella
⚡ High Voltage
❄️ Snowflake
⛄ Snowman Without Snow
🔥 Fire
💧 Droplet
🌊 Water Wave
""".splitlines()
EMOJIS = [x[0] for x in EMOJIS if x.strip()]


def urbit_like(key: bytes, length: Optional[int] = None) -> str:
    """Returns an Urbit-word representation of the key, separated by dashes."""
    syllables = []
    for n, b in enumerate(key):
        left = b * 3
        right = b * 3 + 3
        if n % 2 == 0:
            syllables.append(URBIT_PREFIXES[left:right])
        else:
            syllables[-1] = syllables[-1] + URBIT_SUFFIXES[left:right]
    if length is not None:
        syllables = syllables[:length]
    return "-".join(syllables)


def emoji(key: bytes, length: Optional[int] = None) -> str:
    """Returns an emoji representation of the key, separated by spaces."""
    emojis = []
    for n, b in enumerate(key):
        emojis.append(EMOJIS[b])
    return " ".join(emojis)


__all__ = ["urbit_like", "emoji", "__version__"]
