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

def get_dictionary():
    data = open("Johannsen_Gollek_Kock_Fuchs_GWV_Tutorial_11_sitzordnung.txt", "r")

    text =  data.readlines()

    data.close()
    
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
            
    return dictionary

dictionary = get_dictionary()

def get_dict_value(Person1, Person2):
    if Person1 in dictionary:
        if Person2 in dictionary[Person1]:
            return dictionary[Person1][Person2]
        
    elif Person2 in dictionary:
        if Person1 in dictionary[Person2]:
            return dictionary[Person2][Person1]
    else:
        return 0

print dictionary
print get_dict_value('Peter', 'Juergen')