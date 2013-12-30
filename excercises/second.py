__author__ = 'Janez Stupar'

import codecs


def goofy_cipher(input_text):
    """
    Take a string and take every second and reverse it. Then encode using ROT13.

    Not much else to add. Python comes with batteries included!
    """
    words = input_text.split()
    new_words = []
    for idx, word in enumerate(words):
        if idx % 2 == 0:
            val = "".join(reversed(word))
            new_words.append(codecs.encode(val, 'rot_13'))
        else:
            new_words.append(codecs.encode(word, 'rot_13'))

    return " ".join(new_words)

if __name__ == "__main__":
    foo = goofy_cipher("this is a test string!!!####")
    print foo
    foo = goofy_cipher(foo)
    print foo
    print goofy_cipher("Hello world!")


