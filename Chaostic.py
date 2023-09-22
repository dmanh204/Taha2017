class Taha:
    def __init__(self,key, iv):
        self.P1 = 0xd92921a8
        self.P2 = 0b1101111011110000001111000010110
        self.Us = (iv&0xffffffff00000000) >> 32  # 0x3281395e
        self.Up = iv & 0xffffffff #0xbba3e74b
        self.Ks_1 =  (key&0xffffffff00000000) >>32
        self.Ks_2 = LS3bit(self.Ks_1)
        self.Ks_3 = LS3bit(self.Ks_2)
        self.Kp_1 =  key & 0xffffffff
        self.Kp_2 = LS3bit(self.Kp_2)
        self.Kp_3 = LS3bit(self.Kp_3)
        self.Q1 = self.Us
        self.Q2 = self.Up
        self.Xs_1 = self.Xs_2 = self.Xs_3 = self.Xp_1 = self.Xp_2 = self.Xp_3 = 0
    def LSFR(input):
        a = input
        for i in range(32):
            x = (a ^ (a>>10) ^ (a>>30) ^(a>>31))&0b1 # LFSR 32bit = x^32 + x^22 + x^2 +x^1
            a = ((x<<31)&0xffffffff)|(a>>1)
        return a    # Tra ve gia tri a la gia tri trong thanh ghi hien tai, gia tri output cua qua trinh LFSR thuc ra chinh la dau vao, ta dang tinh gia tri dau ra cua lan thuc hien ke tiep.
    def SkewTentMap(self):
        Us = self.Us
        Ks_1 = self.Ks_1
        Ks_2 = self.Ks_2
        Ks_3 = self.Ks_3
        P1 = self.P1
        Q1 = self.Q1
        n = 32
        F1 = (Us + Ks_1 *Xs_1 +Ks_2 *Xs_2 +Ks_3*Xs_3)%(2**n)

        # skewTentMap
        if(0<Xs_1<P1):
            X0 = math.ceil(2**n *Xs_1/P1)%(2**n)
        elif(Xs_1 == P1):
            X0 = (2**n)-1
        elif(P1<Xs_1<2**n):
            X0 = math.ceil(2**n * (2**n - Xs_1)/(2**n - P1))%(2**n)
        # Tinh Xs:
        Xs = X0 ^ Q1
        # Update tham so:
        self.Xs_3, self.Xs_2, self.Xs_1 = Xs_2, Xs_1, Xs

    def PWLCMap(self):
        Up = self.Up
        Kp_1 = self.Kp_1
        Kp_2 = self.Kp_2
        Kp_3 = self.Kp_3
        P2 = self.P2
        Q2 = self.Q2
        n = 32

        F2 = (Up+ Kp_1 *Xp_1 + Kp_2 *Xp_2 + Kp_3 *Xp_3)%(2**n)
        # PWLC map:
        if(0<Xp_1<P2):
            X0 = math.ceil(2**n *Xp_1)%(2**n)
        elif(P2< Xp_1<2**(n-1)):
            X0 = math.ceil(2**n * (Xp_1 - P2)/(2**(n-1) - P2))%(2**n)
        elif(2^(n-1) < Xp_1 < 2**n - P2):
            X0 = math.ceil(2**n * (2**n - P2 - Xp_1)/(2**(n-1) - P2))%(2**n)
        elif(2**n - P2 < Xp_1 < 2**n - 1):
            X0 = math.ceil(2**n * (2**n - Xp_1)/P2)%(2**n)
        else:
            X0 = 2**n -1 -P2

        Xp = X0 ^ Q2
        # update tham so
        self.Xp_3, self.Xp_2, self.Xp_1 = Xp_2, Xp_1, Xp
    def LS3bit(a):
        a = ((a << 3)&0xffffffff) | (a >> 29)
        return a
    def run(self):
        output = ""
        iNumber = int(input("Insert number of iteration: "))
        for i in range(iNumber):
            self.SkewTentMap()
            self.PWLCMap()
            self.Q1 = LFSR(self.Q1)# update next value Q1
            self.Q2 = LFSR(self.Q2)# update next value Q2
            # Output Xg:
            if (0< (Xp_2 ^ Xs_2)<2**(n-1)):
                Xg = Xs_1
            else:
                Xg = Xp_1
            output += byte2bin(Xg)
        return output
    def byte2bin(integer):
        string =""
        for i in range(32):
            x = 0x01 << (31-i)
            x = x & integer
            x = x >> (31 - i)
            string += str(x)
        return string

