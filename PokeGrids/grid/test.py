'''
import random

selectors = [1,2,3,4]
selectors_weights = [3,1,1,0]
sum1 = 0
sum2 = 0
sum3 = 0
sum4 = 0
for i in range(1000):
    selected = random.choices(selectors, weights=selectors_weights, k=1)[0]
    if selected == 1:
        sum1 += 1
    if selected == 2:
        sum2 += 1
    if selected == 3:
        sum3 += 1
    if selected == 4:
        sum4 += 1 
    print(selected)
print(f'sum1: {sum1} sum2: {sum2} sum3: {sum3} sum4: {sum4} ')
'''
'''
types = ['normal', 'fire', 'water', 'grass', 'electric', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy', 'Mono', 'Dual']
print(types)
types = [t for t in types if t not in {'Mono', 'Dual'}]
print(types)
'''
'''
def check_invalid_combination(type1, type2):
    invalidCombinations = [
        ('normal', 'ice'), ('normal','bug'), ('normal','rock'), ('normal', 'steel'), ('fire', 'fairy'), ('ice', 'poison'), ('ground', 'fairy'), ('bug', 'dragon'),
        ('rock', 'ghost'), ('normal', 'water'), ('fire', 'normal'), ('fire', 'water'), ('fire', 'steel'), ('water', 'steel'), ('grass', 'ice'), ('electric', 'normal'),
        ('electric', 'ghost'), ('electric', 'fire'), ('electric', 'psychic'), ('electric', 'dark'), ('electric', 'poison'), ('ice', 'ghost'), ('ice', 'ground'), ('ice', 'bug'),
        ('ice', 'steel'), ('ice', 'fairy'), ('ice', 'fire'), ('fighting', 'ice'), ('poison', 'normal'), ('poison', 'flying'), ('ground', 'psychic'), ('bug', 'ghost'), 
        ('bug', 'fairy'), ('bug', 'dark'), ('rock', 'dark'), ('rock', 'fighting'), ('rock', 'dragon'), ('ghost', 'poison'), ('dragon', 'fairy'), ('dark', 'steel'), 
        ('dark', 'fairy'), ('steel', 'poison'), ('fairy', 'fighting')
    ]

    return (type1, type2) in invalidCombinations or (type2, type1) in invalidCombinations

types = ['fire', 'water', 'grass', 'electric','fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy', 'Mono', 'Dual']
usedRowTypes = ['normal', 'ice']
for i in range(6):
    while any(check_invalid_combination(types[i], usedType) for usedType in usedRowTypes):
        print(f'Before {i}: {types[i]}')
        types.remove(types[i])
        print(f'After {i}: {types[i]}')
    print(f'Outside {i}: {types[i]}')
'''

def decode(message_file):
    # Read the contents of the file
    with open(message_file, 'r') as file:
        file_content = file.readlines()

    # Create a dictionary to store the associations between numbers and words
    number_word_dict = {}

    # Loop through each line in the file content
    for line in file_content:
        # Split the line into words
        words = line.split()

        # Extract the number and word from the line
        number = int(words[0])
        word = words[1]

        # Store the association in the dictionary
        number_word_dict[number] = word

    # Sort the dictionary by keys to arrange numbers in ascending order
    sorted_numbers = sorted(number_word_dict.keys())
    print(sorted_numbers)
    # Extract the corresponding words and create the decoded message
    decoded_message = create_decoded_message(sorted_numbers, number_word_dict)

    # Return the decoded message as a string
    return decoded_message


def create_decoded_message(sorted_numbers, word_dict):
    decoded_words = []

    row_end = 1
    row_index = 1

    for number in sorted_numbers:
        if row_index == row_end:
            decoded_words.append(word_dict[number])
            row_end += 1
            row_index = 1
        else:
            row_index += 1

    decoded_words = ' '.join(decoded_words)
    return decoded_words

# Example usage:
message_file_path = r'C:\Users\nitro\OneDrive\Documents\Projects\coding_qual_input.txt'
result = decode(message_file_path)
print(result)