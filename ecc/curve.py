

class Curve:
    

    def __init__(self, a, b, P, G, n, h=1):

        """
        parameters: 
        a, b    : Curve parameters (y^2 = x^3 + ax + b).
        P       : Prime modulo for finite Field.
        G       : Generator point.
        n       : Order of Generator point.
        h       : Co-factor (usually 1).
        """
       
        self.a = a
        self.b = b

        self.P = P
        self.G = G
        self.n = n
    
        # Check if the curve is singular 
        if 4*(a**2) + 27*(b**2) == 0:
            raise ValueError("This is a singular curve (discriminant is zero). Choose different parameters for the curve.")
    

    def __repr__(self):

        return f"Curve: y^2 = x^3 + {self.a}x + {self.b} over the Field(Z/{self.P}Z)."


