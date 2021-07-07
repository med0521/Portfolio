#HW6 Scrabble Program
""" A program that takes an input, a scrabble letter rack,
    and outputs all the possible "Scrabble English Words"
    that could be created, along with their scores. Sorted
    by score.
author: Maria DiMedio
version: 3
date: Feb 2, 2021
dependencies: none
calls: none
python version: 3.8
"""

# import statements
import sys
from wordscore import score_word
from collections import Counter


# constants/variables
try:
    #Pull the parameter input from the command line.
    rack = sys.argv[1]
except IndexError:
    print("Rack must be entered to play Scrabble. Format: 'ABCD?*'")
#Handle any upper/lower cases.
rack = rack.upper()

#Read in the list of scrabble english words from the sowpods file.
with open("sowpods.txt","r") as infile:
    raw_input = infile.readlines()
    data = [datum.strip('\n') for datum in raw_input]

# functions
def playwild(word):
    """Returns a list in format [word,letters]
    if a word argument is able to be played by the letters and
    wildcards available in a rack. The second item in the list
    returned is the letters that the wildcards represented.
    Otherwise if a word can't be played, returns 'No'.
    """
    word = word.upper()
    #Copy main rack into function to avoid global var.
    rack2 = list(rack)
    #Str to house letters played by wildcards.
    subbed = ''
    for letter in word:
        if letter in rack2:
            rack2.remove(letter) #Play a letter if it's available.
        elif '*' in rack2:
            rack2.remove('*') #Play one wildcard if available.
            subbed += letter #Record which letter was used with a wild.
        elif '?' in rack2:
            rack2.remove('?') #Play wildcard if available.
            subbed += letter #Record which letter was used with a wild.
        else:
            return 'No'
    return [word.lower(), subbed.lower()]

