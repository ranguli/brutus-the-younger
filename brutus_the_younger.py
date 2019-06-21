# -*- coding: utf-8 -*-
#!/usr/bin/env/python

from subprocess import call
import time

import click
from prettytable import PrettyTable
from nltk.corpus import words
import matplotlib.pyplot as plt
import numpy as np

class Brutus:
    alphabet_sets = []

    wordlist_dir = "wordlist/"
    wordlist = set(line.rstrip() for line in open(wordlist_dir + 'wordlist.txt'))

    supported_ciphers = ['rot','alphabet_substitution','morse', 'vigenere']

    graph_dir = "graphs/"
    graph_files = [
        'english_mongraphs.csv', 'english_digraphs.csv',
        'english_trigraphs.csv', 'english_quadgraphs.csv',
        'english_quintgraphs.csv'
    ]

    alphabet = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z'
    ]

    def clear_screen(self):
        '''OS-specific means to clear the terminal'''
        call('clear')

    @staticmethod
    def all_substrings(string):
        '''Genereate all possible substrings of a string, including the original'''
        j = 2
        a = []

        a.append(string)
        if len(string) != 1:
            while True:
                for i in range(len(string) - j+1):
                    a.append(string[i:i+j])
                if j == len(string):
                    break
                j += 1
        return a

    def find_english_strings(a):
        '''Check all generated substrings to see if they are English'''
        real_words = []
        for element in a:
            if len(element) > 3 and element.lower() in words.words():
                real_words.append(element)
        return real_words

    # List, the list/string in question

    def alphabet_wrap(x, list):
        """Returns a ciruclar list, useful for wrapping alphabets.

        Parameters:
        x (int) : Starting slice integer. 0 for entire phrase + wrapping.
        list (list) : The alphabet in list format to be wrapped

        Returns:
        list: Wrapped alphabet
        """
        result = []
        for i in range(x, (x + 26)):
            if i >= len(list):
                index = 0 + (i - 26)
                result.append(list[index])
            else:
                result.append(list[i])
        return result

    def pad_plaintext(word, length):
        word = list(word)
        for i in word:
            if len(word) != length:
                word.append(i)
        result = ''.join(word)
        return result

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
        while ordinal >= 26:
            ordinal = 0 + (ordinal - 26)
        while ordinal <= -26:
            ordinal = 0 + (26 + ordinal)

        return Brutus.alphabet[ordinal]


    def morse(message, mode, delimiter):
        message = message.upper()
        message = message.strip()
        result = []

        if mode == "encrypt":
            for item in message:
                result.append(morse_list[morse_list.index(item) + 1])
                result.append(" ")

        elif mode == "decrypt":
            message = message.split(" ")
            for item in message:
                if item == delimiter:
                    result.append(" ")
                else:
                    result.append(morse_list[morse_list.index(item) - 1])
        print(''.join(result))
        return result

    def alphabet_substitution(message, cipher_alphabet):
        message = message.upper()
        result = []

        if cipher_alphabet is None:
            print("Please supply a ciphertext alphabet.")
        elif len(cipher_alphabet) != 26:
            print("Alphabet must be 26 characters")
        else:
            for char in message:
                if char == ' ':
                    result.append(" ")
                else:
                    index = alphabet.index(char)
                    char = cipher_alphabet[index]
                    result.append(c)
        result = list(filter(None, result))
        return result


    def is_ascii(string):
        try:
            string.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def is_word(string):
        if string[1] in Brutus.alphabet_sets[Brutus.alphabet.index(string[1][0])]:
            return string

    def get_hist(ciphertext):
        histogram = {}
        ciphertext_hist = {
            "A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0, "E": 0.0, "F": 0.0, "G": 0.0,
            "H": 0.0, "I": 0.0, "J": 0.0, "K": 0.0, "L": 0.0, "M": 0.0, "N": 0.0,
            "O": 0.0, "P": 0.0, "Q": 0.0, "R": 0.0, "S": 0.0, "T": 0.0, "U": 0.0,
            "V": 0.0, "W": 0.0, "X": 0.0, "Y": 0.0, "Z": 0.0
        }

        for char in ciphertext:
            if char != ' ':
                ciphertext_hist[char.upper()] += 1
        total = len(ciphertext)
        for char in ciphertext_hist:
            ciphertext_hist[char.upper()] = (ciphertext_hist[char.upper()] / total) * 100

        for key, value in Brutus.letter_frequency.items():
            if key in ciphertext_hist:
                histogram[key] = value

        return(ciphertext_hist, histogram)

    def plot_hist(ciphertext):

        # This is still being migrated from an SO example :-)

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
    @click.option('--cipher', '--c', '-c', required=True,
            type=click.Choice(supported_ciphers), help="Cipher type to use")
    @click.option('--shift', '--s', '-s', required=False, default=None, help='Shift value to use. Accepts integers or "all"')
    @click.option('--message', '--M', '-M', required=True, help="Message input")
    @click.option('--cipher_alphabet', '--ca', '-ca', required=False, default=False, help='Supply a ciphertext alphabet for a simple substituion cipher')
    @click.option('--pretty_output', '--p', '-P', required=False, default=True, help='Supply a ciphertext alphabet for a simple substituion cipher')

    def brutus(list_ciphers, mode, cipher, shift, message, cipher_alphabet, delimiter, key, pretty_output):

        for i in Brutus.alphabet:
            # This is gross, fix it
            Brutus.alphabet_sets.append(set(line.rstrip().upper() for line in open(Brutus.wordlist_dir + i.lower() + ".txt")))

        if list_ciphers:
            print(supported_ciphers)
        elif cipher == 'rot':
            Rot.main(message, mode, shift)
        elif cipher == 'alphasub':
            alphabet_substitution(message, cipher_alphabet)
        elif cipher == 'vigenere':
            Vigenere.main(message, mode, key, pretty_output)
        elif cipher == 'morse':
            morse(message, mode, delimiter)

