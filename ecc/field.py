class FieldElement:

    def __init__(self, num: int, prime: int):

        if num >= prime or num < 0:
            raise ValueError(f"{num} is not in Filed range 0 to {prime-1}")

        self.num   = num
        self.prime = prime

    
    def __add__(self, other):
        
        if self.prime != other.prime:
            raise TypeError("Can not add the elements of different Field.")

        return FieldElement((self.num + other.num) % self.prime, self.prime)


    def __sub__(self, other):
        
        if self.prime != other.prime:
            raise TypeError("Can not subtract the elements of different Field.")

        return FieldElement((self.num - other.num) % self.prime, self.prime)

    
    def __mul__(self, other):

        if self.prime != other.prime:
            raise TypeError("Can not multiply the elements of different Field.")

        return FieldElement((self.num * other.num) % self.prime, self.prime)


    def __pow__(self, exponent: int):
       
        exponent = exponent % (self.prime - 1)
        return FieldElement(pow(self.num, self.exponet, self.prime), self.prime)


    def __repr__(self):

        return f"F_({self.prime}({self.num}))"


