class QuickHash:

    def __init__(self, e, q, p, b):
        self.e = e
        self.q = q
        self.p = p
        self.b = b

    def hash(self, x):
        return ((self.e * x + self.q) % self.p) % self.b