class Vigenere():

    def main(message, mode, key, pretty_output):
        if mode == "encrypt":
            Vigenere.encrypt(message, key, pretty_output)
        if mode == "decrypt":
            Vigenere.decrypt(message, key, pretty_output)
        if mode == "decrypt_dict_attack":
            Vigenere.decrypt_dict_attack(message)

    def decrypt_dict_attack(message):
        '''Uses brute force to attempt to decrypt a Vigenere cipher'''
        start = time.time()
        message = message.upper()
        improved_wordlist = []
        finalists = []
        # Create a smaller subset of possible matches based on length. We don't need to try comparing longer words
        # to a shorter one because we know they can't equal each other.
        for key in Brutus.wordlist:
            if len(key) <= len(message):
                improved_wordlist.append(key)

        improved_wordlist = set(improved_wordlist)

        for key in improved_wordlist:
            finalists.append([message, Vigenere.decrypt(message, key, pretty_output=False), key])

        result = list(filter(None, map(Brutus.is_word, finalists)))
        end = time.time()

        for i in result:
            print("Cipher " + str(i[0]) + " returned " + str(i[1]) + " with key " + str(i[2]))

        print("Finished in " + str(int(end - start)) + "s.")
        return result

    @staticmethod
    def decrypt(message, key, pretty_output=True):
        start = time.time()
        message = message.upper().strip()

        result = []
        if pretty_output:
            vigenere_table = PrettyTable()

        if key is None:
            print("Please provide a key with --key or -k.")
        else:
            key = key.upper()

            # Set each column as a letter of the alphabet
            if pretty_output:
                for letter in Brutus.alphabet:
                    vigenere_table.add_column(letter, [])

            # Keys that are shorter than the message must be repeated until they are
            # of equal length
            if len(key) < len(message):
                key = Brutus.pad_plaintext(key, len(message))

            # Fill each row with a shifted alphabet based on the key. This will become
            # our lookup table6 for deciphering.
            for char in key:
                if pretty_output:
                    vigenere_table.add_row(Brutus.alphabet_wrap(Brutus.alphabet.index(char), Brutus.alphabet))
                result.append(Brutus.alphabet_wrap(Brutus.alphabet.index(char), Brutus.alphabet))

            ciphertext = []
            i = 0
            for char in message:
                # What is the location of the current letter in its row?
                if char == ' ':
                    ciphertext.append(char)
                else:
                    loc = result[i].index(char)
                    cipher_char = Brutus.alphabet[loc]
                    ciphertext.append(cipher_char)
                i += 1

            if pretty_output:
                table = vigenere_table.get_string()
                print(table)

            end = time.time()
            print("Finished in " + str(int(end - start)) + "s.")
            ciphertext = ''.join(ciphertext)
            print(ciphertext)
            return ciphertext

    @staticmethod
    def encrypt(message, key, pretty_output=True):
        message = message.upper()
        message = message.replace(" ", "")

        result = []
        if pretty_output:
            vigenere_table = PrettyTable()

        if key is None:
            print("Please provide a key with --key or -k.")
        else:
            key = key.upper()

            # Keys that are shorter than the message must be repeated until they are
            # of equal length
            if len(key) < len(message):
                key = Brutus.pad_plaintext(key, len(message))

            # Set each column as a letter of the alphabet
            if pretty_output:
                for letter in Brutus.alphabet:
                    vigenere_table.add_column(letter, [])

            # Fill each row with a shifted alphabet based on the key. This will become
            # our lookup table for enciphering.
            result.insert(0, Brutus.alphabet)
            for char in key:
                if pretty_output:
                    vigenere_table.add_row(Brutus.alphabet_wrap(Brutus.alphabet.index(char), Brutus.alphabet))
                result.append(Brutus.alphabet_wrap(Brutus.alphabet.index(char), Brutus.alphabet))

            ciphertext = []
            i = 0
            for char in message:
                # What is the location of the current letter in our alphabet?
                loc = Brutus.alphabet.index(message[i])

                # Find the letter in the same location in our key row.
                cipher_char = result[i+1][loc]
                ciphertext.append(cipher_char)
                i += 1

            if pretty_output:
                table = vigenere_table.get_string()
                print(table)

            ciphertext = ''.join(ciphertext)
            print(ciphertext)
            return ciphertext


