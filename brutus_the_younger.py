# -*- coding: utf-8 -*-
#!/usr/bin/env/python
import csv
from subprocess import call
import cProfile
import time
import os.path

import pprint
import click
from prettytable import PrettyTable
from itertools import permutations
from nltk.corpus import words
import matplotlib.pyplot as plt
import numpy as np

class Brutus(object):
    alphabet_sets = []
    wordlist = set(line.rstrip().upper() for line in open('words_alpha.txt'))

    supported_ciphers = ['rot','alphabet_substitution','morse', 'vigenere']

    def __init__():
        language_files = [
            'english_mongraphs.csv', 'english_digraphs.csv', 
            'english_trigraphs.csv', 'english_quadgraphs.csv', 
            'english_quintgraphs.csv'
        ]


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
        result = list(filter(None, result))
        return result 


    def is_ascii(s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True
    
    def is_word(string):
        if (string[1] in Brutus.alphabet_sets[Brutus.alphabet.index(string[1][0])]):
            return string

    def get_hist(ciphertext):
        histogram = {} 
        ciphertext_hist = {
            "A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0, "E": 0.0, "F": 0.0, "G": 0.0, 
            "H": 0.0, "I": 0.0, "J": 0.0, "K": 0.0, "L": 0.0, "M": 0.0, "N": 0.0, 
            "O": 0.0, "P": 0.0, "Q": 0.0, "R": 0.0, "S": 0.0, "T": 0.0, "U": 0.0, 
            "V": 0.0, "W": 0.0, "X": 0.0, "Y": 0.0, "Z": 0.0
        }

        for c in ciphertext:
            if c != ' ':
                ciphertext_hist[c.upper()] += 1
        total = len(ciphertext)
        for c in ciphertext_hist:
            ciphertext_hist[c.upper()] = (ciphertext_hist[c.upper()] / total) * 100

        for key, value in Brutus.letter_frequency.items():
            if key in ciphertext_hist:
                histogram[key] = value

        return(ciphertext_hist, histogram)

    def plot_hist(ciphertext):

        ciphertext_hist, histogram = Brutus.get_hist(ciphertext)

        n_groups = len(Brutus.letter_frequency.values())

        womenMeans = list(ciphertext_hist.values())
        #womenMeans = (25, 32, 34, 20, 25)
        #menMeans = (20, 35, 30, 35, 27)
        menMeans = list(Brutus.letter_frequency.values())
        indices = range(len(womenMeans))
        names = list(Brutus.letter_frequency.keys())
        # Calculate optimal width
        width = np.min(np.diff(indices))/3.

        index = np.arange(n_groups)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(indices-width/2.,womenMeans,width, align="center", color='b', label='Ciphertext Histogram')
        ax.bar(indices+width/2.,menMeans,width,color='r', align="center", label='English Histogram')
        ax.set_xticks(index + width / 2)
        ax.axes.set_xticklabels(names)
        ax.set_xlabel('Letters')
        ax.set_ylabel('Frequency')

        ax.legend()
        plt.show()



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

        for i in Brutus.alphabet:
            Brutus.alphabet_sets.append(set(line.rstrip().upper() for line in open("dict/" + i.lower() + ".txt")))

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
            Vigenere.decrypt_brute_force(message)

    def decrypt_brute_force(message):
        start = time.time()
        message = message.upper()
        improved_wordlist = []
        finalists = [] 
        # Create a smaller subset of possible matches based on length. We don't need to try comparing longer words
        # to a shorter one because we know they can't equal each other.
        for key in Brutus.wordlist:
            if (len(key) <= len(message)):
                improved_wordlist.append(key)
        
        improved_wordlist = set(improved_wordlist)

        for key in improved_wordlist:
            finalists.append([message, Vigenere.decrypt(message,key,pretty_output=False), key])

        result = list(filter(None, map(Brutus.is_word, finalists)))
        end = time.time()

        for i in result:
            print("Cipher " + str(i[0]) + " returned " + str(i[1]) + " with key " + str(i[2]))

        print("Finished in " + str(int(end - start)) + "s.")
        return result

    def decrypt(message, key, pretty_output=True):
        start = time.time()
        message = message.upper().strip()

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
            # our lookup table6 for deciphering.
            for c in key:
                if pretty_output == True:
                    vigenere_table.add_row(Brutus.alphabet_wrap(Brutus.alphabet.index(c), Brutus.alphabet))
                result.append(Brutus.alphabet_wrap(Brutus.alphabet.index(c), Brutus.alphabet))

            ciphertext = []
            i = 0 
            for c in message:
                # What is the location of the current letter in its row?
                if (c == ' '):
                    ciphertext.append(c)
                else:
                    loc = result[i].index(c)
                    cipher_char = Brutus.alphabet[loc]
                    ciphertext.append(cipher_char)
                i += 1

            if pretty_output == True:
                table = vigenere_table.get_string()
                print(table)

            end = time.time()
            ciphertext = ''.join(ciphertext)
            print(ciphertext)
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
        #print(result + "\n")
        return(result)

    @staticmethod
    def decrypt_brute_force(message):
        message = message.upper()
        result = []
        for i in range (0, 26):
            phrase = Rot.shift(message,i)
            if Brutus.is_word(phrase) is not None:
                print(phrase)

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
    
