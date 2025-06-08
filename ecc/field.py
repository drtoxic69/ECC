class FieldElement:

    def __init__(self, num: int, prime: int):

        if num >= prime or num < 0:
            raise ValueError(f"{num} is not in Filed range 0 to {prime-1}")

        self.num   = num
        self.prime = prime
