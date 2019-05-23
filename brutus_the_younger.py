#!/usr/bin/env/python
from prettytable import PrettyTable
from itertools import permutations
import pprint
import click
from colorama import Fore

class Brutus(object):

    supported_ciphers = ['rot','alphabet_substitution','morse', 'vigenere']

    alphabet = [
        'A','B','C','D','E','F','G','H','I','J',
        'K','L','M','N','O','P','Q','R','S','T',
        'U','V','W','X','Y','Z'
    ]

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

    def vigenere(message, mode, key):
        message = message.upper()
        message.strip()

        result = [] 
        vigenere_table = PrettyTable() 

        if (key == None):
            print("Please provide a key with --key or -k.")
        else:
            key = key.upper()

            if (mode == "encrypt"):

                # Keys that are shorter than the message must be repeated until they are
                # of equal length
                if (len(key) < len(message)):
                    key = word_wrap(key, len(message))
            
                # Set each column as a letter of the alphabet
                for x in alphabet: 
                    vigenere_table.add_column(x, [])    

                # Fill each row with a shifted alphabet based on the key. This will become
                # our lookup table for enciphering.
                result.insert(0, alphabet) 
                for c in key:
                    vigenere_table.add_row(alphabet_wrap(alphabet.index(c), alphabet))
                    result.append(alphabet_wrap(alphabet.index(c), alphabet))

                ciphertext = []
                i = 0
                for c in message:
                    # What is the location of the current letter in our alphabet?
                    loc = alphabet.index(message[i])
                    
                    # Find the letter in the same location in our key row. 
                    cipher_char = "\033[1;32;40m" + result[i+1][loc]
                    ciphertext.append(cipher_char)
                    i += 1
                
                table = vigenere_table.get_string()
                print(table)
                print(''.join(ciphertext))


            return ciphertext 

    @click.command()
    @click.option('--list_ciphers', '--lc', '-lc', required=False, default=False, help="Lists supported ciphers")
    @click.option('--delimiter', '--d', '-d', required=False, default=False, help="Delimiter character")
    @click.option('--key', '--k', '-k', required=False, help="Key for ciphers that require it")
    @click.option('--mode', '--m', '-m', required=False, default="encrypt", help="Whether to encrypt or decrypt")
    @click.option('--cipher', '--c', '-c', required=True, type=click.Choice(supported_ciphers), help="Cipher type to use")
    @click.option('--shift', '--s', '-s', required=False, default=None, help='Shift value to use. Accepts integers or "all"')
    @click.option('--message', '--M', '-M', required=True, help="Message input")
    @click.option('--cipher_alphabet', '--ca', '-ca', required=False, help='Supply a ciphertext alphabet for a simple substituion cipher')

    def brutus(list_ciphers, mode, cipher, shift, message, cipher_alphabet, delimiter, key):
        if (list_ciphers):
            print(supported_ciphers)
        elif (cipher == 'rot'):
            Rot.encrypt(message, shift)
        elif (cipher == 'alphasub'):
            alphabet_substitution(message, cipher_alphabet)
        elif (cipher == 'vigenere'):
            vigenere(message, mode, key)
        elif (cipher == 'morse'):
            morse(message, mode, delimiter)

class Rot(Brutus):

    def decrypt_brute_force():
        print("yes")

    def encrypt(message, shift):
        message = message.upper()
        result = []

        if (shift == None):
            print("Specify a shift value with --shift or --s. See --help.")
        elif (shift == "all"):
            for i in range (0, 26):
                result.append(Rot.encrypt(message, i))
        else:
            for c in message: 
                if c == ' ':
                    result.append(" ")
                else:
                    rot_c = Brutus.ord(c)
                    rot_c += int(shift)
                    result.append(Brutus.chr(rot_c))
        result = filter(None, result )
        print(''.join(result))
        return str(''.join(result))

brutus_the_younger = Brutus()
brutus_the_younger.brutus()