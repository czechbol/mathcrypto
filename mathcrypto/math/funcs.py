from ..cryptography.primes import Primes


class MathFunctions:
    """A collection of useful mathematical functions"""

    @classmethod
    def phi(cls, num: int) -> int:
        """Euler's Totient function Phi.
        If the number is not prime, the execution time depends on the speed of factorization.


        Args:
            num (int): Any positive whole number

        Returns:
            int: How many elements belong to a multiplicative group set by this number.
        """

        if Primes.is_probable_prime_fermat(num):
            return num - 1

        factors = Primes.factorize(num)
        totient = 1
        used = []
        for factor in factors:
            if factor in used:
                totient = totient * factor  # same as (totient * factor) but faster
            else:
                totient = totient * (factor - 1)  # same as (totient * (factor - 1)) but faster
                used.append(factor)
        return int(totient)

    @classmethod
    def euclid_gcd(cls, num_a: int, num_b: int) -> int:
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
    def crt(cls, lis) -> int:
        """Chinese remainder theorem

        Solves x for problems like:
            x ≡ 8 mod 9\n
            x ≡ 3 mod 5

        Args:
            lis : list
                of [int, int]:

        Example input:
            [[8, 9],[3, 5]] for the example problem

        Returns:
            int: Solution for x
        """

        M = 1
        temp = 0

        moduli = []
        for item in lis:
            if moduli == []:
                moduli.append(item[1])
                M *= item[1]
                continue

            for num in moduli:
                if cls.euclid_gcd(num, item[1]) != 1:
                    break
            else:
                moduli.append(item[1])
                M *= item[1]

        for item in lis:
            N = int(M / item[1])
            L = pow(N, MathFunctions.phi(item[1]) - 1, item[1])
            W = (L * N) % M
            temp += item[0] * W
        return temp % M

    @classmethod
    def eea(cls, modulus: int, number: int, verbose: bool = False) -> int:  # noqa: C901
        """Extended Euclidean Algorithm

        Get multiplicative inverse of a number in modulus

        Args:
            modulus (int): modulus of a multiplicative group
            number (int): number to get inverse to
            verbose (bool, optional): Whether to return a graphical solution. Defaults to False.

        Raises:
            ValueError: If number is not an element of the group defined by ``modulus``

        Returns:
            int: resulting inverse

        If verbose, returns:
            str: Graphical solution of the problem.
        """

        class EEA:
            def __init__(self, n: int, x: int):
                self.n = n
                self.x = x

                if cls.euclid_gcd(n, x) != 1:
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
