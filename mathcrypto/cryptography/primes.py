import math
import random
from itertools import count, islice


class Primes:
    @classmethod
    def get_prime(cls, bit_length: int) -> int:
        """Get a n-bit prime

        Args:
            bit_length (int): Bit size of the desired prime number

        Returns:
            int: desired prime number
        """
        prime = random.getrandbits(bit_length)  # nosec
        while not cls.is_probable_prime_fermat(prime):
            prime = random.getrandbits(bit_length)
        return prime

    @classmethod
    def is_prime(cls, num: int) -> bool:
        """Classic number modulus check

        Tests divisibility by 2 and then every odd number up to sqrt(num).
        Takes longer to compute than Fermat's primality test but has 100% certainty.
        Cannot handle numbers larger than the system maxint.

        Args:
            num (int): Number to test

        Raises:
            OverflowError: If the number is too large

        Returns:
            bool: True if ``num`` is prime
        """

        if num < 2:
            return False

        if (num % 2) == 0:
            return False
        try:
            for number in islice(count(3, 2), int((math.sqrt(num) / 2) - 1)):
                if num % number == 0:
                    return False
        except OverflowError:
            raise OverflowError("The number is too large to process.")

        return True

    @classmethod
    def is_probable_prime_fermat(cls, num: int, rounds: int = 5) -> bool:
        """Automatic Fermat's primality test

        This test can not provide 100% certainty that the number is indeed prime, \
        so more than 1 round should be required.
        If determined that the number is not prime, that is on the other hand 100% certain.
        Tests for the number of rounds specified, 2-3 rounds are generally enough.
        If any round returns a result that is not 1, the number is not prime.

        Args:
            num (int): Number to be tested
            rounds (int): How many rounds of testing to perform
            verbose (bool, optional): Whether to return optional \
                list of [<number it was tested against>: `int`,<result>: `int`]. \
                Defaults to False.

        Returns:
            bool: True if probably prime

        If verbose, returns:
            (tuple): tuple containing:

                - bool: True if probably prime
                - list: List of [<number it was tested against>: `int`,<result>: `int`]
        """

        if num == 1 or num == 2:
            return True

        if num % 2 == 0:
            return False

        if num - 1 < rounds:
            rounds = num - 1
        else:
            rounds = rounds

        for i in range(rounds):
            testnum = random.randint(2, num - 1)
            if pow(testnum, num - 1, num) != 1:
                return False
        return True

    @classmethod
    def factorize(cls, num: int) -> list:
        """Classic number factorization

        Tests divisibility by 2 and then every odd number up to sqrt(num)\
        while appending the factors. If the number contains multiple instances of a factor,\
        this function returns a list with duplicates.
        Very fast unless the number is a compound of more than one large prime (more than 7 digits, 8 is still acceptable).

        Args:
            num (int): Number to factorize

        Returns:
            list: List of factors including duplicates
        """

        factors = []
        if cls.is_probable_prime_fermat(num):
            return [num]

        for number in range(2, math.isqrt(num) + 1):  # isqrt is the integer result of sqrt
            was_in_while = False
            while (num % number) == 0:  # same as (num % number) but faster
                was_in_while = True
                factors.append(int(number))
                num = int(num / number)  # same as int(num / number) but faster
            if was_in_while:
                if cls.is_probable_prime_fermat(num) or num == 1:
                    break

        if num > 1:
            factors.append(int(num))
        return factors
