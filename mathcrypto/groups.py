import math
from .funcs import MathFunctions


class MultiplicativeGroup:

    """Multiplicative group objects

    Attributes:
        mod (int): Modulus of the group
        elements (list): List of elements in the group
        order (order): Order of the group
        generators (generators): List of generators of the group
    """

    def __init__(self, mod):
        self.mod = mod
        self.elements = self._generate_elements(mod)
        self.order = len(self.elements)
        self.generators = self._get_generators()

    def __repr__(self):
        return f'<MultiplicativeGroup mod="{self.mod}" order="{self.order}" elements="{self.elements}" generators="{self.generators}">'

    def _generate_elements(self):
        """Generates all elements in the group

        Returns:
            list: list of elements
        """

        elements = []
        for i in range(1, self.mod):
            if math.gcd(i, self.mod) == 1:
                elements.append(i)
        return elements

    def _get_generators(self):
        """Finds all generators of the group

        Returns:
            list: list of generators
        """

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
        """Gets the order of an element in the group

        Args:
            element (int): Element of the group

        Raises:
            ValueError: When the ``element`` does not belong to the group

        Returns:
            int: Returns the order of ``element`` in the group
        """

        if element not in self.elements:
            raise ValueError
        if element in self.generators:
            return self.order

        s = set()
        for exp in range(len(self.elements)):
            s.add(element ** exp % self.mod)
        return len(s)

    def get_inverse_element(self, element: int):
        """Gets the inverse to an element in the group

        Args:
            element (int): Element of the group

        Raises:
            ValueError: When the ``element`` does not belong to the group

        Returns:
            int: Inverse element to ``element``
        """

        """Returns the inverse to an element in the group"""
        if element not in self.elements:
            raise ValueError
        inverse = pow(element, MathFunctions.phi(self.mod) - 1, self.mod)
        return inverse
