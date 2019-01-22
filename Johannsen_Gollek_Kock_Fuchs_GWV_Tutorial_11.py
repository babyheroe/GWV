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
import profile

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
    
    return bestSeatingOrder, bestRating

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

    #print pickedPerson, "has swapped with ", seatingOrder[bestSwapIndex]
    seatingOrder[index], seatingOrder[bestSwapIndex] = seatingOrder[bestSwapIndex], seatingOrder[index]

    #print "New seating order: ", seatingOrder, bestRating, "\r\n"
    return seatingOrder, bestRating

# Picks a fix number of randomly persons and checks all of their neighbours for best swapping
# Count: All actual swaps, defined by tries
def greedy_ascent(randomSeatingOrder, dictionary):
    rating = get_rating(randomSeatingOrder, dictionary)
    oldRating = rating
    run = True
    seatingOrder = randomSeatingOrder

    while(run):
        for i in range(0, len(seatingOrder)):
            newSeatingOrder, newRating = get_best_swap(seatingOrder, seatingOrder[i], dictionary, rating)
            if newRating > rating:
                seatingOrder = newSeatingOrder
                rating = newRating
                i = len(seatingOrder) + 1
        if rating > oldRating:
            oldRating = rating
        else:
            run = False

    return seatingOrder, rating

# Checks for len(seatingOrder)/2 persons for a better rating.
# If not found, seatingOrder will be randomly assigned new and then compared with the old seatingOrder
# maxRestarts: How many times the algorithm may restart randomly in max
# The error count for a restart is defined when calling greedy
def greedy_ascent_restart(seatingOrder, dictionary, tries):
    bestRating = get_rating(seatingOrder, dictionary)
    bestSeatingOrder = seatingOrder
    i = 0
    while i < tries:
        randomSeatingOrder = get_random_seating_order(dictionary)
        newSeatingOrder, newRating =  greedy_ascent(randomSeatingOrder, dictionary)
        i += 1
        if newRating > bestRating:
            bestSeatingOrder = newSeatingOrder
            bestRating = newRating
            i = 0
    return bestSeatingOrder, bestRating

def greedy_ascent_trio(tries, seatingOrder, dicti):
    rating = get_rating(seatingOrder, dicti)    
    worstPerson = None
    worstTrioRating = sys.maxint
    
    #for-loop für anzahl der Schritte
    for i in range(0, tries):
        #foor-loop um die Person mit der schlechtesten Platzierung zu finden
        for seat in range(0, len(seatingOrder)):
            #sonderfall für letzte Person
            if (seat == len(seatingOrder) - 1):
                trio = [seatingOrder[seat - 1], seatingOrder[seat], seatingOrder[0]]  
            else:
                trio = [seatingOrder[seat - 1], seatingOrder[seat], seatingOrder[seat + 1]]
            
            #rating für die Person und die Nachbarn
            trioRating = get_rating(trio, dicti)
            
            #schlechteres Trio gefunden
            if trioRating < worstTrioRating:
                worstTrioRating = trioRating
                worstPerson = seat
        
        #funktion zum sitzplatztauschen.
        newSeatingOrder, newRating = ascent_trio(worstPerson, seatingOrder, dicti, rating)
        
        #update rating
        if newRating > rating:
            rating = newRating
            seatingOrder = newSeatingOrder
        
        i += 1
        
    return seatingOrder, rating
            
