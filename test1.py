import aes
S = [[3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12],
    [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4],
    [8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2],
    [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14],
    [1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13],
    [15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1],
    [7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0],
    [1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6]]


def multi_append(*args,array):
    array.extend(args)
    return array
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
        pre_word.append(aes.bytes_to_long(data[i:i+4]))
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
def split_128(word):
    word_array = [(word >> 96) & 0xffffffff, (word >> 64) & 0xffffffff, (word >> 32) & 0xffffffff, word & 0xffffffff]
    return word_array

def sbox_32(word,k):
    word_int_array = [(word >> i) & 0b1111 for i in range(0, 32, 4)]
    for i in range(len(word_int_array)):
        word_int_array[i] = S[k][word_int_array[i]]
    num = sum([(word_int_array[i] << (28 - i * 4)) for i in range(8)])
    return num

def sbox_128(word,k):
    word_array = [(word >> 96) & 0xffffffff, (word >> 64) & 0xffffffff, (word >> 32) & 0xffffffff, word & 0xffffffff]
    for i in word_array:
        i = sbox_32(i,k)
    word = (word_array[0] << 96) | (word_array[1] << 64) | (word_array[2] << 32) | word_array[3]
    return word

def pre_word_split(pre_word):
    split_pw = []
    for i in range(0,len(pre_word,4)):
        temp =[]
        for j in range(i,i+4):
            temp.append(pre_word[j])
        split_pw.append(temp)
    return split_pw
def key_schedule(split_pw):
    k = 3
    for i in split_pw:
        for j in range(4):
            split_pw[i][j] = sbox_32(split_pw[i][j],k)
        k = k - 1
        if k < 0 :
            k = 7
    return split_pw
def merge_key_schedule(key_schedule):
    merged_key =[]
    for i in key_schedule:
        merged_key.append((i[0] << 96) | (i[1] << 64) | (i[2] << 32) | i[3])
    return merged_key

def LTM(key_mixing) :
    key_mixing = sbox_128(key_mixing)
    key_mixing = bytearray(key_mixing)
    X0 = key_mixing[0]
    X1 = key_mixing[1]
    X2 = key_mixing[2]
    X3 = key_mixing[3]
    X0 = ROTL(X0,13)
    X2 = ROTL(X2,13)
    X1 = X1 ^ X2 ^ X3
    X3 = X3 ^ X2 ^ ROTL(X0,3)
    X1 = ROTL(X1,1)
    X3 = ROTL(X3,7)
    X0 = X0 ^ X1 ^ X3
    X2 = X2 ^ X3 + ROTL(X1,7)
    X0 = ROTL(X0,5)
    X2 = ROTL(X2,22)
    return key_mixing
def euclidean_algorithm(a, b):
    """
    """
    s0, s1, t0, t1 = 1, 0, 0, 1
    while b:
        q, r = divmod(a, b) #chia lay du
        a, b = b, r
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return a, s0, t0


def inverse(num, p):
    """
    Calculates the inverse of a number in 2^32
    """
    gcd, x, _ = euclidean_algorithm(num, p)
    if gcd == 1:
        return x % p
    else:
        raise ValueError("The number is not invertible in 2^32")

def LSFR(array,a):
    new_array =[] 
    new_array.append(new_array[9] ^ inverse(a) ^ array[3] ^ (a*array[0]))
    array = new_array + array[9:]
    return array

def mux(c,x,y):
    c = bin(c)
    if( c[(len(c) - 1 ):] == '0'):
        return x
    else :
        return y
def Trans(Z):
    M = 0x54655307
    return ROTL((M*Z)%(2**32),7)

def FSM(R1,R2,S1,S8,S9):
    R1_next =(R2 + mux(R1, S1, S1 ^ S8)) % (2**32)
    R2_next = Trans(R1)
    FSM_turn = ((S9 + R1_next)%(2**32)) ^ R2_next
    return R1_next,R2_next,FSM_turn

def encrypt(k):
    #1 khoi tao k  va pading 256 bit
    k_pad = pad(k)
    split_w = split_word(k_pad) #2 chia thanh 8 word ban dau
    pre_w = word_gen(split_w) #gen 100 word 
    pre_w_split = pre_word_split(pre_w)# chia thanh ma tran 2 chieu 25 x 4
    key_schedule_gen = key_schedule(pre_w_split)
    sub_key =merge_key_schedule(key_schedule_gen)
    #intialize B0(128 bit)
    B_temp = b'16bytebtempforst'
    B_temp = aes.bytes_to_long(B_temp)
    k=0
    for i in range(len(sub_key) - 1):
        key_mix = B_temp ^ i
        B_temp = LTM(key_mix)
        if i == 11 :
            vector_12 = B_temp
        elif i == 17 :
            vector_18 = B_temp
        elif i ==  23:
            vector_24 = B_temp ^ sub_key[i+1] 
    S9,S8,S7,S6 = split_128[vector_12]
    R1,S4,R2,S5 = split_128[vector_18]
    S3,S2,S1,S0 = split_128[vector_24]
    LSFR_array = []
    LSFR_array = multi_append(S0,S1,S2,S3,S4,S5,S6,S7,S8,S9,LSFR_array = LSFR_array)
    #time 
    t = 10
    ft = []
    Gk = []
    for i in t :
        a = 0x23
        LSFR_array = LSFR(LSFR_array)
        LSFR_array_temp = LSFR_array
        
        for j in range(4):
            R1,R2,F_turn = FSM(R1,R2,LSFR_array_temp[1],LSFR_array_temp[8],LSFR_array_temp[9])
            LSFR_array_temp = LSFR(LSFR_array_temp)
            ft.append(F_turn)
        for m in range(ft) :
            Gk.append(ft[m]^LSFR_array[m])
    
"""main"""
k = b'do viet hung'
if __name__ == "__main__":
    print(encrypt(k))




        

    


 


                    
    






    
