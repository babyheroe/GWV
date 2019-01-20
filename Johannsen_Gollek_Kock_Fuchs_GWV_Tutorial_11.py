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

# Aufgabe 1

import random
import sys

list_of_5_names = ['Andreas', 'Berta', 'Charlie', 'Dorothea', 'Eberhart']
list_of_8_names = ['Andreas', 'Berta', 'Charlie', 'Dorothea', 'Eberhart',
                   'Ferdinand', 'Gertrud', 'Hans']
list_of_10_names = ['Andreas', 'Berta', 'Charlie', 'Dorothea', 'Eberhart',
                    'Ferdinand', 'Gertrud', 'Hans', 'Isabella', 'Juergen']
list_of_20_names = ['Andreas', 'Berta', 'Charlie', 'Dorothea', 'Eberhart',
                    'Ferdinand', 'Gertrud', 'Hans', 'Isabella', 'Juergen',
                    'Karo', 'Lennard', 'Markus', 'Nina', 'Olga',
                    'Peter', 'Quetzal', 'ROOOOBERT', 'Sven', 'Theodor']
list_of_50_names = ['Eleonore', 'Lynn', 'Nikia', 'Amos', 'Cyril',
                    'Margeret', 'Chanelle', 'Kerri', 'Shira', 'Margery',
                    'Meagan', 'Lucile', 'Tonette', 'Rashida', 'Emelda',
                    'Nadene', 'Pilar', 'Ettie', 'Cammie', 'Sandee',
                    'Xochitl', 'Macy', 'Graig', 'Wen', 'Toni',
                    'Leesa', 'Yadira', 'Mellisa', 'Maurita', 'Chara',
                    'Dorsey', 'Gail', 'Sergio', 'Davis', 'Shannan',
                    'Birdie', 'Estelle', 'Merissa', 'Fred', 'Mariam',
                    'Wilber', 'Neil', 'Reuben', 'Selina', 'Lizabeth',
                    'Sylvie', 'Elinore', 'Sunday', 'Bessie', 'Liberty']


# Reads the dictionary from the .txt file
def get_dictionary():
    # Reading .txt into text
    data = open("Johannsen_Gollek_Kock_Fuchs_GWV_Tutorial_11_sitzordnung.txt", "r")
    text = data.readlines()
    data.close()

    # Writing content of text into dictionary
    dictionary = {}
    for i in range(0, len(text)):
        text[i] = str(text[i].strip('\n'))
        if text[i] != '':
            person1 = text[i].split(";")[0]
            person2 = text[i].split(";")[1]
            relation = int(text[i].split(";")[2])

            if person1 in dictionary and person2 not in dictionary[person1]:
                dictionary[person1][person2] = relation
            else:
                dictionary[person1] = {person2: relation}

    # print "Current dictionary:"
    # print dictionary
    # print ""
    return dictionary


# Randomizes the relationships in the .txt file
def get_randomize_relationships(names):
    newDictionary = {}

    # Writing randomized relationships for every possible relation in newDictionary
    for i in range(0, len(names)):
        for j in range(i + 1, len(names)):
            person1 = names[i]
            person2 = names[j]
            relation = random.randint(-5, 5)
            if person1 in newDictionary:
                newDictionary[person1][person2] = relation
            else:
                newDictionary[person1] = {person2: relation}

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

    return ratingValue


# Generates new random seating order as a name list
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


"""
Tests:
dict1 = get_dictionary()
listOfNames = get_random_seating_order(dict1)
dict2 = get_randomize_relationships(listOfNames)
seatingOrder = get_random_seating_order(dict2)
get_rating(seatingOrder, dict2)
dict3 = get_randomize_relationships(list_of_10_names)
brute_force(dict3, 100)
"""


# Gives
def brute_force(dictionary, allowedFailures):
    bestSeatingOrder = []
    bestRating = -sys.maxint - 1
    failures = 0
    while failures <= allowedFailures:
        seatingOrder = get_random_seating_order(dictionary)
        rating = get_rating(seatingOrder, dictionary)
        if rating > bestRating:
            bestRating = rating
            bestSeatingOrder = seatingOrder
            failures = 0
        else:
            failures += 1
    print "brute force:"
    print "seating order: ", bestSeatingOrder
    print "rating: ", bestRating


# Picks a fix number of randomly persons and checks all of their neighbours for best swapping
# Count: All actual swaps, defined by tries
def greedy_ascent_costly(tries, randomSeatingOrder, dicti):
    rating = get_rating(randomSeatingOrder, dicti)

    for i in range(0, tries):
        pickedPerson = random.choice(randomSeatingOrder)

        print "Initial seating order: ", randomSeatingOrder, rating
        seatingOrder, rating = get_best_swap(randomSeatingOrder, pickedPerson, dicti, rating)
        i += 1

    return seatingOrder, rating


# Checks all swap possibilities for person by swapping with left neigbours
# returns the new best seatingOrder and belonging ratingValue
def get_best_swap(seatingOrder, pickedPerson, dicti, rating):
    index = seatingOrder.index(pickedPerson)
    swapIndex = index - 1
    bestSwapIndex = swapIndex
    bestRating = rating

    for i in range(0, len(seatingOrder)):
        newSeatingOrder = list(seatingOrder)
        newSeatingOrder[index], newSeatingOrder[swapIndex] = newSeatingOrder[swapIndex], newSeatingOrder[index]
        newRating = get_rating(newSeatingOrder, dicti)
        if newRating > rating:
            bestSwapIndex = swapIndex
            bestRating = newRating
        swapIndex -= 1

    print pickedPerson, "has swapped with ", seatingOrder[bestSwapIndex]
    seatingOrder[index], seatingOrder[bestSwapIndex] = seatingOrder[bestSwapIndex], seatingOrder[index]

    print "New seating order: ", seatingOrder, bestRating, "\r\n"
    return seatingOrder, bestRating


# Checks for len(seatingOrder)/2 persons for a better rating.
# If not found, seatingOrder will be randomly assigned new and then compared with the old seatingOrder
# maxRestarts: How many times the algorithm may restart randomly in max
# The error count for a restart is defined when calling greedy
def greedy_ascent_Restart(maxRestarts, randomSeatingOrder, dicti):
    initialRating = get_rating(randomSeatingOrder, dicti)
    initialOrder = list(randomSeatingOrder)

    seatingOrder, rating = greedy_ascent_costly(len(randomSeatingOrder) / 2, randomSeatingOrder, dicti)
    if rating <= initialRating:
        rating = initialRating

        for i in range(0, maxRestarts - 1):
            randomRestartOrder = get_random_seating_order(dicti)

            # randomRestartRating = get_rating(randomRestartOrder, dicti)
            # oder einfach randomRestartRating vergleichen und nicht nochmal verbessern?

            newSeatingOrder, newRating = greedy_ascent_costly(len(randomRestartOrder) / 2, randomRestartOrder, dicti)
            if newRating > rating:
                return "With i+1 randomRestarts: ", newSeatingOrder, newRating
            else:
                i += 1
        return "No randomRestart helped. InitialOrder: ", initialOrder, initialRating


dict1 = get_dictionary()
seats = get_random_seating_order(dict1)
# print greedy_ascent_costly(5, seats, dict1)
print greedy_ascent_Restart(4, seats, dict1)