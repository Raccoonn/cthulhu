import json
import random



def build_npc(name):
    '''
    Create an random NPC with given name
        - Assign full, half, and fifth values for each characteristic
          and for every attributes

        - Writes NPC to file with given name
    '''
    ## Load in character information
    with open('characters.json') as f:
        data = json.load(f)

    ## Initialize NPC
    npc = {}

    ## Physical attributes
    npc['age'] = random.randint(15, 70)
    npc['sex'] = random.choice(['M', 'F'])

    ## Characteristic distribution
    stats = ['STR', 'CON', 'SIZ', 'DEX', 'APP', 'EDU', 'INT', 'POW']
    cvals  = [40, 50, 50, 50, 60, 60, 70, 80]
    random.shuffle(cvals)
    npc['characteristics'] = {s : [v, v//2, v//5] for s,v in zip(stats, cvals)}

    ## Skill selection
    skills = data['base_character']['skills']
    keys = random.choices(list(skills.keys()), k=14)

    ## Primary skills
    primary_vals   = [70, 60, 60, 50, 50, 50, 40, 40, 40]
    npc['primary_skills'] = {s : [v, v//2, v//5] for s,v in zip(keys[:10], primary_vals)}

    ## Secondary skillls
    secondary_vals = [20, 20, 20, 20]
    npc['secondary_skills'] = {s : [(skills[s]+v), (skills[s]+v)//2, (skills[s]+v)//5] 
                                for s,v in zip(keys[10:14], secondary_vals)}

    ## Randomly assing a mania and a phobia
    npc['phobias'] = random.choice(data['base_character']['phobias'])
    npc['manias']  = random.choice(data['base_character']['manias'])

    ## Damage bonus and build
    val = npc['characteristics']['STR'][0] + npc['characteristics']['SIZ'][0]
    if 2 < val < 64:
        bonus = -2
        buuld = -2
    elif 65 < val < 84:
        bonus = -1
        build = -1
    elif 85 < val < 124:
        bonus = 0
        build = 0
    elif 125 < val < 164:
        bonus = random.randint(1, 4)
        build = 1
    elif 165 < val < 204:
        bonus = random.randint(1, 6)
        build = 2

    npc['bonus'] = bonus
    npc['build'] = build

    ## Dodge
    npc['dodge'] = npc['characteristics']['DEX'][0] // 2


    ## Hit points
    npc['hit points'] = (npc['characteristics']['SIZ'][0] + npc['characteristics']['CON'][0]) // 10

    ## Magic points
    npc['magic points'] = npc['characteristics']['POW'][0] // 5

    ## Move rate
    if (npc['characteristics']['STR'][0] < npc['characteristics']['SIZ'][0] and
        npc['characteristics']['DEX'][0] < npc['characteristics']['SIZ'][0]):
        move = 7
    elif (npc['characteristics']['STR'][0] >= npc['characteristics']['SIZ'][0] or
          npc['characteristics']['DEX'][0] >= npc['characteristics']['SIZ'][0]):
        move = 8
    else:
        move = 9

    ages = [40, 50, 60, 70, 80]
    for i, a in enumerate(ages[:-1]):
        if ages[i] < a < ages[i+1]:
            move -= i+1
    
    npc['move'] = move


       

    ## Sanity
    npc['sanity'] = npc['characteristics']['POW'][0]

    ## Luck
    npc['luck'] = sum([random.randint(1, 6) for _ in range(3)]) * 5


    ## Write new NPC to json
    with open(f'{name}.json', 'w') as f:
        json.dump(npc, f, indent=4)



build_npc('aaron')
