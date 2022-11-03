import math

class MyVector:
    vectors = []
    def __init__(self, a):
        self.vectors = a

    def __add__(self, other):
        new_vectors = []
        for i in range(len(self.vectors)):
            new_vectors.append(self.vectors[i] + other.vectors[i])

        return MyVector(new_vectors)

    def get_vector(self):
        return self.vectors

    def norm(self):
        sum = 0
        for i in range(len(self.vectors)):
            sum += self.vectors[i] ** 2
        
        return math.sqrt(sum)

    def __mul__(self, other):
        mul = 0
        for i in range(len(self.vectors)):
            mul += self.vectors[i] * other.vectors[i]
        return mul
