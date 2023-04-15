import aes
import binascii
S = [3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12,
    15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4,
    8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2,
    0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14,
    1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13,
    15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1,
    7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0,
    1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6]

k = b'do viet hung'


def pad(data):
    n_size = 32
    data_size = len(data)
    padding_length = n_size - ((n_size + 1) % data_size)
    pre_padding = bytes(chr(49),encoding='utf-8')
    padding = bytes(chr(48)*padding_length,encoding='utf-8')
    return data + pre_padding + padding

def split_word(data):
    pre_word = []
    for i in range(0,len(data),4):
        pre_word.append(hex(aes.bytes_to_long(data[i:i+4])))
    return pre_word

def ROTL(value,n):
    return int(( value << n ) & 0xFFFFFFFF | ( value >> (32-n) ))

def word_gen(pre_word):
    phi = 0x9e3779b9
    for i in range(8,100):    
        new_word = ROTL((pre_word[i-8] ^ pre_word[i-5] ^ pre_word[i-3] ^ pre_word[i-1] ^ phi ^ hex(i)),11)
        pre_word.append(new_word)
    return pre_word
#def subkey_gen(pre_word):
#print(ROTL(0x646f2076,11
def sbox(word):
    word_int_array = [(word >> i) & 0b1111 for i in range(0, 32, 4)]
    for i in range(len(word_int_array)):
        word_int_array[i] = S[word_int_array[i]]
    num = sum([(word_int_array[i] << (28 - i * 4)) for i in range(8)])
    return num

    
print(sbox(0x12345678))         