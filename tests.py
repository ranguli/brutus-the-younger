import pytest
from brutus_the_younger import Brutus
from brutus_the_younger import Rot
from brutus_the_younger import Vigenere 

brutus = Brutus()

test_alphabet = [
    'A','B','C','D','E','F','G','H','I','J',
    'K','L','M','N','O','P','Q','R','S','T',
    'U','V','W','X','Y','Z'
]

class TestSubstring(object):

    def test_all_subtrings_1(object):
        expected = ['CHEESE', 'CH', 'HE', 'EE', 'ES', 'SE', 'CHE', 'HEE', 'EES', 'ESE', 'CHEE', 'HEES', 'EESE', 'CHEES', 'HEESE', 'CHEESE']
        result = Brutus.all_substrings("CHEESE")
        assert result == expected 

    def test_all_substrings_2(object):
        expected = ['ATTACK AT DAWN', 'AT', 'TT', 'TA', 'AC', 'CK', 'K ', ' A', 'AT', 'T ', ' D', 'DA', 'AW', 'WN', 'ATT', 'TTA', 'TAC', 'ACK', 'CK ', 'K A', ' AT', 'AT ', 'T D', ' DA', 'DAW', 'AWN', 'ATTA', 'TTAC', 'TACK', 'ACK ', 'CK A', 'K AT', ' AT ', 'AT D', 'T DA', ' DAW', 'DAWN', 'ATTAC', 'TTACK', 'TACK ', 'ACK A', 'CK AT', 'K AT ', ' AT D', 'AT DA', 'T DAW', ' DAWN', 'ATTACK', 'TTACK ', 'TACK A', 'ACK AT', 'CK AT ', 'K AT D', ' AT DA', 'AT DAW', 'T DAWN', 'ATTACK ', 'TTACK A', 'TACK AT', 'ACK AT ', 'CK AT D', 'K AT DA', ' AT DAW', 'AT DAWN', 'ATTACK A', 'TTACK AT', 'TACK AT ', 'ACK AT D', 'CK AT DA', 'K AT DAW', ' AT DAWN', 'ATTACK AT', 'TTACK AT ', 'TACK AT D', 'ACK AT DA', 'CK AT DAW', 'K AT DAWN', 'ATTACK AT ', 'TTACK AT D', 'TACK AT DA', 'ACK AT DAW', 'CK AT DAWN', 'ATTACK AT D', 'TTACK AT DA', 'TACK AT DAW', 'ACK AT DAWN', 'ATTACK AT DA', 'TTACK AT DAW', 'TACK AT DAWN', 'ATTACK AT DAW', 'TTACK AT DAWN', 'ATTACK AT DAWN']
        result = Brutus.all_substrings("ATTACK AT DAWN")
        assert result == expected
    
    def test_all_substrings_3(object):
        expected = ['A']
        result = Brutus.all_substrings("A")
        assert result == expected


class TestWrap(object):

    def test_alphabet_wrap_1(self):
        result = Brutus.alphabet_wrap(0, test_alphabet)
        assert result == test_alphabet

    def test_alphabet_wrap_2(self):
        result = Brutus.alphabet_wrap(5, test_alphabet)
        expected = ['F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','A','B','C','D','E']
        assert result == expected 

    def test_alphabet_wrap_3(self):
        result = Brutus.alphabet_wrap(26, test_alphabet)
        assert result == test_alphabet 


class TestRot(object):

    def test_rot_shift_1(self):
        result = Rot.shift("hello", 1)
        assert result == "IFMMP"

    def test_rot_shift_2(self):
        result = Rot.shift("A", 26)
        assert result == "A"

    def test_rot_shift_3(self):
        result = Rot.shift("A", 0)
        assert result == "A"

    def test_rot_shift_4(self):
        result = Rot.shift("A A", 0)
        assert result == "A A"

    def test_rot_decrypt_1(self):
        assert Rot.decrypt("hello", 1) == Rot.shift("hello", 1)

    def test_rot_encrypt_1(self):
        assert Rot.encrypt("hello", 1) == Rot.shift("hello", 1)

    def test_rot_ecrypt_decrypt_1(self):
        assert Rot.encrypt("hello", 1) == Rot.decrypt("hello", 1)

class TestVigenere(object):
    def test_vigenere_1(self):
        assert Vigenere.encrypt("hello", "test", False) == "AIDEH" 

    def test_vigenere_2(self):
        assert Vigenere.decrypt("AIDEH", "test", False) == "HELLO" 

    def test_vigenere_3(self):
        assert Vigenere.encrypt("ATTACK AT DAWN", "LEMON", False) == "LXFOPVEFRNHR" 

