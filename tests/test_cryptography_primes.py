import pytest

from mathcrypto.cryptography.primes import Primes


@pytest.mark.parametrize("num", [32, 64, 128])
def test_get_prime(num):
    assert Primes.is_probable_prime_fermat(Primes.get_prime(num), 10)


@pytest.mark.parametrize("num,expected", [(13, True), (240, False), (17, True)])
def test_is_prime(num, expected):
    assert Primes.is_prime(num) == expected


@pytest.mark.parametrize("num,expected", [(13, True), (240, False), (17, True)])
def test_is_probable_prime_fermat(num, expected):
    assert Primes.is_probable_prime_fermat(num) == expected


@pytest.mark.parametrize("num,expected", [(123, [3, 41]), (13, [13]), (24, [2, 2, 2, 3])])
def test_factorize(num, expected):
    assert Primes.factorize(num) == expected
