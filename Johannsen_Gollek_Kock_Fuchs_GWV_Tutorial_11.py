# -*- coding: utf-8 -*-
"""
Dieses Dokument wurde von
Malte Johannsen (6946244),
Marc Fuchs (6054068),
Sünje Gollek (6894597)
& Marius Kock (6947933) 
bearbeitet.

GWV Tutorial 
"""

#Aufgabe 1

import random

# Reads the dictionary from the .txt file
def get_dictionary():
    # Reading .txt into text
    data = open("Johannsen_Gollek_Kock_Fuchs_GWV_Tutorial_11_sitzordnung.txt", "r")
    text =  data.readlines()
    data.close()
    
    # Writing content of text into dictionary
    dictionary = {}
    for i in range(0, len(text)):
        text[i] = str(text[i].strip('\n'))
        if text[i] != '':
            person1 = text[i].split(";")[0]
            person2 = text[i].split(";")[1]
            relation = text[i].split(";")[2]
            
            if person1 in dictionary and person2 not in dictionary[person1]:
                dictionary[person1][person2] = relation
            else: 
                dictionary[person1] = {person2 : relation}
    
    print "Current dictionary:"
    print dictionary
    print ""
    return dictionary

# Writes a new relationship into the .txt file
def set_new_dataset(person1, person2, relation, dictionary):
    # New relation with known or unknown person2
    if person1 in dictionary:
        dictionary[person1][person2] = relation
    # New person1
    else: 
        dictionary[person1] = {person2 : 1, 'count' : 1.0}
    print dictionary
    print dictionary[person1][person2]
    
    return dictionary

# Randomizes the relationships in the .txt file
def get_randomize_relationships(dictionary):
    newDictionary = {}
    # Get all names
    names = get_random_seating_order(dictionary)
        
    # Writing randomized relationships for every possible relation in newDictionary
    for i in range(0, len(names)):
        for j in range(i+1, len(names)):
            person1 = names[i]
            person2 = names[j]
            relation = random.randint(-5, 5)
            if person1 in newDictionary:
                newDictionary[person1][person2] = relation
            else: 
                newDictionary[person1] = {person2 : relation}
    
    # Writing randomized dictionary into .txt
    data = open("Johannsen_Gollek_Kock_Fuchs_GWV_Tutorial_11_sitzordnung.txt", "w")
    for person1 in newDictionary:
        for person2 in newDictionary[person1]:
            relation = newDictionary[person1][person2]
            data.write(person1 + ";" + person2 + ";" + str(relation) + "\n")
    data.close()
    
    print "Randomized relationships:"
    print newDictionary
    print ""
    return newDictionary

# Gives the relationship value for 2 persons 
def get_dict_value(Person1, Person2, dictionary):
    if Person1 in dictionary:
        if Person2 in dictionary[Person1]:
            return dictionary[Person1][Person2]
        
    elif Person2 in dictionary:
        if Person1 in dictionary[Person2]:
            return dictionary[Person2][Person1]
    return 0

# Gives rating of an seating order
def get_rating(seatingOrder, dictionary):
    ratingValue = 0
    # current relationship value for whole table
    for j in range(0, len(seatingOrder) - 1):
        ratingValue += get_dict_value(seatingOrder[j], seatingOrder[j + 1], dictionary)

    # relation of last person with first person
    ratingValue += get_dict_value(seatingOrder[-1], seatingOrder[0], dictionary)

    print "Current relationship value: ", ratingValue
    print ""
    return ratingValue
    
# Generates new random seating order and calculates current relationship value
def get_random_seating_order(dictionary):
    seatingOrder = []

    # randomizes seatingOrder as list
    for name1 in dictionary:
        for name2 in dictionary[name1]:
            if name1 not in seatingOrder:
                seatingOrder.append(name1)
            elif name2 not in seatingOrder:
                seatingOrder.append(name2)
    random.shuffle(seatingOrder)
    
    return seatingOrder

#Tests:
dict1 = get_dictionary()
dict2 = get_randomize_relationships(dict1)
seatingOrder = get_random_seating_order(dict2)
get_rating(seatingOrder, dict2)

# Gives always the perfect solution by trying every possible combination
def brute_force(dictionary):
    #TooDo
    
    
    
    
    
    
    
    
    
    
    