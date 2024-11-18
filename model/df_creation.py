from model.characters import Character
from collections import Counter

def elemental_reaction(character_1, character_2, character_3, character_4):
    elements = set([character_1.element, character_2.element, character_3.element, character_4.element])
    names = set([character_1.name, character_2.name, character_3.name, character_4.name])
    if 'Navia' in names:
        return 'Crystal'
    if 'Dendro' in elements:
        if 'Electro' in elements:
            if 'Hydro' in elements:
                if 'Pyro' in elements:
                    return 'Fruit Salad'
                return 'HyperBloom'
            if 'Pyro' not in elements:
                return 'AggraSpread'
        if 'Hydro' in elements:
            if 'Pyro' in elements:
                return 'Burgeon'
            return 'Bloom'
        if 'Pyro' in elements:
            return 'Burn'
    if 'Hydro' in elements:
        if 'Electro' in elements:
            if 'Pyro' in elements:
                return 'National'
            return 'Taser'
        if 'Pyro' in elements:
            return 'Vape'
        if 'Cryo' in elements:
            return 'Freeze'
    if 'Cryo' in elements:
        if 'Pyro' in elements:
            return 'Melt'
        if 'Electro' in elements:
            return 'Superconduct'
    return None
    
def elemental_ressonance(character_1, character_2, character_3, character_4):
    elements = dict(Counter([character_1.element, character_2.element, character_3.element, character_4.element]))
    if len(elements) == 4:
        return 'Resistance'
    if 'Hydro' in elements and elements['Hydro'] > 1:
        return 'HP'
    if 'Pyro' in elements and elements['Pyro'] > 1:
        return 'ATK'
    if 'Dendro' in elements and elements['Dendro'] > 1:
        return 'Elemental Mastery'
    if 'Geo' in elements and elements['Geo'] > 1:
        return 'General Damage'
    if 'Electro' in  elements and elements['Electro'] > 1:
        return 'Energy Recharge'
    if 'Cryo' in elements and elements['Cryo'] > 1:
        return 'CRIT Rate'
    if 'Anemo' in elements and elements['Anemo'] > 1:
        return 'Speed'