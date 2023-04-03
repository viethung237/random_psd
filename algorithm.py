class MT:
    def __init__(self):
        self.index = 624
        self.state = [0]*624

    def seed(self, seed_value):
        self.index = 624
        self.state[0] = seed_value
        for i in range(1, 624):
            self.state[i] = 0xffffffff & (1812433253 * (self.state[i-1] ^ (self.state[i-1] >> 30)) + i)

    def rand(self):
        if self.index >= 624:
            self.twist()
        y = self.state[self.index]
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9d2c5680)
        y = y ^ ((y << 15) & 0xefc60000)
        y = y ^ (y >> 18)
        self.index += 1
        return 0xffffffff & y

    def twist(self):
        for i in range(624):
            y = (self.state[i] & 0x80000000) + (self.state[(i+1) % 624] & 0x7fffffff)
            self.state[i] = self.state[(i+397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.state[i] = self.state[i] ^ 0x9908b0df
        self.index = 0
rng = MT()
rng.seed(12345)
random_sequence = [rng.rand() for i in range(500000)]
binary = ''
for i in random_sequence:
    binary += str(bin(i))[-1:]
with open('result.txt','w',encoding="utf-8") as text :
    text.write(binary)
