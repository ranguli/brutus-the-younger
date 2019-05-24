# -*- coding: utf-8 -*-
#!/usr/bin/env/python
from prettytable import PrettyTable
from itertools import permutations
from nltk.corpus import words

from subprocess import call
import pprint
import click
import os.path

class Brutus(object):

    supported_ciphers = ['rot','alphabet_substitution','morse', 'vigenere']

    alphabet = [
        'A','B','C','D','E','F','G','H','I','J',
        'K','L','M','N','O','P','Q','R','S','T',
        'U','V','W','X','Y','Z'
    ]

    def clear_screen(): 
        # check and make call for specific operating system 
        call('clear')


    def all_substrings(string):
        j = 2
        a = [] 

        # Genereate all possible substrings of a string, including the original
        a.append(string)
        if (len(string) != 1):
            while True:
                for i in range(len(string) - j+1):
                    a.append(string[i:i+j])
                if j == len(string):
                    break
                j += 1
        return a

    """ Check all generated substrings to see if they are English """
    def find_english_strings(a):
        real_words = []
        for element in a:
            if (len(element) > 3) and (element.lower() in words.words()):
                real_words.append(element)
        return real_words
    
    """ Returns a ciruclar list, useful for wrapping alphabets"""
    # Accepts x, the starting slice integer (0 for entire phrase + wrapping)
    # List, the list/string in question
    # length, the desired length of wrapping

    def alphabet_wrap(x, list):
        result = []
        for i in range(x, (x + 26)):
            if i >= len(list):
                index = 0 + (i - 26)
                result.append(list[index])
            else:
                result.append(list[i])
        return(result)

    def word_wrap(word, length):
        word = list(word)
        for i in word:
            if (len(word)) != length:
                word.append(i)
        result = ''.join(word)
        return(result)

    morse_list = [ 
            "A", ".-", 
            "B", "-...",
            "C", "-.-.",
            "D", "-..",
            "E", ".",
            "F", "..-.",
            "G", "--.",
            "H", "....",
            "I", "..",
            "J", ".---",
            "K", "-.-",
            "L", ".-..",
            "M", "--",
            "N", "-.",
            "O", "---",
            "P", ".--.",
            "Q", "--.-",
            "R", ".-.",
            "S", "...",
            "T", "-",
            "U", "..-",
            "V", "...-",
            "W", ".--",
            "X", "-..-",
            "Y", "-.--",
            "Z", "--..",
    ]

    def ord(char):
        return Brutus.alphabet.index(char) 

    def chr(ordinal):
        while (ordinal >= 26):
            ordinal = 0 + (ordinal - 26)
        while (ordinal <= -26):
            ordinal = 0 + (26 + ordinal)

        return Brutus.alphabet[ordinal]


    def morse(message, mode, delimiter):
        message = message.upper()
        message = message.strip()
        result = []
        
        if (mode == "encrypt"):
            for item in message:
                result.append(morse_list[morse_list.index(item) + 1])
                result.append(" ")

        elif (mode == "decrypt"):
            message = message.split(" ")
            for item in message:
                if (item == delimiter): 
                    result.append(" ")
                else:
                    result.append(morse_list[morse_list.index(item) - 1])
        print(''.join(result))
        return result

    def alphabet_substitution(message, cipher_alphabet):
        message = message.upper()
        result = []

        if cipher_alphabet == None:
            print("Please supply a ciphertext alphabet.")
        elif len(cipher_alphabet) != 26:
            print("Alphabet must be 26 characters")
        else:
            for c in message:
                if c == ' ':
                    result.append(" ")
                else:
                    index = alphabet.index(c)
                    c = cipher_alphabet[index]
                    result.append(c)
        result = list(filter(None, result ))
        return result 


    def is_ascii(s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True


    @click.command()
    @click.option('--list_ciphers', '--lc', '-lc', required=False, default=False, help="Lists supported ciphers")
    @click.option('--delimiter', '--d', '-d', required=False, default=False, help="Delimiter character")
    @click.option('--key', '--k', '-k', required=False, help="Key for ciphers that require it")
    @click.option('--mode', '--m', '-m', required=False, help="Whether to encrypt or decrypt")
    @click.option('--cipher', '--c', '-c', required=True, type=click.Choice(supported_ciphers), help="Cipher type to use")
    @click.option('--shift', '--s', '-s', required=False, default=None, help='Shift value to use. Accepts integers or "all"')
    @click.option('--message', '--M', '-M', required=True, help="Message input")
    @click.option('--cipher_alphabet', '--ca', '-ca', required=False, help='Supply a ciphertext alphabet for a simple substituion cipher')
    @click.option('--pretty_output', '--p', '-P', required=False, default=True, help='Supply a ciphertext alphabet for a simple substituion cipher')

    def brutus(list_ciphers, mode, cipher, shift, message, cipher_alphabet, delimiter, key, pretty_output):
        if (list_ciphers):
            print(supported_ciphers)
        elif (cipher == 'rot'):
            Rot.main(message, mode, shift)
        elif (cipher == 'alphasub'):
            alphabet_substitution(message, cipher_alphabet)
        elif (cipher == 'vigenere'):
            Vigenere.main(message, mode, key, pretty_output)
        elif (cipher == 'morse'):
            morse(message, mode, delimiter)

class Vigenere(Brutus):

    def main(message, mode, key, pretty_output):
        if mode == "encrypt":
            Vigenere.encrypt(message, key, pretty_output)
        if mode == "decrypt":
            Vigenere.decrypt(message, key, pretty_output) 
        if mode == "decrypt_brute_force":
            Vigenere.decrypt_brute_force(message ) 

    def decrypt_brute_force(message):
        result = []
        message = message.upper()
        print("Trying list of keys and seeing if returned plaintext resembles english...")
        with open("words_alpha.txt") as f:
            i = 0
            for line in f.readlines():
                line = line.rstrip()
                line = line.upper()
                i += 1
                if (len(line) <= len(message)):
                    string = Vigenere.decrypt(message,line,pretty_output=False)
                    print("(" + str(i) + ") Trying key \t" + line + "\t on cipher " + message + " got result: \t" + string)
                    with open("dict/" + string[0].lower() + ".txt") as g:
                        for word in g.readlines():
                            word = word.rstrip()
                            word = word.upper()
                            if string == word:
                                result.append([line, message, string])
                    f.close()

        print(result)
        return result



    def decrypt(message, key, pretty_output=True):
        message = message.upper()
        message.strip()

        result = [] 
        if pretty_output == True:
            vigenere_table = PrettyTable() 

        if (key == None):
            print("Please provide a key with --key or -k.")
        else:
            key = key.upper()

            # Set each column as a letter of the alphabet
            if pretty_output == True:
                for x in Brutus.alphabet: 
                    vigenere_table.add_column(x, [])    

            # Keys that are shorter than the message must be repeated until they are
            # of equal length
            if (len(key) < len(message)):
                key = Brutus.word_wrap(key, len(message))

            # Fill each row with a shifted alphabet based on the key. This will become
            # our lookup table for deciphering.
            for c in key:
                if pretty_output == True:
                    vigenere_table.add_row(Brutus.alphabet_wrap(Brutus.alphabet.index(c), Brutus.alphabet))
                result.append(Brutus.alphabet_wrap(Brutus.alphabet.index(c), Brutus.alphabet))

            ciphertext = []
            i = 0 
            for c in message:
                # What is the location of the current letter in its row?
                loc = result[i].index(c)
                # Find the letter in that same position in the alphabet
                cipher_char = Brutus.alphabet[loc]
                ciphertext.append(cipher_char)
                i += 1

            if pretty_output == True:
                table = vigenere_table.get_string()
                print(table)

            ciphertext = ''.join(ciphertext)
            return ciphertext 

    def encrypt(message, key, pretty_output=True):
        message = message.upper()
        message = message.replace(" ", "")

        result = [] 
        if pretty_output == True:
            vigenere_table = PrettyTable() 

        if (key == None):
            print("Please provide a key with --key or -k.")
        else:
            key = key.upper()

            # Keys that are shorter than the message must be repeated until they are
            # of equal length
            if (len(key) < len(message)):
                key = Brutus.word_wrap(key, len(message))
        
            # Set each column as a letter of the alphabet
            if pretty_output == True:
                for x in Brutus.alphabet: 
                    vigenere_table.add_column(x, [])    

            # Fill each row with a shifted alphabet based on the key. This will become
            # our lookup table for enciphering.
            result.insert(0, Brutus.alphabet) 
            for c in key:
                if pretty_output == True:
                    vigenere_table.add_row(Brutus.alphabet_wrap(Brutus.alphabet.index(c), Brutus.alphabet))
                result.append(Brutus.alphabet_wrap(Brutus.alphabet.index(c), Brutus.alphabet))

            ciphertext = []
            i = 0
            for c in message:
                # What is the location of the current letter in our alphabet?
                    loc = Brutus.alphabet.index(message[i])
                    
                    # Find the letter in the same location in our key row. 
                    cipher_char = result[i+1][loc]
                    ciphertext.append(cipher_char)
                    i += 1

            if pretty_output == True:
                table = vigenere_table.get_string()
                print(table)

            ciphertext = ''.join(ciphertext)
            print(ciphertext)
            return ciphertext 

class Rot(Brutus):
    def main(message, mode, shift):
        if mode == None:
            print("Please enter a mode with --mode encrypt|decrypt")
        elif mode == "encrypt":
            Rot.encrypt(message, shift)
        elif (shift == None):
            print("Please provide a shift value with --shift")
        elif mode == "decrypt":
            if (shift == "all"):
                Rot.decrypt_brute_force(message)
            else:
                Rot.decrypt(message,shift)

    @staticmethod
    def encrypt(message,shift_value):
        result = Rot.shift(message, shift_value)
        print(result)
        return(result)

    @staticmethod
    def decrypt(message, shift_value):
        result = Rot.shift(message, shift_value)
        print(result)
        return(result)

    @staticmethod
    def decrypt_brute_force(message):
        message = message.upper()
        result = []
        for i in range (0, 26):
            phrase = Rot.shift(message,i)
            result.append(phrase)
            substrings = Brutus.all_substrings(phrase)
            real_words = Brutus.find_english_strings(substrings)
            for j in real_words:
                if j:
                    print("\033[1;32;40m[+]\033[1;37;40m English phrase " + "'" + j + "' " + "detected with ROT-" + str(i) + " in " + phrase)
            #    else:
                    #print("\033[1;37;40m[-] " + phrase)
        #print(result)
        return str(''.join(result))

    @staticmethod
    def shift(message, shift_value):
        message = message.upper()
        phrase = []
        for c in message: 
            if c == ' ':
                phrase.append(" ")
            else:
                rot_c = Brutus.ord(c)
                rot_c += int(shift_value)
                phrase.append(Brutus.chr(rot_c))
        phrase = ''.join(phrase)
        return(phrase)
    