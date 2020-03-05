"""
Created on Thu Mar  5 18:43:20 2020

@author: tbour
"""

"""
Create a MongoDB database to test the API.
"""

import pandas as pd
from random import randint, choice, choices
from datetime import date

# Number of names and first names to consider when generating names.
n = 10000

# n most popular first and last name in France
first_name = pd.read_csv('prenom.csv').sort_values('sum', ascending=False)
last_name = pd.read_csv('patronymes.csv').sort_values('count', ascending=False)
f_name = first_name['prenom'].values[:n]
l_name = last_name['patronyme'].values[:n]

# The fifteen most populated cities in France
cities = ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes',
          'Montpellier', 'Strasbourg', 'Bordeaux', 'Lille', 'Rennes',
          'Reims', 'Saint-Etienne', 'Le Havre', 'Toulon']


real_estate = ['Appartement', 'Maison']

room = ['Chambre', 'Salle de bain', 'Cuisine', 'Salle à manger', 'Salon']

def generate_date():
    """
    Random birthdate.
    Generate a random birthdate between 1950 and 2000.
    """
    year = randint(1950, 2000)
    month = randint(1, 13)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = randint(1, 31)
    elif month==2:
        day = randint(1, 28)
    else:
        day = randint(1, 30)
    return date(year, month, day)
    
    
def generate_user():
    """
    Random user.
    Generate a random user. A user is defined by his/her last name, first name
    and birthdate.
    """
    user = {}
    user['first_name'] = choice(f_name)
    user['last_name'] = choice(l_name)
    user['birthdate'] = generate_date()
    return user

def generate_rooms_orga(n_rooms):
    """
    Random rooms organisation.
    Generate a random real estate, with at least 1 'Chambre' if n_rooms=1, and
    1 'Chambre' + 1 'Salle de bain' if n_rooms=2. Some of the rooms are less
    likely to be picked.
    """
    estate = {'Chambre' : 1, 'Salle de bain' : 1, 'Cuisine' : 0,
              'Salle à manger' : 0, 'Salon' : 0}
    if n_rooms == 1:
        estate['Salle de bain'] -= 1
    if n_rooms > 2:
        diff = n_rooms - 2
        weights = [5, 1, 3, 1, 2]
        r = choices(room, weights=weights, k=diff)
        for key in r:
            estate[key] += 1
    return estate

def generate_description(estate, estate_type, city):
    """
    Random description.
    Generate a random description of the real estate.
    """
    description = ""
    description += estate_type + ' situé(e) à ' + city + ' comprenant '
    for key in estate.keys():
        if estate[key] != 0:
            description += str(estate[key]) + ' ' + key + '(s), '
    description = description[:-2] + '.'
    return description

def generate_estate(user):
    """
    Random estate.
    Generate a random estate (estate type, rooms organisation, city...). The
    owner name is the same name as the user.
    """
    estate_type = choice(real_estate)
    city = choice(cities)
    n_rooms = randint(1, 10)
    rooms_orga = generate_rooms_orga(n_rooms)
    if n_rooms >= 4:
        estate_type = choice(real_estate)
    else:
        estate_type = 'Appartement'
    description = generate_description(rooms_orga, estate_type, city)
    estate = {'owner': user['first_name'] + ' ' + user['last_name'],
              'estate_type': estate_type,
              'city': city,
              'rooms': rooms_orga,
              'description': description
            }
    return estate