def ascent_trio(worstPerson, seatingOrder, dicti, rating):
    #liste zum speichern der möglichen restpartner, ohne worstPerson
    swapPartner = list(seatingOrder)
    swapPartner.pop(worstPerson)
    newRating = -sys.maxint -1
    
    #läuft solange es tauschpartner gibt und kein besseres rating erreich wurde
    while newRating < rating and len(swapPartner) != 0:
        newSeatingOrder = list(seatingOrder)
        #wählt zufällige person aus
        swapIndex = seatingOrder.index(random.choice(swapPartner))
        #probetausch von personen
        newSeatingOrder[worstPerson], newSeatingOrder[swapIndex] = newSeatingOrder[swapIndex], newSeatingOrder[worstPerson]
        
        #proberating erstellen
        newRating = get_rating(newSeatingOrder, dicti)
        #keine verbesserung tauschpartner entfernen
        if newRating < rating:
            swapPartner.pop(swapPartner.index(random.choice(swapPartner)))
    
    #entweder bei keiner verbesserung bestehendes zurückgeben oder verbessertes
    if len(swapPartner) != 0:
        return newSeatingOrder, newRating
    else:
        return seatingOrder, rating

#dict1 = get_dictionary()
#seats = get_random_seating_order(dict1)
#print greedy_ascent_costly(5, seats, dict1)
#print greedy_ascent_Restart(4, seats, dict1)
#print greedy_ascent(20000, seats, dict1)

def greedy_best_first(dictionary, seatingOrder):
    randomSeatingOrder = list(seatingOrder)
    person1 = randomSeatingOrder[0]
    result = [person1]
    randomSeatingOrder.remove(person1)
    while randomSeatingOrder != []:
        bestRelation = -5
        bestPerson = person1
        for person2 in randomSeatingOrder:
            relation = get_dict_value(person1, person2, dictionary)
            if bestRelation <= relation:
                bestRelation = relation
                bestPerson = person2
        result.append(bestPerson)
        randomSeatingOrder.remove(bestPerson)
        person1 = bestPerson
    rating = get_rating(result, dictionary)
    return result, rating

def greedy_best_first_optimized(dictionary, persons):
    list_of_persons = list(persons)
    bestResult = []
    bestRating = -sys.maxint - 1
    for person in persons:
        list_of_persons.remove(person)
        new_list_of_persons = [person] + list_of_persons
        result, rating = greedy_best_first(dictionary, new_list_of_persons)
        list_of_persons = list(new_list_of_persons)
        if rating > bestRating:
            bestRating = rating
            bestResult = result
    return bestResult, bestRating

# Evaluiert die Algorythmen
def evaluate_all(persons):
    averageBestFirst = 0
    averageAscentRestart = 0
    averageAscent = 0
    averageBruteForce = 0
    averageAscentTrio = 0
    for i in (range(1, 1000)):
        dictionary = get_randomize_relationships(persons)
        _, tempBestFirst = greedy_best_first_optimized(dictionary, persons)
        _, tempAscentRestart = greedy_ascent_restart(persons, dictionary, 5)
        _, tempAscent = greedy_ascent(persons, dictionary)
        _, tempBruteForce = brute_force(dictionary, 5)
        _, tempAscentTrio = greedy_ascent_trio(5, persons, dictionary)
        
        averageBestFirst += tempBestFirst
        averageAscentRestart += tempAscentRestart
        averageAscent += tempAscent
        averageBruteForce += tempBruteForce
        averageAscentTrio += tempAscentTrio
        print (i)
    averageBestFirst /= 1000
    averageAscentRestart /= 1000
    averageAscent /= 1000
    averageBruteForce /= 1000
    averageAscentTrio /= 1000
    print ("Best First: " + str(averageBestFirst))
    print ("Ascent Restart: " + str(averageAscentRestart))
    print ("Ascent: " + str(averageAscent))
    print ("Brute Force: " + str(averageBruteForce))
    print ("Ascent Trio: " + str(averageAscentTrio))
        
    

list_of_names = list_of_50_names
evaluate_all(list_of_names)
"""
dict3 = get_randomize_relationships(list_of_names)
profile.run('print(greedy_best_first_optimized(dict3, list_of_names)); print()')
profile.run('print(greedy_ascent_restart(list_of_names, dict3, 5)); print()')
profile.run('print(greedy_ascent(list_of_names, dict3)); print()')
profile.run('print(brute_force(dict3, 5)); print()')
profile.run('print(greedy_ascent_trio(5, list_of_names, dict3)); print()')
"""