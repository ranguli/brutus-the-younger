class Rot:

    def decrypt_brute_force():
        print("yes")

    def encrypt(self, message, shift):
        message = message.upper()
        result = []

        if (shift == None):
            print("Specify a shift value with --shift or --s. See --help.")
        elif (shift == "all"):
            for i in range (0, 26):
                result.append(self.encrypt(message, i))
        else:
            for c in message: 
                if c == ' ':
                    result.append(" ")
                else:
                    rot_c = ord(c)
                    rot_c += int(shift)
                    result.append(chr(rot_c))
        #result = filter(None, result )
        print(''.join(result))
        return result
