# HW4
# Write a program to lazily rewrap text from the filename passed so that it fits an 80
# column window without breaking any words. Use a generator that yields the next lines
# of text, each containing as many words as possible

def lazy_rewrapper(file_name):
    text = open(file_name, 'r').readlines()
    for line in text:
        list_of_words = line.split(' ')

        cursor = 0
        length_of_line = 0
        current_line = []

        while True:
            if length_of_line > 81:
                yield ' '.join(current_line[:-1])
                length_of_line = 0
                current_line = []
                cursor -= 1
            else:
                length_of_line += (len(list_of_words[cursor]) + 1)
                current_line.append(list_of_words[cursor])
                cursor += 1
            if cursor == len(list_of_words):
                print(' '.join(current_line[:-1]))
                break


'''
example
of
the
implementation as below:
'''
wrapped_text = lazy_rewrapper("/Users/mvrayo-mini/Downloads/text.txt")


while True:
    try:
        print(next(wrapped_text))
    except StopIteration:
        break
