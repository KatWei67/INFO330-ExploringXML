
import sqlite3
import sys
import xml.etree.ElementTree as ET

# Incoming Pokemon MUST be in this format
#
# <pokemon pokedex="" classification="" generation="">
#     <name>...</name>
#     <hp>...</name>
#     <type>...</type>
#     <type>...</type>
#     <attack>...</attack>
#     <defense>...</defense>
#     <speed>...</speed>
#     <sp_attack>...</sp_attack>
#     <sp_defense>...</sp_defense>
#     <height><m>...</m></height>
#     <weight><kg>...</kg></weight>
#     <abilities>
#         <ability />
#     </abilities>
# </pokemon>



# Read pokemon XML file name from command-line
# (Currently this code does nothing; your job is to fix that!)
if len(sys.argv) < 2:
    print("You must pass at least one XML file name containing Pokemon to insert")


# connect to database
conn = sqlite3.connect('pokemon.sqlite')
c = conn.cursor()


for i, arg in enumerate(sys.argv):
    # Skip if this is the Python filename (argv[0])
    if i == 0:
        continue

    # prase xml file
    tree = ET.parse(arg)
    root = tree.getroot()
    
    # extract pokemon data
    pokedex = root.attrib.get('pokedex', None)
    classification = root.attrib.get('classification', None)
    generation = root.attrib.get('generation', None)
    name = root.attrib.get('name', None)
    hp = root.attrib.get('hp', None)
    type = [type.text for type in root.findall('type') ]
    attack = root.attrib.get('attack', None)
    defense = root.attrib.get('defense', None)
    speed = root.attrib.get('speed', None)
    sp_attack = root.attrib.get('sp_attack', None)
    sp_defense = root.attrib.get('sp_defense', None)
    height = root.attrib.get('height', None)
    weight = root.attrib.get('weight', None)
    abilities = [abilities.text for abilities in root.findall('abilities/ability')]

    # check if pokemon already exist in the database
    c.execute("SELECT COUNT(*) FROM pokemon WHERE name=?", (name,))
    count = c.fetchone()[0]
    if count > 0:
        continue
    
    # insert new pokemon into database
    c.execute("INSERT INTO pokemon(pokedex, classification, generation, hp, type, attack, defense, speed, sp_attack, sp_defense, height, weight, abilities) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (pokedex, classification, generation, hp, '|'.join(type), attack, defense, speed, sp_attack, sp_defense, height, weight, abilities))
    pokemon_id = c.lastrowid
    
    # insert abilities into database
    for ability in abilities:
        c.execute("INSERT INTO pokemon_abilities(pokemon_id, ability) values(?,?)", (pokemon_id, ability))

# commit change and close the connection
conn.commit()
conn.close()
