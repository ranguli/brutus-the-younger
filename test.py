alphabet = [
    'A','B','C','D','E','F','G','H','I','J',
    'K','L','M','N','O','P','Q','R','S','T',
    'U','V','W','X','Y','Z'
]

""" Returns a ciruclar loop """

x = alphabet.index('H')

def list_loop(x, alpha):
    result = []
    for i in range(x, (x + 26)):
        if i >= len(alpha):
            index = 0 + (i - 26)
            result.append(alpha[index])
        else:
            result.append(alpha[i])
    print(result)

list_loop(x, alphabet)