class Rot:
    """Provides Rot cipher methods"""

    def main(message, mode, shift):
        if mode is None:
            print("Please enter a mode with --mode encrypt|decrypt")
        elif mode == "encrypt":
            Rot.encrypt(message, shift)
        elif shift is None:
            print("Please provide a shift value with --shift")
        elif mode == "decrypt":
            if shift == "all":
                Rot.decrypt_brute_force(message)
            else:
                Rot.decrypt(message, shift)

    @staticmethod
    def encrypt(message, shift_value):
        result = Rot.shift(message, shift_value)
        print(result)
        return result

    @staticmethod
    def decrypt(message, shift_value):
        result = Rot.shift(message, shift_value)
        #print(result + "\n")
        return result

    @staticmethod
    def decrypt_brute_force(message):
        message = message.upper()
        for i in range(0, 26):
            phrase = Rot.shift(message, i)
            if Brutus.is_word(phrase) is not None:
                print(phrase)

    @staticmethod
    def shift(message, shift_value):
        message = message.upper()
        phrase = []
        for char in message:
            if char == ' ':
                phrase.append(" ")
            else:
                rot_char = Brutus.ord(char)
                rot_char += int(shift_value)
                phrase.append(Brutus.chr(rot_char))
        phrase = ''.join(phrase)
        return phrase

brutus = Brutus()
brutus.brutus()
