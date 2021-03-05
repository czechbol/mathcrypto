import math
from .funcs import MathFunctions


class MultiplicativeGroup(object):
    def __init__(self, mod=None):
        self.mod = mod
        self.elements = self._generate_elements(mod)
        self.order = len(self.elements)
        self.generators = self._get_generators()

    def __repr__(self):
        return f'<MultiplicativeGroup mod="{self.mod}" order="{self.order}" elements="{self.elements}" generators="{self.generators}">'

    def _generate_elements(self, mod: int):
        """Generates all elements in the group"""
        elements = []
        for i in range(1, mod):
            if math.gcd(i, mod) == 1:
                elements.append(i)
        return elements

    def _get_generators(self):
        """Finds all generators of the group and """
        phi = MathFunctions.phi(self.mod)
        phi_factors = MathFunctions.factorize(phi)
        cleaned_factors = []
        for i in phi_factors:
            if i not in cleaned_factors:
                cleaned_factors.append(i)

        generators = []
        for element in self.elements:
            for factor in cleaned_factors:
                if pow(element, int(phi / factor), self.mod) == 1:
                    break
            else:
                generators.append(element)
        return generators

    def get_element_order(self, element):
        """Returns the order of an element in the group"""
        if element not in self.elements:
            raise ValueError
        if element in self.generators:
            return self.order

        s = set()
        for exp in range(len(self.elements)):
            s.add(element ** exp % self.mod)
        return len(s)

    def get_inverse_element(self, element: int):
        """Returns the inverse to an element in the group"""
        if element not in self.elements:
            raise ValueError
        inverse = pow(element, MathFunctions.phi(self.mod) - 1, self.mod)
        return inverse