# Program to calculate all possible words, and their scores, from a Scrabble Rack input.
if __name__ == "__main__":
    #Raise an exception error if the length of the rack is not between 2-7 characters.
    if len(rack) < 2 or len(rack) > 7:
        raise Exception("Scrabble Rack must be between 2-7 letters")

    #Initialize lists to contain chars of the Rack input.
    wildcards = []
    az = []
    #Figure out how many wildcards vs. A-Z chars are in rack.
    for char in rack.upper():
        if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            az.append(char)
        elif char in '*?':
            wildcards.append(char)
        #Raise an exception if the rack contains a char that is not a wildcard or letter.
        else:
            raise Exception('Character in Rack is not a wildcard or letter A-Z')
    #Handle inputs with >1 of each wildcard type.
    if wildcards.count('?') > 1 or wildcards.count('*') > 1:
        raise Exception('Cannot have more than 1 of each wildcard type (* or ?) in a Rack')
    #Raise an exception if there are more than 2 wildcard symbols entered.
    if len(wildcards) > 2:
        raise Exception('Cannot have more than 2 wildcards in a Rack')


    #Using Counter, create a dictionary of letter occurences in our rack.
    rackcount = Counter(rack)
    rackcount = dict(rackcount)
    #If there are no wildcards in the scrabble rack.
    if len(wildcards) == 0:
        #If the user input included arguments for position and wildcards.
        if len(sys.argv)>2:

            letter = sys.argv[2].upper()
            #Raise an error if the user only gave a letter or position, not both.
            try:
                position = int(sys.argv[3])
            except IndexError:
                print('Must include a position and letter arguement')
            #Reposition the rack to have the letter in the position the user specified.
            rack = rack.replace(letter,'')
            rack = list(rack)
            rack.insert(position-1,letter)
            rack = ''.join(rack)
            #Reduce the word options to be words of similar length, and then of positional arguements.
            datalength = [word for word in data if len(word) <= len(rack)]
            datalength = [word for word in datalength if word[position-1] == rack[position-1]]

            sameletters = []
            #Append words that have the same letters as the rack to sameletters list.
            for word in datalength:
                if set(word).issubset(set(rack)):
                    sameletters.append(word)
            #Create a dictionary of letter counts out of possible words of similar letters.
            possdict = {possword:dict(Counter(possword)) for possword in sameletters}
            #Compare letter counts to rack letters available using dictionary. Create list of not possible options.
            notpossible = [word for word in possdict for letter in word if possdict[word][letter] > rackcount[letter]]
            #remove the not possible options from the list of possible options.
            possibles = list(set(sameletters) - set(notpossible))
            #Remove again any words which might not have the letter in the right location, according to user input.
            notlocation = [word for word in possibles if word[position-1] != rack[position-1]]
            possibles = list(set(possibles) - set(notlocation))

            #create a list of sublists(words and their scores), sort by score in descending order, then alphabetically
            scoreoptions = [[score_word(word.lower()), word.lower()] for word in possibles]
            scoreoptions_sorted = sorted(scoreoptions, key = lambda x:((-x[0]),x[1]))

            #print out the possible words and total number of options
            for poss in scoreoptions_sorted:
                print("({}, {})".format(poss[0],poss[1]))
            print("Total number of words:",len(scoreoptions_sorted))

        else:
            #Locate the possible words that contain some or all of the letters in the Rack input.
            #Initiate list to add all the Scrable words that are subsets of the rack
            sameletters = []

            #to help our code run faster, reduce the list to only words of less than or equal length to the tiles in our rack
            datalength = [word for word in data if len(word) <= len(rack)]

            #for every word in our shortened list, check to see if it's a subset of our rack's letters.
            for word in datalength:
                if set(word).issubset(set(rack)):
                    sameletters.append(word)

            #Create a dictionary of the words in the list of words made up of the same letters
            #use Counter to find the number of occurences of each letter in the possible words
            possdict = {possword:dict(Counter(possword)) for possword in sameletters}

            #From our dictionary of words and their letter counts, find the words which have
            #More letters than the rack. Add these to the 'not possible' list and then remove any of those words
            #From our list and create a list of 'possible' words
            notpossible = [word for word in possdict for letter in word if possdict[word][letter] > rackcount[letter]]
            possibles = list(set(sameletters) - set(notpossible))

            #Create a list of sublists(words and their scores), sort by score in descending order, then alphabetically
            scoreoptions = [[score_word(word.lower()), word.lower()] for word in possibles]
            scoreoptions_sorted = sorted(scoreoptions, key = lambda x:((-x[0]),x[1]))

            #Print out the possible words and total number of options
            for poss in scoreoptions_sorted:
                print("({}, {})".format(poss[0],poss[1]))
            print("Total number of words:",len(scoreoptions_sorted))


    else:
        #For any racks that contain a wild card, use our wildcard playing function to check if we can play words.
        #Simplify our list of possible words by reducing it according to rack length
        datalength = [word for word in data if len(word) <= len(rack)]

        if len(sys.argv)>2:
             #Make the letter in a given position stay in place as given if user inputs a second argument.
            letter = sys.argv[2].upper()
            #raise an error if the user only gave a letter or position, not both.
            try:
                position = int(sys.argv[3])
            except IndexError:
                print('Must include a position and letter arguement')

            rack = rack.replace(letter,'')
            rack = list(rack)
            rack.insert(position-1,letter)
            rack = ''.join(rack)

            #Reduce the list of potential words to only those that have the letter in the right position.
            datalength = [word for word in datalength if word[position-1] == rack[position-1]]

            possibles = []
            #Iterate through list of words of same char length as rack.
            for word in datalength:
                if playwild(word) != 'No':
                    possibles.append(playwild(word))
            #Initialize list to store possible words that don't need a wildcard (for scoring), and that do.
            scoreoptionsAZ = []
            scoreoptionswild = []
            #Iterate through list of possibles to see if they needed a wildcard or not
            #playwild() returns: (word,['letters replaced by wild']); if len(['lettersreplaced']) = 0
            for word in possibles:
                if len(word[1]) == 0:
                    scoreoptionsAZ.append(word)
                else:
                    scoreoptionswild.append(word)
            #initialize a list to append possible words to play, and their scores
            scoreoptions = []

            for word,used in scoreoptionswild:
                score = score_word(word) - score_word(used)  #subtract value of wild letters (they should = 0)
                scoreoptions.append([score,word.lower()]) #append overall score, and word played

            #add to scoreoptions the regularly scored words (non-wildcard use) in the same format
            scoreoptions += [[score_word(word[0]), word[0]] for word in scoreoptionsAZ]
            #sort scoreoptions by A: score (descending) then B: alphabetically
            scoreoptions_sorted = sorted(scoreoptions, key = lambda x:((-x[0]),x[1]))

            #print out possible scores in tuple format, along with total count of possible words to play
            for poss in scoreoptions_sorted:
                print("({}, {})".format(poss[0],poss[1]))
            print("Total number of words:",len(scoreoptions_sorted))


        else:
            #initialize a list to append possible words to
            possibles = []
            #Iterate through list of words of same char length as rack.
            #Add words to possibles list if they are able to be played.
            for word in datalength:
                if playwild(word) != 'No':
                    possibles.append(playwild(word))

            scoreoptionsAZ = []
            scoreoptionswild = []
            #iterate through list of possibles to see if they needed a wildcard or not
            for word in possibles:
                if len(word[1]) == 0:
                    scoreoptionsAZ.append(word)
                else:
                    scoreoptionswild.append(word)
            #Initialize a list to append possible words to play, and their scores.
            scoreoptions = []
            #Subtract value of wild letters (they should = 0). Append overall score, and word played
            for word,used in scoreoptionswild:
                score = score_word(word) - score_word(used)
                scoreoptions.append([score,word.lower()])

            #add to scoreoptions the regularly scored words (non-wildcard use) in the same format
            scoreoptions += [[score_word(word[0]), word[0]] for word in scoreoptionsAZ]
            #sort scoreoptions by A: score (descending) then B: alphabetically
            scoreoptions_sorted = sorted(scoreoptions, key = lambda x:((-x[0]),x[1]))

            #print out possible scores in tuple format, along with total count of possible words to play
            for poss in scoreoptions_sorted:
                print("({}, {})".format(poss[0],poss[1]))
            print("Total number of words:",len(scoreoptions_sorted))
