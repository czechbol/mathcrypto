import math
import random
from itertools import count, islice


class MathFunctions:
    """A collection of useful mathematical functions"""

    @classmethod
    def is_prime(cls, num: int):
        """Classic number modulus check

        Tests divisibility by 2 and then every odd number up to sqrt(num).
        Takes longer to compute than Fermat's primality test but has 100% certainty.

        Args:
            num (int): Number to test

        Returns:
            bool: True if ``num`` is prime
        """

        if num < 2:
            return False

        if (num % 2) == 0:
            return False
        for number in islice(count(3, 2), int((math.sqrt(num) / 2) - 1)):
            if num % number == 0:
                return False
        return True

    @classmethod
    def auto_fermat_prime_test(cls, num: int, rounds: int, verbose: bool = False):
        """Automatic Fermat's primality test

        This test can not provide 100% certainty that the number is indeed prime,\
        so more than 1 round should be required.
        If determined that the number is not prime, that is on the other hand 100% certain.
        Tests for the number of rounds specified, 2-3 rounds are generally enough.
        If any round returns a result that is not 1, the number is not prime.

        Args:
            num (int): Number to be tested
            rounds (int): How many rounds of testing to perform
            verbose (bool, optional): Whether to return optional list of dictionary pairs "tester", "result". Defaults to False.

        Returns:
            bool: True if probably prime

        If verbose, returns:
            (tuple): tuple containing:

                - bool: True if probably prime
                - dict: Dictionary of "tester" and "result"
        """

        if num - 1 < 5:
            rounds = num - 1
        else:
            rounds = 5

            result_list = []
        is_prime = None
        for x in range(rounds):
            tester = random.randint(2, num - 2)
            res = pow(tester, num - 1, num)
            if res != 1:
                is_prime = False
            result_list.append({"tester": tester, "result": res})
        if is_prime is None:
            is_prime = True

        if verbose:
            return is_prime, result_list
        return is_prime

    @classmethod
    def manual_fermat_prime_test(cls, num: int, tester: int, verbose: bool = False):
        """Manual Fermat's primality test

        This test can not provide 100% certainty that the number is indeed prime,\
        so more than 1 round should be required.
        If determined that the number is not prime, that is on the other hand 100% certain.
        You should test for at least 2-3 rounds.
        If any round returns a result that is not 1, the number is not prime.

        Args:
            num (int): Number to be tested
            tester (int): Number to test the primality of ``num`` with
            verbose (bool, optional): Whether to return optional list of dictionary pairs "tester", "result". Defaults to False.

        Returns:
            bool: True if probably prime

        If verbose, returns:
            (tuple): tuple containing:

                - bool: True if probably prime
                - dict: Dictionary of "tester" and "result"
        """

        res = pow(tester, num - 1, num)
        result = {"tester": tester, "result": res}
        if res != 1:
            is_prime = False
        else:
            is_prime = True
        return is_prime, result

    @classmethod
    def factorize(cls, num: int):
        """Classic number factorization

        Tests divisibility by 2 and then every odd number up to sqrt(num)\
        while appending the factors. If the number contains multiple instances of a factor,\
        this function returns a list with duplicates.

        Args:
            num (int): Number to factorize

        Returns:
            list: List of factors including duplicates
        """

        factors = []

        while (num % 2) == 0:
            factors.append(2)
            num //= 2
        for number in islice(count(3, 2), int((math.sqrt(num) / 2) - 1)):
            while (num % number) == 0:
                factors.append(number)
                num //= number

        if num > 1:
            factors.append(num)
        return factors

    @classmethod
    def phi(cls, num: int):
        """Euler's Totient function Phi

        Args:
            num (int): Any positive whole number

        Returns:
            int: How many elements belong to a multiplicative group set by this number.
        """

        if cls.is_prime(num):
            return num - 1

        result = 0
        for i in range(1, num):
            if math.gcd(i, num) == 1:
                result += 1
        return result

    @classmethod
    def euclid_gcd(cls, num_a: int, num_b: int):
        """Euclidean algorithm

        Calculates the Greatest Common Divisor of two numbers.

        Args:
            num_a (int): First number
            num_b (int): Second number

        Returns:
            int: Greatest Common Divisor of the two numbers
        """

        if num_a == 0:
            return num_b
        return cls.euclid_gcd(num_b % num_a, num_a)

    @classmethod
    def crt(cls, lis):
        """Chinese remainder theorem

        Solves x for problems like:
            x ≡ 8 mod 9\n
            x ≡ 3 mod 5

        Args:
            lis : list
                of {str: int}:

        Example input:
            [{"modulus": 9, "result": 8},{"modulus": 3, "result": 5}] for the example problem

        Returns:
            int: Solution for x
        """

        M = 1
        temp = 0

        moduli = []
        for item in lis:
            if moduli == []:
                moduli.append(item["modulus"])
                M *= item["modulus"]

            for num in moduli:
                if math.gcd(num, item["modulus"]) != 1:
                    break
            else:
                moduli.append(item["modulus"])
                M *= item["modulus"]

        for item in lis:
            N = int(M / item["modulus"])
            L = pow(N, MathFunctions.phi(item["modulus"]) - 1, item["modulus"])
            W = (L * N) % M
            temp += item["result"] * W
        return temp % M

    @classmethod
    def eea(cls, modulus: int, number: int, verbose: bool = False):
        """Extended Euclidean Algorithm

        Get multiplicative inverse of a number in modulus

        Args:
            modulus (int): modulus of a multiplicative group
            number (int): number to get inverse to
            verbose (bool, optional): Whether to return a graphical solution. Defaults to False.

        Raises:
            ValueError: If number is not an eleent of the group defined by ``modulus``

        Returns:
            int: resulting inverse

        If verbose, returns:
            str: Graphical solution of the problem.
        """

        class EEA:
            def __init__(self, n: int, x: int):
                self.n = n
                self.x = x

                if math.gcd(n, x) != 1:
                    raise ValueError(f"{x} is not element of group Z_{n}^*.")

                self.table = self._compute_table()

            def _compute_table(self):
                """Compute values"""
                table = []

                # get initial row
                table.append([self.n, 0])

                # compute next rows
                left = self.x
                while left > 0:
                    table.append([left, table[-1][0] // left])
                    left = table[-2][0] - (left * table[-1][1])
                table.append([0, 0])

                # compute right column
                for i, row in enumerate(table):
                    # do not include the lowest row
                    if i == 0:
                        table[-i - 1].append(0)
                        continue

                    # add 0 and 1 going upwards
                    if i == 1:
                        table[-i - 1].append(0)
                        continue
                    if i == 2:
                        table[-i - 1].append(1)
                        continue

                    # get value
                    a = table[-i][1]
                    b = table[-i][2]
                    try:
                        c = table[-i + 1][2]
                    except IndexError:
                        # top row
                        c = 0
                    table[-i - 1].append(a * b + c)

                return table

            def _format_ascii_cell_left(self, row: int):
                return f"{self.table[row][0]} = {self.table[row-2][0]}-({self.table[row-1][0]}*{self.table[row-1][1]})"

            def _format_ascii_cell_right(self, row: int):
                return f"{self.table[row][2]} = {self.table[row+1][1]}*{self.table[row+1][2]}+{self.table[row+2][2]}"

            def _format_ascii_cell_middle(self, row: int):
                return f"{self.table[row][1]} = ⌊{self.table[row-1][0]}/{self.table[row][0]}⌋"

            def _format_ascii_cell(self, row: int, cell: int):
                # the top row starts with "n = "
                if row == 0 and cell == 0:
                    return f"n = {self.table[row][0]}"
                # the top row center is empty
                if row == 0 and cell == 1:
                    return ""
                # the first row starts with "x = "
                if row == 1 and cell == 0:
                    return f"x = {self.table[row][0]}"
                # the last row is "0, -, -"
                if row == len(self.table) - 1 and cell in (1, 2):
                    return ""
                # n-2th row ends with "1"
                if row == len(self.table) - 3 and cell == 2:
                    return "1"
                # n-1th row ends with "0"
                if row == len(self.table) - 2 and cell == 2:
                    return "0"
                # defaults
                if cell == 0:
                    return self._format_ascii_cell_left(row)
                if cell == 1:
                    return self._format_ascii_cell_middle(row)
                if cell == 2:
                    return self._format_ascii_cell_right(row)

                # an error
                raise ValueError(f"Wrong index: [{row}, {cell}]")

            def ascii(self):
                result = []
                for r in range(len(self.table)):
                    row = []
                    for c in range(3):
                        row.append(self._format_ascii_cell(r, c))
                    result.append(row)

                width = []
                for i in range(3):
                    width.append(max(len(s[i]) for s in result))

                canvas = []
                for row in result:
                    line = "  ".join(row[i].ljust(width[i]) for i in range(3))
                    canvas.append(line)

                resnum = self.table[0][2]
                if (resnum * self.x) % self.n != 1:
                    canvas.append(
                        f"Inverse for {self.x} in Z_{self.n}^* is -{resnum} mod {self.n} = {-resnum % self.n}."
                    )
                else:
                    canvas.append(f"Inverse for {self.x} in Z_{self.n}^* is {resnum}.")

                return "\n".join(canvas)

            @property
            def result(self):
                r = self.table[0][2]
                if (r * self.x) % self.n != 1:
                    r = -r % self.n
                return r

            def __str__(self):
                return f"Extended Euclidean Algorithm: {self.x} * ? = 1 (mod {self.n})"

            def __repr__(self):
                return f"<EEA n={self.n} x={self.x}>"

        if verbose:
            return EEA(modulus, number).ascii()
        else:
            return EEA(modulus, number).result
