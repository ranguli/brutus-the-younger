#!/usr/bin/env/python
import click

supported_ciphers = ['rot','alphabet_substitution','morse']

alphabet = [
    'A','B','C','D','E','F','G','H','I','J',
    'K','L','M','N','O','P','Q','R','S','T',
    'U','V','W','X','Y','Z'
]

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
    return alphabet.index(char) 

def chr(ordinal):
    while (ordinal >= 26):
        ordinal = 0 + (ordinal - 26)
    while (ordinal <= -26):
        ordinal = 0 + (26 + ordinal)

    return alphabet[ordinal]

def rot(message, shift):
    message = message.upper()
    result = []

    if (shift == None):
        print("Specify a shift value with --shift or --s. See --help.")
    elif (shift == "all"):
        for i in range (0, 26):
            result.append(rot(message, i))
    else:
        for c in message: 
            if c == ' ':
                result.append(" ")
            else:
                rot_c = ord(c)
                rot_c += int(shift)
                result.append(chr(rot_c))
    result = list(filter(None, result ))
    print(''.join(result))
    return result

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
    print(''.join(result))
    return result 


@click.command()
@click.option('--list_ciphers', '--lc', '-lc', required=False, default=False, help="Lists supported ciphers")
@click.option('--delimiter', '--d', '-d', required=False, default=False, help="Delimiter character")
@click.option('--mode', '--m', '-m', required=False, default="encrypt", help="Whether to encrypt or decrypt")
@click.option('--cipher', '--c', '-c', required=True, type=click.Choice(supported_ciphers), help="Cipher type to use")
@click.option('--shift', '--s', '-s', required=False, default=None, help='Shift value to use. Accepts integers or "all"')
@click.option('--message', '--M', '-M', required=True, help="Message input")
@click.option('--cipher_alphabet', '--ca', '-ca', required=False, help='Supply a ciphertext alphabet for a simple substituion cipher')

def brutus(list_ciphers, mode, cipher, shift, message, cipher_alphabet, delimiter):
    if (list_ciphers):
        print(supported_ciphers)
    if (cipher == 'rot'):
        rot(message, shift)
    if (cipher == 'alphasub'):
        alphabet_substitution(message, cipher_alphabet)
    if (cipher == 'morse'):
        morse(message, mode, delimiter)

if __name__ == '__main__':
    brutus()