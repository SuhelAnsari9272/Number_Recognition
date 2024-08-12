import random
import inflect

# Initialize the inflect engine
p = inflect.engine()

# Function to get the word representation of a number in different styles
def get_number_word(number):
    word = p.number_to_words(number)
    words = word.replace('-', ' ').split()
    lower_words = [''.join(word.lower()) for word in words]
    lower_word = ' '.join(lower_words)
    upper_words = [''.join(word.upper()) for word in words]
    upper_word = ' '.join(upper_words)
    title_words= [''.join(word.title()) for word in words]
    title_word = ' '.join(title_words)
    if number == 100 :
      lower_word, upper_word,title_word = lower_words[1] , upper_words[1], title_words[1]
      
    word_list = [lower_word, upper_word, title_word]
    return word_list

# Generating the list of words for numbers from 1 to 100
words = []

for i in range(1, 101):
    words.extend(get_number_word(i))

# Print the list of words
for word in words:
    print(word)

print(len(words))
